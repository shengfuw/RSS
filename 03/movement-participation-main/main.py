import argparse
import csv
import itertools
import os
import math
import random
import matplotlib.pyplot as plt
import multiprocessing
import numpy as np
import networkx as nx
from scipy.stats import truncnorm
from scipy.stats import pearsonr
from sympy import is_convex

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
        self.R = None # R_i (ego i's own resources)
        self.I = None # I_ti (ego i's level of interest in collective goods at t iteration)
        self.P = None # P_i (ego i's power/centrality)

        # sum param
        self.sum_R = None
        self.sum_P = None

        # the degree of influence ego i exert over j
        # a list of len(agents)
        self.P_ij = None 

        # initalized as all defectors
        self.is_volunteer = 0 # V_ti (ego i's decision to participate at t iteration)

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
    
    def add_net_member(self, neighbors, neighbors_p_sum):
        self.net = neighbors 
        self.neighbors_p_sum = neighbors_p_sum

    @staticmethod
    def _draw(p):
        return True if np.random.uniform() < p else False
    
    def _get_p_ij(self, ag_j) -> float:
        p_i = self.P
        p_j = ag_j.P
        p_k_sum = ag_j.neighbors_p_sum - p_i
        return math.sqrt(p_i/(p_i+p_j+EPSILON) * p_i/(p_k_sum+EPSILON)) # formula (6)
    
    def _get_net_pi(self):
        if self.net is not None:
            pi_is_not_volun = sum([ag.R*ag.is_volunteer for ag in self.net]) / self.sum_R # formula (5)
        else:
            pi_is_not_volun = 0.0

        if self.net is not None:
            pi_is_volun = (pi_is_not_volun + self.R + sum([self._get_p_ij(ag)*ag.R for ag in self.net if not ag.is_volunteer])) / self.sum_R # formula (7)
        else:
            pi_is_volun = (pi_is_not_volun + self.R) / self.sum_R

        return (pi_is_not_volun, pi_is_volun)
    
    @staticmethod
    def _get_production_level(pi):
        return 1 / (1 + math.exp(10*(.5-pi))) # formula (1)

    def to_volunteer(self) -> None: 
        # formula (8)
        pi_is_not_vol, pi_is_vol = self._get_net_pi()
        expect_is_not_vol = self._get_production_level(pi_is_not_vol)*self.sum_R*self.I
        expect_is_vol = self._get_production_level(pi_is_vol)*self.sum_R*self.I - self.R 
        expect_marginal = (expect_is_vol - expect_is_not_vol) / self.R
        # print(pi_is_vol, expect_is_vol)
        # print(pi_is_not_vol, expect_is_not_vol)
        p = 0
        try:
            p = 1 / (1 + math.exp(10*(1.0-expect_marginal))) # formula (8)
        except:
            if 1.0-expect_marginal > 0:
                p = 0.0
            else:
                p = 1.0
        # print(p)
        # print("===============")
        self.is_volunteer = self._draw(p)
        # if not self.is_volunteer:
        #     print(pi_is_vol, expect_is_vol)
        #     print(pi_is_not_vol, expect_is_not_vol)
        #     print(p)
        #     print("===============")
    
    def to_influence(self) -> None:
        if self.net is None:
            return
         
        if self.is_volunteer: # choose to participate 
            # upward influence "form j"
            others_list = [ag for ag in self.net if not ag.is_volunteer and self.I > ag.I] 
            others_list = sorted(others_list, key=lambda ag: ag.R*self._get_p_ij(ag), reverse=True)
            resourse_left = self.R
            for ag in others_list:
                ag.I_delta += (self.I - ag.I)*self._get_p_ij(ag) # formula (10)
                resourse_left -= (1 / (self.net_n*self.net_density)) * (self.P/(ag.P+EPSILON))
                if resourse_left <= 0:
                    break
            # mutual reinforcement "from j"
            for ag in self.net:
                if ag.is_volunteer:
                    ag.I_delta += (math.sqrt(self.I**2 + ag.I**2) - ag.I) * self._get_p_ij(ag) # formula (12)
        else: # chooses to defect 
            # downward influence "from j"
            for ag in self.net:
                if ag.is_volunteer and self.I < ag.I:
                    ag.I_delta += (self.I - ag.I)*self._get_p_ij(ag)

class PublicGoodsGame(object):
    def __init__(self, args: argparse.ArgumentParser, verbose=True) -> None:
        super().__init__()

        Agent._ids = itertools.count(0)
        self.verbose = verbose

        self.args = args
        if self.verbose:
            print("Args: {}".format(args))

        self.ags = self.init_ags()
        
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

    def bulid_network(self, N, density, k = 20, across_ratio=.3):
        edge_n = int(density * N * (N-1) / 2) # undirected 
        within_edge_n = int(edge_n * across_ratio)
        between_edge_n = edge_n - within_edge_n
        
        within_group, between_group = [], []
        for i in range(N):
            for j in range(N):
                if j > i:
                    i_group_index, j_group_index = int(i/k), int(j/k)
                    if i_group_index == j_group_index:
                        within_group.append((i, j))
                    else:
                        between_group.append((i, j))
        
        edges = random.sample(within_group, k=within_edge_n) + random.sample(between_group, k=between_edge_n)
        G = nx.Graph()
        G.add_nodes_from(range(0, N))
        G.add_edges_from(edges)
        return G

    def init_ags(self) -> list:
        # built network 
        self.G = self.bulid_network(self.args.N, self.args.net_density)
        
        # P
        ## calculate the eigenvalues and choose the eigenvectors of the largest eigenvalue for P = [P_1, P_2, ..., P_N]
        ### method 1
        P = list(nx.eigenvector_centrality(self.G).values())
        # w, v = np.linalg.eig(relation_matrix)
        # P = np.abs(v[:, np.argmax(w)])
        ### method 2
        # P = get_chi_square(size=self.args.N, df=self.args.P_df, mean=1)

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
        
        # add neighbors to agents
        for i in range(self.args.N):
            neighbors = [ags[n] for n in list(self.G.neighbors(i))]
            neighbors_p_sum = sum([ag_j.P for ag_j in neighbors])
            ags[i].add_net_member(neighbors, neighbors_p_sum)
        
        if self.verbose:
            self.check_distribution(ags, self.args)
        
        return ags


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
        ax.set_ylim([-1, 101])

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
    avg_I_hd = PlotLinesHandler(xlabel="Iteration", ylabel="avgI",
                                  ylabel_show="Average level of Interest")
    contrib_hd = PlotLinesHandler(xlabel="Iteration", ylabel="contrib",
                                ylabel_show="Total Contribution")
    for exp_legend, exp_args in args_dict.items():
        np.random.seed(seed=exp_args.seed)
        game = PublicGoodsGame(exp_args)
        game.simulate()

        avg_I_hd.plot_line(game.get_avg_I_list(), exp_legend)
        contrib_hd.plot_line(game.get_contribution_list(), exp_legend)
        param = ""
    avg_I_hd.save_fig(param)
    contrib_hd.save_fig(param)