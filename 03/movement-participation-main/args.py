import argparse
import copy

def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")


class ArgsModel(object):
    
    def __init__(self) -> None:
        super().__init__()
    
        self.parser = argparse.ArgumentParser()
        # self.parser = self.add_production_algo_param(self.parser)
        # self.parser = self.add_decision_making_algo_param(self.parser)
        # self.parser = self.add_interpersonal_influence_param(self.parser)
        self.parser = self.add_distribution_param(self.parser)
        self.parser = self.add_exp_param(self.parser)
        
    @staticmethod
    def add_production_algo_param(parser: argparse.ArgumentParser):
        return parser
    
    @staticmethod
    def add_decision_making_algo_param(parser: argparse.ArgumentParser):
        return parser
    
    @staticmethod
    def add_interpersonal_influence_param(parser: argparse.ArgumentParser):
        return parser
    
    @staticmethod
    def add_distribution_param(parser: argparse.ArgumentParser):
        parser.add_argument("--R_df", type=int, default=20,
            help="the degree of freedom of R's chi-square distribution. 3, 7, or 20.")
        parser.add_argument("--I_df", type=int, default=3,
            help="the degree of freedom of I's chi-square distribution. 3, 7, or 20.")
        parser.add_argument("--P_df", type=int, default=3,
            help="the degree of freedom of P's chi-square distribution. 3, 7, or 20.")
        parser.add_argument("--r_RP", type=int, default=1,
            help="the correlation between R and P. Support only 1 for positively or -1 for negatively.")
        parser.add_argument("--r_IP", type=int, default=1,
            help="the correlation between I and P. Support only 1 for positively or -1 for negatively.")
        return parser

    @staticmethod
    def add_exp_param(parser: argparse.ArgumentParser):
        parser.add_argument("--N", type=int, default=100,
            help="# of agent.")
        parser.add_argument("--n_iter", type=int, default=200,
            help="# of iterations.")
        parser.add_argument("--net_density", type=float, default=0.1,
            help="the density of the network. [0., 1.]")
        parser.add_argument("--net_df", type=int, default=3,
            help="the degree of freedom of the chi-square distribution for # of edges. 3, 7, or 20.")
        parser.add_argument("--figNo", type=int, default=1,
            help="the figure to replicate. 0 for custom parameters.")
        parser.add_argument("--seed", type=int, default=123,
            help="random seed.")
        return parser

    @staticmethod
    def set_fig_param(args, figNo) -> dict:
        """ set essential parameters for each experiments """
        args.figNo = figNo
        if figNo == 1:
            args.N = 100
            args.n_iter = 160
            args.net_density = 0.1
            args.net_df = 20 # not assigned in the paper

            args.R_df = 20
            args.I_df = 3
            args.P_df = 3

            # Four Regimes
            rtn_dict = dict()
            # args_privileged = copy.deepcopy(args)
            # args_privileged.r_RP = 1
            # args_privileged.r_IP = 1
            # rtn_dict["Privileged"] = args_privileged

            args_rebellious = copy.deepcopy(args)
            args_rebellious.r_RP = -1
            args_rebellious.r_IP = 1
            rtn_dict["Rebellious"] = args_rebellious

            # args_impoverished = copy.deepcopy(args)
            # args_impoverished.r_RP = 1
            # args_impoverished.r_IP = -1
            # rtn_dict["Impoverished"] = args_impoverished
            
            # args_estranged  = copy.deepcopy(args)
            # args_estranged.r_RP = -1
            # args_estranged.r_IP = -1
            # rtn_dict["Estranged"] = args_estranged

            return rtn_dict
    

    def get_args(self, custom_legend="custom") -> dict:
        args = self.parser.parse_args()
        if args.figNo == 0:
            return {custom_legend: args}
        else:
            return self.set_fig_param(args, args.figNo)
    
    
    def get_fig_args(self, figNo:int) -> dict:
        args = self.parser.parse_args()
        return self.set_fig_param(args, figNo)