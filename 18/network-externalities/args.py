import argparse


class ArgsModel(object):
    
    def __init__(self) -> None:
        super().__init__()
    
        self.parser = argparse.ArgumentParser()
        self.parser = self.add_agent_param(self.parser)
        self.parser = self.add_internet_param(self.parser)
        self.parser = self.add_network_param(self.parser)
        self.parser = self.add_exp_param(self.parser)
    

    @staticmethod
    def add_agent_param(parser):
        parser.add_argument("--k", type=float, default=0.1,
            help="multiplicative constants for the pure income effect")
        parser.add_argument("--delta", type=float, default=0.1,
            help="multiplicative constants for network effect")
        parser.add_argument("--gamma", type=float, default=0.5,
            help="exponents of income")
        parser.add_argument("--alpha", type=float, default=0.5,
            help="exponents of the proportion of adopters")
        return parser
    

    @staticmethod
    def add_internet_param(parser):
        parser.add_argument("--p_0", type=float, default=60.0,
            help="the initial Internet price")
        parser.add_argument("--p_min", type=float, default=28.74,
            help="the equilibrium price level")
        parser.add_argument("--a", type=float, default=3.34,
            help="the speed of reversion to that equilibrium price")
        return parser
    

    @staticmethod
    def add_network_param(parser):
        parser.add_argument("--w_race", type=float, default=0.83,
            help="the weight of race")
        parser.add_argument("--w_edu", type=float, default=0.53,
            help="the weight of education")
        parser.add_argument("--w_inc", type=float, default=0.53,
            help="the weight of income")
        parser.add_argument("--h", type=float, default=0.,
            help="homophily bias")
        parser.add_argument("--is_spec_net", type=bool, default=True,
            help="is identity-specific net")
        parser.add_argument("--scaler", type=int, default=3,
            help="""the scaler to times the target number of relations for the agent i
                    as the size of the agent i"s in-group.""")
        return parser
    

    @staticmethod
    def add_exp_param(parser):
        parser.add_argument("--n_period", type=int, default=100,
            help="the # of the period to simulate.")
        parser.add_argument("--n_trails", type=int, default=2,
            help="the # of the simulation for each condition.")
        parser.add_argument("--rnd_seed", type=int, default=1025,
            help="random seed.")
        parser.add_argument("--expNo", type=int, default=1,
            help="the number of the experiments to model one of the 7 conditions.")
        parser.add_argument("--run_all", type=bool, nargs="?", const=True, default=False, 
            help="use \"--run_all\" to run all experiments and plot results.")
        parser.add_argument("--vis", type=bool, nargs="?", const=True, default=False, 
            help="use \"--vis\" to visualize each period in the experiments expNo.")
        return parser
    

    @staticmethod
    def set_exp_param(args, expNo):
        """ set essential parameters for each experiments """
        args.expNo = expNo
        if expNo == 1:
            args.delta = 0.
            args.is_spec_net = False
        elif expNo == 2:
            args.delta = 0.1
            args.is_spec_net = False
        elif expNo == 3:
            args.delta = 0.1
            args.is_spec_net = True
            args.h = 0.0
        elif expNo == 4:
            args.delta = 0.1
            args.is_spec_net = True
            args.h = 0.25
        elif expNo == 5:
            args.delta = 0.1
            args.is_spec_net = True
            args.h = 0.5
        elif expNo == 6:
            args.delta = 0.1
            args.is_spec_net = True
            args.h = 0.75
        elif expNo == 7:
            args.delta = 0.1
            args.is_spec_net = True
            args.h = 1.0
        return args


    def get_args(self):
        args = self.parser.parse_args()
        return self.set_exp_param(args, args.expNo)
    
    
    def get_args_by_expNo(self, expNo):
        args = self.parser.parse_args()
        return self.set_exp_param(args, expNo)