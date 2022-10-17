import os
import csv
import argparse
import itertools
from tkinter import Y
from turtle import shape
import numpy as np
import matplotlib.pyplot as plt
from args import ArgsModel
from scipy.stats import truncnorm

N_RANDOM_TRAILS = 100 
# N_RANDOM_TRAILS = 3
RAMOM_SEED = 123
COLORS = ["red", "blue"]
CWD = os.path.dirname(os.path.abspath(__file__))

def get_truncated_normal(mean=0, sd=1, low=0, upp=np.inf):
    return truncnorm((low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)

class Agent(object):
    _ids = itertools.count(0)

    def __init__(self, args) -> None:
        super().__init__()
        self.id = next(self._ids)

        self.thres = None # Thershold
        self.net = None # Network
        self.R = None # Resource
        self.I = None # Interest
        self.E = None # Learning rate
        self.M = args.M # Slope parameter

        self.S = 0 # Share of the public goods
        self.O = 0 # Outcome
        self.is_volunteer = False # Whether to participate 
    
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
        prob = 1 / (1 + np.exp((self.thres - pi)*self.M)) # Formula 1
        self.is_volunteer = self.draw(prob)
    
    def get_net_pi(self):
        if self.net is None:
            raise TypeError("haven't initialized social net for the agent.")
        return sum([ag.is_volunteer for ag in self.net]) / len(self.net) 

class PublicGoodsGame(object):
    def __init__(self, args: argparse.ArgumentParser, verbose=True) -> None:
        super().__init__()
        Agent._ids = itertools.count(0)
        
        self.verbose = verbose
        self.args = args
        if self.verbose:
            print("Args: {}".format(args))

        self.ags = self.init_ags(args)

        self.total_R = sum([ag.R for ag in self.ags]) # Total resource
        self.global_pi = self._get_global_pi()
        self.global_R_ratio = self._get_global_R_ratio()

        self.R_ratio_list = list()
        self.R_ratio_list.append(self.global_R_ratio)

        self.L = 0 # Level of production
    
    @staticmethod
    def get_thres(thres_type: str, mean=0.5, sd=0.1): # Initial threshold for every agent
        if thres_type == "all_defector":
            return 1.
        elif thres_type == "uniform":
            return np.random.uniform()
        elif thres_type == "normal":
            return get_truncated_normal(mean=mean, sd=sd, low=0, upp=1).rvs()

    @staticmethod
    def get_RI(R_type, I_type, corr_RI, mean=1, sd=0.5):
        if R_type == "normal" and I_type == "normal":
            ################ Q3, Q4-2 #################
            x1 = get_truncated_normal(mean=mean, sd=sd, low=0, upp=np.inf).rvs() # R default
            x2 = get_truncated_normal(mean=mean, sd=sd, low=0, upp=np.inf).rvs() # I default
            # x1 = get_truncated_normal(mean=mean, sd=.1, low=0, upp=np.inf).rvs()
            # x2 = get_truncated_normal(mean=mean, sd=.1, low=0, upp=np.inf).rvs()
            #########################################
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
    ################# Q3 #################
    def get_E(E_type, mean=0.5, sd=0.5): # default
    # def get_E(E_type, mean=0, sd=1): 
    ######################################
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

        # Built agents
        for _ in range(args.N):
            ag = Agent(args)
            thres = self.get_thres(args.thres_type)
            R, I = self.get_RI(args.R_type, args.I_type, args.corr_RI)
            E = self.get_E(args.E_type)
            ag.set_param(thres, R, I, E)
            ags.append(ag)
        if self.verbose:
            self.check_distribution(ags)

        ############### Q4-1 ###############
        ## default ##
        total_R = sum([ag.R for ag in ags])
        for ag in ags:
            ag.R = ag.R / total_R
        #############
        # max_R = max([ag.R for ag in ags])
        # for ag in ags:
        #     ag.R = ag.R / max_R
        ####################################

        # Build network (undirected graph)
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
        return sum([ag.is_volunteer for ag in self.ags]) / self.args.N
    
    def _get_global_R_ratio(self):
        return sum([ag.R for ag in self.ags if ag.is_volunteer]) / self.total_R
    
    def get_ag_pi(self, ag:Agent):
        if self.args.net_group == "parallel":
            return 0
        elif self.args.net_group == "serial":
            ######### Q2 #########
            return self._get_global_pi() # default: synchronous
            # return self.global_pi # asynchronous
            ######################
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
        ############## Q1-2 ##############
        # Formula 3 
        self.L = 1/(1 + np.exp((.5-self.global_pi)*10)) - (1-self.args.X)/2 # default
        # self.L = 1/(1 + np.exp((.5-self.global_R_ratio)*10)) - (1-self.args.X)/2 
        ##################################
        S_max = -np.inf
        for ag in self.ags:
            # Value of j's share
            S_ij = self.L*self.total_R*ag.I/(self.total_R**(1-self.args.J)) - int(ag.is_volunteer)*ag.R # formula 4
            # Standardized outcome
            O_ij = ag.E * (2*S_ij - ag.S) # formula 5
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
            
            # formula 6
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
            ##############  Q1-1 ##############
            self.R_ratio_list.append(self.global_pi) # default
            # self.R_ratio_list.append(self.global_R_ratio) 
            ###################################
            if self.verbose and iter % log_v == 0:
                print("| iter {} | pi = {:.4f}; R = {:.4f}; L = {:.4f}".format(("  "+str(iter))[-3:], self.global_pi, self.global_R_ratio, self.L))
    
    def get_pi_list(self):
        return np.array(self.R_ratio_list)

########## Some utilities ##########
def save_to_csv(record_data, file_name):
    output_dir = os.path.join(CWD, "csvfiles")
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    with open('{file_path}.csv'.format(file_path=os.path.join(output_dir, file_name)), 'w') as csv_file:
        writer = csv.writer(csv_file)
        for row in record_data:
            writer.writerow(row)

def save_plot(file_name, fig, ax, n_iter):
    output_dir = os.path.join(CWD, "imgfiles")
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    ax.set_ylim(-.03, 1) 
    ax.set_xlim(-1, n_iter)
    ax.set_yticks(np.arange(0, 1.01, .1))
    ax.set_xticks(np.arange(0, n_iter+1, int(n_iter/5)))
    ax.yaxis.set_major_formatter(lambda x, pos: f'{x:.3f}'.strip('0').rstrip('.') if x != 0 else 0)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())

    fig.set_facecolor('white')
    plt.savefig(output_dir+'/'+file_name+'.png') 

