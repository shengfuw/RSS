import argparse
import csv
import itertools
import os
import math
import matplotlib.pyplot as plt
import multiprocessing
import numpy as np
from scipy.stats import truncnorm

from args import ArgsModel


def get_truncated_normal(mean=0, sd=1, low=0, upp=10):
    return truncnorm(
        (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)


class Agent(object):
    _ids = itertools.count(0)

    def __init__(self, args) -> None:
        super().__init__()
        
        self.id = next(self._ids)

        self.thres = None
        self.M = args.M
        self.net = None
        self.R = None
        self.I = None
        self.E = None

        self.S = 0
        self.O = 0
        self.is_volunteer = False
    
    @staticmethod
    def draw(p):
        return True if np.random.uniform() < p else False
    
    def set_param(self, thres, R, I, E):
        self.thres, self.R, self.I, self.E = thres, R, I, E
    
    def add_net_member(self, ag):
        if self.net is None:
            self.net = list()
        self.net.append(ag)
    
    def to_volunteer(self, pi) -> None:
        #print("agent {} | pi = {:4f}".format(("  "+str(self.id))[-3:], pi))
        if self.thres == 1 and pi == 0:
            self.is_volunteer = False
        elif self.thres == 0 and pi == 1:
            self.is_volunteer = True
        else:
            p = 1/(1+math.exp(self.M * (self.thres - pi)))
            self.is_volunteer = self.draw(p)
    
    def get_net_pi(self):
        if self.net is None:
            raise TypeError("haven't initialized social net for the agent.")
        return sum([1 for ag in self.net if ag.is_volunteer]) / len(self.net)
    

class PublicGoodsGame(object):

    def __init__(self, args: argparse.ArgumentParser, verbose=True) -> None:
        super().__init__()
        Agent._ids = itertools.count(0)
        
        self.verbose = verbose
        self.args = args
        if self.verbose:
            print("Args: {}".format(args))

        self.ags = self.init_ags(args)
        self.global_pi = self._get_global_pi()

        self.total_R = sum([ag.R for ag in self.ags])
        self.global_R_ratio = self._get_global_R_ratio()

        self.R_ratio_list = list()
        self.R_ratio_list.append(self.global_R_ratio)

        self.L = 0
    
    @staticmethod
    def get_thres(thres_type: str, mean=0.5, sd=0.1):
        if thres_type == "all_defector":
            return 1.
        elif thres_type == "uniform":
            return np.random.uniform()
        elif thres_type == "normal":
            return get_truncated_normal(mean=mean, sd=sd, low=0, upp=1).rvs()

    @staticmethod
    def get_RI(R_type, I_type, corr_RI, mean=1, sd=0.5):
        if R_type == "normal" and I_type == "normal":
            x1 = get_truncated_normal(mean=mean, sd=sd, low=0, upp=np.inf).rvs()
            x2 = get_truncated_normal(mean=mean, sd=sd, low=0, upp=np.inf).rvs()
            if corr_RI == "orthogonal":
                return float(x1), float(x2)
            elif corr_RI == "pos":
                return float(x1), float(x1)
            elif corr_RI == "neg":
                return float(x1), -float(x1)
        elif R_type == "equal" and I_type == "normal":
            x1 = get_truncated_normal(mean=mean, sd=sd, low=0, upp=np.inf).rvs()
            return 1., float(x1)
        else:
            raise TypeError("haven't coded distributions other than normal.")
    
    @staticmethod
    def get_E(E_type, mean=0.5, sd=0.1):
        if E_type == "normal":
            return get_truncated_normal(mean=mean, sd=sd, low=0, upp=1).rvs()
    
    @staticmethod
    def check_distribution(ags):
        R = np.array([ag.R for ag in ags])
        I = np.array([ag.I for ag in ags])
        E = np.array([ag.E for ag in ags])
        print("R: mean={:5f}; sd={:5f}".format(np.mean(R), np.std(R)))
        print("I: mean={:5f}; sd={:5f}".format(np.mean(I), np.std(I)))
        print("E: mean={:5f}; sd={:5f}".format(np.mean(E), np.std(E)))
    
    @staticmethod
    def get_group_dis_n(n_ag, n_group=21, low=3, high=6) -> list:
        group_dis_n = [low] * n_group
        n_ag_ctr = low * n_group
        while n_ag_ctr < n_ag:
            chosen_gp = np.random.randint(n_group)
            if group_dis_n[chosen_gp] < high:
                group_dis_n[chosen_gp] += 1
                n_ag_ctr += 1
        assert(sum(group_dis_n) == n_ag)
        return group_dis_n
    
    @staticmethod
    def get_randint(low, high, exclude, size:int) -> list:
        ctr = 0
        ans = list()
        while ctr < size:
            chosen_ag = np.random.randint(low, high)
            if chosen_ag != exclude:
                ans.append(chosen_ag)
                ctr += 1
        return ans

    def init_ags(self, args: argparse.ArgumentParser) -> list:
        ags = list()

        # built agents
        for _ in range(args.N):
            ag = Agent(args)
            thres = self.get_thres(args.thres_type)
            R, I = self.get_RI(args.R_type, args.I_type, args.corr_RI)
            E = self.get_E(args.E_type)
            ag.set_param(thres, R, I, E)
            ags.append(ag)
        if self.verbose:
            self.check_distribution(ags)

        # build network (undirected graph)
        if args.net_group == "strong":
            n_ag_ctr = 0
            for n_ag_gp in self.get_group_dis_n(args.N):
                for i in range(n_ag_ctr, n_ag_ctr+n_ag_gp):
                    for j in range(i+1, n_ag_ctr+n_ag_gp):
                        ags[i].add_net_member(ags[j])
                        ags[j].add_net_member(ags[i])
                n_ag_ctr += n_ag_gp
        if args.net_group == "weak":
            for ag_ctr, ag in enumerate(ags):
                for chosen_ag in self.get_randint(0, args.N, ag_ctr, size=3):
                    ag.add_net_member(ags[chosen_ag])
        return ags   

    def _get_global_pi(self):
        return sum([1 for ag in self.ags if ag.is_volunteer]) / self.args.N
    
    def _get_global_R_ratio(self):
        return sum([ag.R for ag in self.ags if ag.is_volunteer]) / self.total_R
    
    def get_ag_pi(self, ag:Agent):
        # paper: pi is "the participation rate"
        if self.args.net_group == "parallel":
            return 0.5
        elif self.args.net_group == "serial":
            return self.global_pi
        elif self.args.net_group in {"strong", "weak"}:
            return ag.get_net_pi()

    def simulate_iter(self, epsilon=10**-6):
        """ At iteration i:
        1. determine status of every agent based on pi_{i-1}.
        2. update global_pi and global_R_ratio
        3. calculate L; and find S_ij and O_ij for every agent j
        4. update T_ij for every agent j
        """
        # 1.
        for ag in self.ags:
            ag.to_volunteer(pi=self.get_ag_pi(ag))
        
        # 2.
        self.global_pi = self._get_global_pi()
        self.global_R_ratio = self._get_global_R_ratio()

        # 3.
        # paper: pi is "the rate of contribution"
        self.L = 1/(1+math.exp(10*(0.5-self.global_R_ratio))) - (1-self.args.X)/2
        S_max = -np.inf
        for ag in self.ags:
            S_ij = self.L*self.total_R*ag.I/(self.total_R**(1-self.args.J)) - int(ag.is_volunteer)*ag.R
            O_ij = ag.E * (2*S_ij - ag.S)
            S_max = max(S_max, abs(S_ij))
            ag.S = S_ij
            ag.O = O_ij
        
        # 4.
        for ag in self.ags:
            ag.O = ag.O / (3*S_max)
            ag.O += epsilon
            
            t_drop = ag.O * (1 - (1-ag.thres)**(1/abs(ag.O)))
            t_increase = ag.O * (1 - ag.thres**(1/abs(ag.O)))
            t_drop = 0 if np.isnan(t_drop) else t_drop
            t_increase = 0 if np.isnan(t_increase) else t_increase

            # threshold drops
            if ag.is_volunteer and ag.O>0:
                ag.thres -= t_drop
            elif not ag.is_volunteer and ag.O<0:
                ag.thres += t_drop
            # threshold increases
            elif ag.is_volunteer and ag.O<0:
                ag.thres -= t_increase
            elif not ag.is_volunteer and ag.O>0:
                ag.thres += t_increase
            
            ag.thres = min(ag.thres, 1.)
            ag.thres = max(ag.thres, 0.)

    def simulate(self, log_v=50):
        if self.verbose:
            print("| iter   0 | pi = {:.4f}; R = {:.4f}; L = {:.4f}".format(self.global_pi, self.global_R_ratio, self.L))
        for iter in range(1, self.args.n_iter+1):
            self.simulate_iter()
            self.R_ratio_list.append(self.global_R_ratio) # pi: the rate of contribution
            if self.verbose and iter % log_v == 0:
                print("| iter {} | pi = {:.4f}; R = {:.4f}; L = {:.4f}".format(("  "+str(iter))[-3:], self.global_pi, self.global_R_ratio, self.L))
    
    def get_pi_list(self):
        return np.array(self.R_ratio_list)


class PlotLinesHandler(object):

    def __init__(self, xlabel, ylabel, ylabel_show,
        figure_size=(9, 9), output_dir=os.path.join(os.getcwd(), "imgfiles")) -> None:
        super().__init__()

        self.output_dir = output_dir
        self.title = "{}-{}".format(ylabel, xlabel)
        self.legend_list = list()

        plt.figure(figsize=figure_size, dpi=80)
        plt.title("{} - {}".format(ylabel_show, xlabel))
        plt.xlabel(xlabel)
        plt.ylabel(ylabel_show)
        ax = plt.gca()
        ax.set_ylim([0., 1.])

    def plot_line(self, data, legend,
        linewidth=1, color="", alpha=1.0):
        self.legend_list.append(legend)
        if color:
            plt.plot(np.arange(data.shape[-1]), data,
                linewidth=linewidth, color=color, alpha=alpha)
        else:
            plt.plot(np.arange(data.shape[-1]), data, linewidth=linewidth)

    def save_fig(self, title_param="", add_legend=True, title_lg=""):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        if add_legend:
            plt.legend(self.legend_list)
            title_lg = "_".join(self.legend_list)
        fn = "_".join([self.title, title_lg, title_param]) + ".png"
            
        plt.savefig(os.path.join(self.output_dir, fn))
        print("fig save to {}".format(os.path.join(self.output_dir, fn)))


N_RANDOM_TRAILS = 10
COLORS = ["red", "blue"]

if __name__ == "__main__":
    parser = ArgsModel()
    
    ## multiple trails on one condition
    custom_legend = "Pos vs. Neg"
    args_dict = parser.get_fig_args(1)
    plot_line_hd = PlotLinesHandler(xlabel="Iteration", ylabel="pi",
                                    ylabel_show="Level of Contribution "+r"$\pi$")
    for n_trail in range(N_RANDOM_TRAILS):
        for args_ctr, (exp_legend, exp_args) in enumerate(args_dict.items()):
            print("| trail {}/{} |".format(n_trail+1, N_RANDOM_TRAILS))
            np.random.seed(seed=exp_args.seed+n_trail)
            game = PublicGoodsGame(exp_args, verbose=False)
            game.simulate()
            plot_line_hd.plot_line(game.get_pi_list(), "",
                color=COLORS[args_ctr], alpha=0.15)
            param = "N_{}_T_{}_ntrails_{}".format(exp_args.N, exp_args.thres_type, N_RANDOM_TRAILS)
    plot_line_hd.save_fig(param, add_legend=False, title_lg=custom_legend)

    # ## figure 1
    # args_dict = parser.get_fig_args(1)
    # plot_line_hd = PlotLinesHandler(xlabel="Iteration", ylabel="pi",
    #                                 ylabel_show="Level of Contribution "+r"$\pi$")
    # for exp_legend, exp_args in args_dict.items():
    #     np.random.seed(seed=exp_args.seed)
    #     game = PublicGoodsGame(exp_args)
    #     game.simulate()
    #     plot_line_hd.plot_line(game.get_pi_list(), exp_legend)
    #     param = "N_{}_T_{}".format(exp_args.N, exp_args.thres_type)
    # plot_line_hd.save_fig(param)

    # ## figure 2
    # args_dict = parser.get_fig_args(2)
    # plot_line_hd = PlotLinesHandler(xlabel="Iteration", ylabel="pi",
    #                                 ylabel_show="Level of Contribution "+r"$\pi$")
    # for exp_legend, exp_args in args_dict.items():
    #     np.random.seed(seed=exp_args.seed)
    #     game = PublicGoodsGame(exp_args)
    #     game.simulate()
    #     plot_line_hd.plot_line(game.get_pi_list(), exp_legend)
    #     param = "N_{}_T_{}".format(exp_args.N, exp_args.thres_type)
    # plot_line_hd.save_fig(param)