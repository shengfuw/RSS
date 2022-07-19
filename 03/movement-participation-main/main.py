import argparse
from cgi import print_environ
import csv
import itertools
import os
import math
import matplotlib.pyplot as plt
import multiprocessing
import numpy as np
from scipy.stats import truncnorm
from scipy.stats import pearsonr

from args import ArgsModel

EPSILON = 10**-11

def get_truncated_normal(mean=0, sd=1, low=0, upp=10):
    return truncnorm(
        (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)

def get_chi_square(size=None, df=3, mean=1):
    """ return: float or a ndarray of float (if size is given) """
    if size is None:
        return float(np.random.chisquare(df)) / df * mean
    else:
        return np.random.chisquare(df, size=size) / df * mean


class Agent(object):
    _ids = itertools.count(0)

    def __init__(self, args) -> None:
        super().__init__()
        
        self.id = next(self._ids)

        # net
        self.net = None
        self.not_in_net = None

        # following chi-square
        self.R = None
        self.I = None
        self.P = None

        # sum param
        self.sum_R = None
        self.sum_P = None

        # the degree of influence ego i exert over j
        # a list of len(agents)
        self.P_ij = None

        # initalized as all defectors
        self.is_volunteer = 0

        # N and density
        self.net_n = args.N
        self.net_density = args.net_density

        # I_delta in iteration i
        self.I_delta = 0
    
    def set_param_PRI(self, P:float, R:float, I:float):
        R, I, P = list(map(float, [R, I, P]))
        self.R, self.I, self.P = R, I, P
    
    def set_param_sum_PR(self, sum_P: float, sum_R:float):
        sum_R, sum_P = list(map(float, [sum_R, sum_P]))
        self.sum_R, self.sum_P = sum_R, sum_P
    
    def update_I(self):
        self.I += self.I_delta
        self.I = min(100.0, self.I)
        self.I_delta = 0
    
    def add_net_member(self, ag):
        if self.net is None:
            self.net = list()
        self.net.append(ag)
    
    def add_not_in_net_member(self, ag):
        if self.not_in_net is None:
            self.not_in_net = list()
        self.not_in_net.append(ag)
    
    @staticmethod
    def _draw(p):
        return 1 if np.random.uniform() < p else 0
    
    def _get_p_ij(self, p_i: float, p_j:float) -> float:
        return math.sqrt(p_i/(p_i+p_j+EPSILON) * p_i/(self.sum_P-p_i))
    
    def _get_net_pi(self):
        if self.net is not None:
            pi_is_not_volun = sum([ag.R*ag.is_volunteer for ag in self.net]) / self.sum_R
        else:
            pi_is_not_volun = 0.0
        
        # if self.not_in_net is not None:
        #     pi_is_volun = pi_is_not_volun + (self.R + sum([self._get_p_ij(self.P, ag.P)*ag.R*(1-ag.is_volunteer) for ag in self.not_in_net])) / self.sum_R
        # else:
        #     pi_is_volun = pi_is_not_volun + (self.R) / self.sum_R
        
        if self.net is not None:
            pi_is_volun = (pi_is_not_volun + self.R + sum([self._get_p_ij(self.P, ag.P)*ag.R*(1-ag.is_volunteer) for ag in self.net])) / self.sum_R
        else:
            pi_is_volun = (pi_is_not_volun + self.R) / self.sum_R

        # if self.net is not None:
        #     pi_is_volun = pi_is_not_volun + (self.R + sum([self._get_p_ij(self.P, ag.P)*ag.R*(1-ag.is_volunteer) for ag in self.net])) / self.sum_R
        # else:
        #     pi_is_volun = pi_is_not_volun + (self.R) / self.sum_R

        return (pi_is_not_volun, pi_is_volun)
    
    @staticmethod
    def _get_production_level(pi):
        return 1 / (1 + math.exp(10*(0.5-pi)))

    def to_volunteer(self) -> None:
        # eq. 8
        pi_is_not_vol, pi_is_vol = self._get_net_pi()
        expect_is_not_vol = self._get_production_level(pi_is_not_vol)*self.sum_R*self.I
        expect_is_vol = self._get_production_level(pi_is_vol)*self.sum_R*self.I - self.R
        expect_marginal = (expect_is_vol - expect_is_not_vol) / self.R
        # print(pi_is_vol, expect_is_vol)
        # print(pi_is_not_vol, expect_is_not_vol)
        p = 0
        try:
            p = 1 / (1 + math.exp(10*(1.0-expect_marginal)))
        except:
            if 1.0-expect_marginal > 0:
                p = 0.0
            else:
                p = 1.0
        # print(p)
        # print("===============")
        self.is_volunteer = self._draw(p)
    
    def to_influence(self) -> None:
        if self.net is None:
            return
        
        if self.is_volunteer:
            others_list = [ag_j for ag_j in self.net if (not ag_j.is_volunteer and self.I > ag_j.I) or ag_j.is_volunteer]
            others_list = sorted(others_list, key=lambda ag_j: ag_j.R*(self.P/(ag_j.P+EPSILON)), reverse=True)
            resourse_left = self.R
            for ag_j in others_list:
                if not ag_j.is_volunteer:
                    # eq.10; participate influence not participate
                    ag_j.I += (self.I-ag_j.I) * self._get_p_ij(self.P, ag_j.P)
                else:
                    # eq.12; participate influence participate
                    ag_j.I += (math.sqrt(self.I**2 + ag_j.I**2) - ag_j.I) * self._get_p_ij(self.P, ag_j.P)
                resourse_left -= 1 / (self.net_n*self.net_density) * max(1.0, ag_j.P/(self.P+EPSILON))
                if resourse_left <= 0:
                    break
        else:
            others_list = [ag_j for ag_j in self.net if ag_j.is_volunteer and self.I < ag_j.I]
            others_list = sorted(others_list, key=lambda ag_j: ag_j.R*(self.P/(ag_j.P+EPSILON)), reverse=True)
            resourse_left = self.R
            for ag_j in others_list:
                if ag_j.is_volunteer:
                    # eq.11; not participate influence participate
                    ag_j.I += (self.I-ag_j.I) * self._get_p_ij(self.P, ag_j.P)
                resourse_left -= 1 / (self.net_n*self.net_density) * max(1, ag_j.P/(self.P+EPSILON))
                if resourse_left <= 0:
                    break


class PublicGoodsGame(object):

    def __init__(self, args: argparse.ArgumentParser, verbose=True) -> None:
        super().__init__()

        Agent._ids = itertools.count(0)
        self.verbose = verbose

        self.args = args
        if self.verbose:
            print("Args: {}".format(args))

        self.ags, self.relation_matrix = self.init_ags()
        
        # record
        self.avg_I_list = list()
        self.avg_I_list.append(self._get_global_interest())
        self.total_contribution_list = list()
        self.total_contribution_list.append(self._get_global_contribution())
    

    @staticmethod
    def get_exclude_randint(N, low, high, exclude, size:int) -> list:
        """ Sample from [0, N) with [low, high) excluded. Return a list of ints. """
        ctr = 0
        s = np.zeros(N)
        s[exclude] = 1.0
        ans = list()
        while ctr < min(size, N-(high-low)):
            chosen_ag = np.random.randint(0, N)
            if (chosen_ag < low or chosen_ag >= high) and s[chosen_ag] == 0.0:
                ans.append(chosen_ag)
                s[chosen_ag] = 1.0
                ctr += 1
        return ans
    

    @staticmethod
    def get_randint(low, high, exclude, size:int) -> list:
        """ Sample from [low, high). Return a list of ints. """
        ctr = 0
        s = np.zeros(high)
        s[exclude] = 1.0
        ans = list()
        while ctr < min(size, high-low):
            chosen_ag = np.random.randint(low, high)
            if s[chosen_ag] == 0.0:
                ans.append(chosen_ag)
                s[chosen_ag] = 1.0
                ctr += 1
        return ans
    

    def init_ags(self) -> list:
        # built network 
        relation_matrix = np.zeros((self.args.N, self.args.N))
        edges_n = self.args.N*(self.args.N-1) * self.args.net_density
        edges_ag = list(np.round(get_chi_square(size=self.args.N, df=self.args.net_df, mean=edges_n/self.args.N), 0).astype(np.int32))

        ## group into 5 groups, 30% of the ties are sent across groups
        for g_idx in range(5):
            ag_idx_low, ag_idx_high = int(self.args.N*g_idx/5), int(self.args.N*(g_idx+1)/5)
            for ag_i in range(ag_idx_low, ag_idx_high): # group members: index from [low, high)
                j = list()
                e_n = edges_ag[ag_i]
                # across groups
                for ag_j in self.get_exclude_randint(self.args.N, ag_idx_low, ag_idx_high, ag_i, size=round(e_n*0.3)):
                    relation_matrix[ag_i][ag_j] = 1.0
                    j.append(ag_j)
                # within groups
                for ag_j in self.get_randint(ag_idx_low, ag_idx_high, ag_i, size=e_n-round(e_n*0.3)):
                    relation_matrix[ag_i][ag_j] = 1.0
                    j.append(ag_j)
        
        # P
        ## calculate the eigenvalues
        ## and choose the eigenvectors of the largest eigenvalue for P = [P_1, P_2, ..., P_N]

        # method 1
        # w, v = np.linalg.eig(relation_matrix)
        # P = np.abs(v[:, np.argmax(w)])

        # method 2
        P = get_chi_square(size=self.args.N, df=self.args.P_df, mean=1)

        CORR_STANDARD_ALPHA = 0.01

        # R
        R = None
        while True:
            R = get_chi_square(size=self.args.N, df=self.args.R_df, mean=1)
            r, p_value = pearsonr(P, R)
            if self.args.r_RP * r > 0 and p_value < CORR_STANDARD_ALPHA:
                print("Success | r_RP = {:5f}; p-value={:3f}".format(r, p_value))
                break
            # else:
            #     print("Fail    | r_RP = {:5f}; p-value={:3f}".format(r, p_value))
        
        # I
        I = None
        while True:
            I = get_chi_square(size=self.args.N, df=self.args.I_df, mean=1)
            r, p_value = pearsonr(P, I)
            if self.args.r_IP * r > 0 and p_value < CORR_STANDARD_ALPHA:
                print("Success | r_IP = {:5f}; p-value={:3f}".format(r, p_value))
                break
            # else:
            #     print("Fail    | r_IP = {:5f}; p-value={:3f}".format(r, p_value))
                
        # build agents
        ags = list()
        for ag_idx in range(self.args.N):
            ag = Agent(self.args)
            ag.set_param_PRI(P[ag_idx], R[ag_idx], I[ag_idx])
            ag.set_param_sum_PR(np.sum(P), np.sum(R))
            ags.append(ag)
        
        # build network
        for ag_i in range(self.args.N):
            for ag_j in range(self.args.N):
                if relation_matrix[ag_i][ag_j] == 1.0:
                    ags[ag_i].add_net_member(ags[ag_j])
                elif ag_i != ag_j:
                    ags[ag_i].add_not_in_net_member(ags[ag_j])
        
        if self.verbose:
            self.check_distribution(ags, self.args)
        
        return ags, relation_matrix


    @staticmethod
    def check_distribution(ags, args):
        edges_n = args.N*(args.N-1) * args.net_density

        tie = np.array([len(ag.net) if ag.net is not None else 0 for ag in ags])
        R = np.array([ag.R for ag in ags])
        I = np.array([ag.I for ag in ags])
        P = np.array([ag.P for ag in ags])

        # back to original X^2 distribution
        ori_tie = tie / (edges_n/args.N) * args.net_df
        ori_R = R / 1 * args.R_df
        ori_I = I / 1 * args.I_df

        print("\mu * (# of ties) ~ X^2({}): mean={:5f}; sd={:5f}".format(args.net_df, np.mean(ori_tie), np.std(ori_tie)))
        print("\mu * P: mean={:5f}; sd={:5f}".format(np.mean(P), np.std(P)))
        print("\mu * R ~ X^2({}): mean={:5f}; sd={:5f}".format(args.R_df, np.mean(ori_R), np.std(ori_R)))
        print("\mu * I ~ X^2({}): mean={:5f}; sd={:5f}".format(args.I_df, np.mean(ori_I), np.std(ori_I)))
    

    def _get_global_interest(self):
        return sum([ag.I for ag in self.ags]) / self.args.N
    
    
    def _get_global_contribution(self):
        return sum([ag.R for ag in self.ags if ag.is_volunteer])
    

    def get_avg_I_list(self):
        return np.array(self.avg_I_list)
    

    def get_contribution_list(self):
        return np.array(self.total_contribution_list)
    

    def simulate_iter(self):
        """ At iteration i:
        1. ego i determine whether to parcipate
        2. ego i tries to influence other
        """
        # 1.
        for ag in self.ags:
            ag.to_volunteer()
        
        for ag in self.ags:
            ag.to_influence()
            ag.update_I()

        # record
        self.avg_I_list.append(self._get_global_interest())
        self.total_contribution_list.append(self._get_global_contribution())
    

    def simulate(self, log_v=50):
        if self.verbose:
            print("| iter   0 | avg_I = {:.4f}; global contribution = {:.4f}".format(self.avg_I_list[-1], self.total_contribution_list[-1]))
        for iter in range(1, self.args.n_iter+1):
            self.simulate_iter()
            if self.verbose and iter % log_v == 0:
                print("| iter {} | avg_I = {:.4f}; global contribution = {:.4f}".format(("  "+str(iter))[-3:], self.avg_I_list[-1], self.total_contribution_list[-1]))

    
    


class PlotLinesHandler(object):
    _ids = itertools.count(0)

    def __init__(self, xlabel, ylabel, ylabel_show,
        figure_size=(9, 9), output_dir=os.path.join(os.getcwd(), "imgfiles")) -> None:
        super().__init__()

        self.id = next(self._ids)

        self.output_dir = output_dir
        self.title = "{}-{}".format(ylabel, xlabel)
        self.legend_list = list()

        plt.figure(self.id, figsize=figure_size, dpi=80)
        plt.title("{} - {}".format(ylabel_show, xlabel))
        plt.xlabel(xlabel)
        plt.ylabel(ylabel_show)

        ax = plt.gca()
        ax.set_ylim([0., 100.])

    def plot_line(self, data, legend,
        linewidth=1, color="", alpha=1.0):

        plt.figure(self.id)
        self.legend_list.append(legend)
        if color:
            plt.plot(np.arange(data.shape[-1]), data,
                linewidth=linewidth, color=color, alpha=alpha)
        else:
            plt.plot(np.arange(data.shape[-1]), data, linewidth=linewidth)

    def save_fig(self, title_param="", add_legend=True, title_lg=""):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        plt.figure(self.id)
        if add_legend:
            plt.legend(self.legend_list)
            title_lg = "_".join(self.legend_list)
        fn = "_".join([self.title, title_lg, title_param]) + ".png"
            
        plt.savefig(os.path.join(self.output_dir, fn))
        print("fig save to {}".format(os.path.join(self.output_dir, fn)))


N_RANDOM_TRAILS = 30
COLORS = ["red", "blue"]

if __name__ == "__main__":
    parser = ArgsModel()
    
    ## multiple trails on one condition
    custom_legend = "Test"
    args_dict = parser.get_args()
    avg_I_hd = PlotLinesHandler(xlabel="Iteration", ylabel="contrib",
                                ylabel_show="Total Contribution")
    contrib_hd = PlotLinesHandler(xlabel="Iteration", ylabel="avgI",
                                  ylabel_show="Average level of Interest")
    for exp_legend, exp_args in args_dict.items():
        np.random.seed(seed=exp_args.seed)
        game = PublicGoodsGame(exp_args)
        game.simulate()

        avg_I_hd.plot_line(game.get_avg_I_list(), exp_legend)
        contrib_hd.plot_line(game.get_contribution_list(), exp_legend)
        param = ""
    avg_I_hd.save_fig(param)
    contrib_hd.save_fig(param)