def plot_result(record_data, file_name, alpha=.1):
    types = list(np.unique(np.array(record_data)[:, 0]))
    fig, ax = plt.subplots(1, 1, figsize=(11, 7))
    for row in record_data:
        row_type, row_data = row[0], row[1:]
        ax.plot(row_data, label=row_type, color=COLORS[types.index(row_type)], alpha=alpha)
    
    save_plot(file_name, fig, ax, len(record_data[0]))

def plot_result_mean(record_data, file_name, alpha=.85):
    record_data = np.array(record_data)
    types = list(np.unique(record_data[:, 0]))
    fig, ax = plt.subplots(1, 1, figsize=(11, 7))
    for t in types:
        t_data = record_data[record_data[:,0]==t, 1:].astype(float)
        y = np.mean(t_data, axis=0)
        ci = 0.05 * np.std(y) / np.mean(y)
        ax.plot(y, label=t, color=COLORS[types.index(t)], alpha=alpha)
        plt.fill_between(np.arange(0, len(y)), (y-ci), (y+ci), color=COLORS[types.index(t)], alpha=0.05)

    save_plot(file_name+'_mean', fig, ax, len(record_data[0]))


if __name__ == "__main__":
    np.random.seed(RAMOM_SEED)
    parser = ArgsModel()

    exp = "Default_"

    ############## Multiple trails ##############
    ## Figure 1
    args_dict = parser.get_fig_args(1)
    record_data = list()
    for n_trail in range(N_RANDOM_TRAILS):
        for args_ctr, (exp_legend, exp_args) in enumerate(args_dict.items()):
            # print("| trail {}/{} |".format(n_trail+1, N_RANDOM_TRAILS))
            game = PublicGoodsGame(exp_args, verbose=False)
            game.simulate()
            record_data.append([exp_args.net_group] + list(game.get_pi_list()))
    file_name = exp + "Fig1_ntrails_{}".format(N_RANDOM_TRAILS)
    save_to_csv(record_data, file_name)
    plot_result(record_data, file_name)
    plot_result_mean(record_data, file_name)
    print(exp+'FIG1 done!')

    ## Figure 2
    args_dict = parser.get_fig_args(2)
    record_data = list()
    for n_trail in range(N_RANDOM_TRAILS):
        for args_ctr, (exp_legend, exp_args) in enumerate(args_dict.items()):
            # print("| trail {}/{} |".format(n_trail+1, N_RANDOM_TRAILS))
            game = PublicGoodsGame(exp_args, verbose=False)
            game.simulate()
            record_data.append([exp_args.net_group] + list(game.get_pi_list()))
    file_name = exp + "Fig2_ntrails_{}".format(N_RANDOM_TRAILS)
    save_to_csv(record_data, file_name)
    plot_result(record_data, file_name)
    plot_result_mean(record_data, file_name)
    print(exp+'FIG2 done!')

    ## Figure 5
    # args_dict = parser.get_fig_args(5)
    # record_data = list()
    # for n_trail in range(N_RANDOM_TRAILS):
    #     for args_ctr, (exp_legend, exp_args) in enumerate(args_dict.items()):
    #         # print("| trail {}/{} |".format(n_trail+1, N_RANDOM_TRAILS))
    #         game = PublicGoodsGame(exp_args, verbose=False)
    #         game.simulate()
    #         record_data.append([exp_args.corr_RI] + list(game.get_pi_list()))
    # file_name = exp + "Fig5_ntrails_{}".format(N_RANDOM_TRAILS)
    # save_to_csv(record_data, file_name)
    # plot_result(record_data, file_name)
    # plot_result_mean(record_data, file_name)
    # print(exp+'FIG5 done!')

    ############### Single trail ###############
    ## Figure 1
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

    ## Figure 2
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

    # Some notes:
    # 最後的指標到底是 人數比率 還是 contribution 的比率？
    # formula 3 裡的 pi 是 "rate of contribution." 到底是「參加的比例」還是「所有資源中被貢獻出來的比率」
    # participation rate 是當下還是現在？ （Try this!）
    # E 的分佈：normal, [0, 1]
    # 對於 R 的理解？ 我現在理解應該是「加總等於 1 的 normal distribution」? N 是 total resource 還是 人數？
    # Smax ???
    # 均衡狀態的條件 ???
   
    # (x)
    # 確認 strong, weak network type
    # 確認 RI correlation 的設定

    # (V)
    # 確認各 Fig 的 threshold 初始化 -> Fig1, 2, 5 一開始都是1
    # 把資料儲存起來，再畫成圖
    # C=[0,1] 的地方都寫錯，應該是 V=[0,1]。這是因為受到舊版的影響?
    # rnd seed = 123