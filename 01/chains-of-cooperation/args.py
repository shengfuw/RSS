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
        self.parser = self.add_decision_algo_param(self.parser)
        self.parser = self.add_production_algo_param(self.parser)
        self.parser = self.add_learning_algo_param(self.parser)
        self.parser = self.add_exp_param(self.parser)

    @staticmethod
    def add_decision_algo_param(parser: argparse.ArgumentParser):
        parser.add_argument("--M", type=float, default=5.0,
            help="slope parameter.")
        parser.add_argument("--thres_type", type=str, default="normal",
            help="type of distribution for agents' thresholds. \
                \"all_defector\" for all set to 1. \
                \"uniform\" for uniformly or \"normal\" for normally distributed.")
        parser.add_argument("--net_group", type=str, default="serial",
            help="the size of reference group. parallel, strong, weak, or serial.")
        parser.add_argument("--R_type", type=str, default="normal",
            help="type of distribution for resources. equal, normal, or lognormal.")
        parser.add_argument("--div", type=str2bool, nargs="?", const=True, default=False,
            help="divisible contribution for agents if set.")
        return parser
        
    @staticmethod
    def add_production_algo_param(parser: argparse.ArgumentParser):
        parser.add_argument("--X", type=float, default=0.,
            help="the const that determined the range of L. X \in \[-1, 1\]. \
                X = -1 for -1 <= L <= 0; \
                X = 1 for 0 <= L <= 1;")
        parser.add_argument("--J", type=float, default=0.5,
            help="jointness of supply. J \in \[0, 1\].")
        
        # distribution of I_j is not disccussed in the paper.
        parser.add_argument("--I_type", type=str, default="normal",
            help="normal distribution for agent's interest in public goods with mean=1.")
        parser.add_argument("--corr_RI", type=str, default="orthogonal",
            help="correlation between the distribution of resource and interests. \
                pos for r_RI = 1; neg for r_RI=1; orthogonal for independent dis.")
        return parser
    
    @staticmethod
    def add_learning_algo_param(parser: argparse.ArgumentParser):
        parser.add_argument("--E_type", type=str, default="normal",
            help="normal distribution for agent's learning rate parameter.")
        return parser

    @staticmethod
    def add_exp_param(parser: argparse.ArgumentParser):
        parser.add_argument("--N", type=int, default=1000,
            help="# of agent.")
        parser.add_argument("--n_iter", type=int, default=200,
            help="# of iterations.")
        parser.add_argument("--figNo", type=int, default=0,
            help="the figure to replicate. 0 for custom parameters.")
        parser.add_argument("--seed", type=int, default=1025,
            help="random seed.")
        return parser

    @staticmethod
    def set_fig_param(args, figNo) -> dict:
        """ set essential parameters for each experiments """
        args.figNo = figNo
        if figNo == 1:
            args.N = 100
            args.thres_type = "uni"
            args.div = False
            args.X = 0.
            args.J = 0.5
            args.n_iter = 200

            args.R_type = "normal"
            args.I_type = "normal"
            args.E_type = "normal"
            args.corr_RI = "orthogonal"

            args1 = copy.deepcopy(args)
            args2 = args
            args1.net_group = "parallel"
            args2.net_group = "serial"
            return {"Parallel Choice": args1, "Serial Choice": args2}
        
        if figNo == 2:
            args.N = 100
            args.thres_type = "normal"
            args.div = False
            args.X = 0.
            args.J = 0.5
            args.n_iter = 200

            args.R_type = "normal"
            args.I_type = "normal"
            args.E_type = "normal"
            args.corr_RI = "orthogonal"

            args1 = copy.deepcopy(args)
            args2 = args
            args1.net_group = "strong"
            args2.net_group = "weak"
            return {"Strong ties": args1, "Weak ties": args2}
        
        if figNo == 5:
            args.N = 100
            args.thres_type = "uniform"
            args.div = False
            args.X = 0.
            args.J = 0.5
            args.n_iter = 200

            args.R_type = "normal"
            args.I_type = "normal"
            args.E_type = "normal"
            args.net_group = "serial"
            
            args1 = copy.deepcopy(args)
            args2 = args
            args1.corr_RI = "pos"
            args2.corr_RI = "neg"
            return {"Positively correlated": args1, "Negatively correlated": args2}


    def get_args(self, custom_legend="custom") -> dict:
        args = self.parser.parse_args()
        if args.figNo == 0:
            return {custom_legend: args}
        else:
            return self.set_fig_param(args, args.figNo)
    
    
    def get_fig_args(self, figNo:int) -> dict:
        args = self.parser.parse_args()
        return self.set_fig_param(args, figNo)