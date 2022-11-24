import argparse

class ArgsConfig:
    
    def __init__(self) -> None:
    
        parser = argparse.ArgumentParser()

        # firm
        parser.add_argument("--n_firm", type=int, default=100,
            help="the # of firms.")
        parser.add_argument("--alpha", type=float, default=0.33,
            help="the weight of innovation merit when evaluating outcomes.")
        parser.add_argument("--beta", type=float, default=0.33,
            help="the weight of consultant quality when evaluating outcomes.")
        parser.add_argument("--gamma_f", type=float, default=0.5,
            help="the weight of historical past on aspirations.")
        parser.add_argument("--xi_f", type=float, default=0.8,
            help="the speed with which historical aspirations are updated.")
        parser.add_argument("--a_f", type=float, default=2.0,
            help="a parameter in the logistic function of abandonment.")
        parser.add_argument("--b_f", type=float, default=10.0,
            help="a parameter in the logistic function of abandonment.")
        parser.add_argument("--p_mimic_f", type=float, default=0.8,
            help="the probability of mimicing the most successful peers when making a change.")

        # consultant
        parser.add_argument("--n_consultant", type=int, default=100,
            help="the # of consultants.")
        parser.add_argument("--eta", type=float, default=1.0,
            help="a constant that tunes the level of consulting returns.")
        parser.add_argument("--gamma_c", type=float, default=0.5,
            help="the weight of historical past on aspirations.")
        parser.add_argument("--xi_c", type=float, default=0.8,
            help="the speed with which historical aspirations are updated.")
        parser.add_argument("--a_c", type=float, default=2.0,
            help="a parameter in the logistic function of abandonment.")
        parser.add_argument("--b_c", type=float, default=10.0,
            help="a parameter in the logistic function of abandonment.")
        parser.add_argument("--p_mimic_c", type=float, default=0.8,
            help="the probability of mimicing the most successful peers when making a change.")
        parser.add_argument("--c", type=float, default=0.025,
            help="a constant used when a firm is selecting among the consultants that offer the demanded innovation.")
        parser.add_argument("--window", type=int, default=3,
            help="# of periods considered when a firm is selecting among the consultants that offer the demanded innovation.")

        # models variables
        parser.add_argument("--n_innovation", type=int, default=100,
            help="the # of innovations, numbered from {0, 1, 2, ..., n_innovation-1}.")
        parser.add_argument("--n_periods", type=int, default=300,
            help="the # of periods.")
        parser.add_argument("--n_trails", type=int, default=10,
            help="the # of trials for each config.")
        parser.add_argument("--rnd_seed", type=int, default=123,
            help="random seed.")

        self.parser = parser
    

    def get_args(self):
        args = self.parser.parse_args()
        return args
