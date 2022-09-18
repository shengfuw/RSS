import datetime
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from sklearn.linear_model import LogisticRegression

from args import ArgsModel
from data import AgentDataHolder
from plot_3Dmap import Plot3DArray


CWD = os.path.dirname(os.path.abspath(__file__))
class Agent(object):

    def __init__(self, net_size, id, agent_data, agent_data_norm) -> None:
        super().__init__()

        # reservation price
        self.reser_price = None
        # pure network effect
        self.net_effect = None
        # have adopted the internet
        self.have_bought = False
        # percentage of adopters
        self.net_perc = 0 
        # the list to all agents tied with
        self.spec_net_list = list()

        # agent data
        self.net_size = int(net_size)
        self.id = int(id)
        self.agent_data = agent_data
        self.agent_data_norm = agent_data_norm
        ################# a normally distributed radnom perturbation with a mean of 0 in the first period #################
        # self.inc = self.agent_data[2] 
        self.inc = max(1, int(self.agent_data[2] + np.random.normal(scale=5000)))
        ####################################################################################################################

    def update_reser_price(self, args):
        self.reser_price = (args.k * (self.inc**args.gamma)
            + (self.inc**args.gamma)*args.delta*(self.net_perc**args.alpha))
        self.net_effect = (self.inc**args.gamma)*args.delta*(self.net_perc**args.alpha)
    

    def update_spec_net_perc(self):
        if not self.spec_net_list:
            self.net_perc = 0
        else:
            list_of_bought = [agent for agent in self.spec_net_list if agent.have_bought]
            self.net_perc = len(list_of_bought) / len(self.spec_net_list)
    

    def update_general_net_perc(self, new_net_perc):
        self.net_perc = new_net_perc
    

    def want_adopt_internet(self, market_price):
        if self.reser_price is None:
            raise ValueError("The reservation price is not initialized.")
        return (market_price <= self.reser_price)
    

    def get_social_status(self):
        return self.agent_data_norm
    

    def get_id(self):
        return self.id
    

    def get_net_size(self):
        return self.net_size
    

    def tie_with(self, agent):
        """ agent -> Agent: should be an pointer to an Agent object. """
        self.spec_net_list.append(agent)


class InternetModel(object):
    dis_matrix = None

    class Logger(object):
        """
        Logger for recording group-wise data.
        1. group1 adoption rate
        2. group2 adoption rate
        3. odds ratios of group1 to group2
        """

        def __init__(self, ids_dict, keys) -> None:
            """
            Param:
            - ids_dict -> dict:
                {group1_name: [id1, id2, id3, ... (ids of agent in group1)],
                 group2_name: [id1, id2, id3, ... (ids of agent in group2)]}
            - keys -> list of str:
                [group1_name, group2_name]
            """
            super().__init__()
            self.ids_dict = ids_dict
            self.keys = keys

            self.key1_n = 0
            self.key2_n = 0
            self.key1_perc = list()
            self.key2_perc = list()
            self.key1_key2_odd_ratio = list()
        

        def log_id(self, ag_id):
            if ag_id in self.ids_dict[self.keys[0]]:
                self.key1_n += 1
            if ag_id in self.ids_dict[self.keys[1]]:
                self.key2_n += 1


        def log_into_list(self):
            self.key1_perc.append(self.key1_n/len(self.ids_dict[self.keys[0]]))
            self.key2_perc.append(self.key2_n/len(self.ids_dict[self.keys[1]]))
            self.key1_key2_odd_ratio.append(self.cal_odd_ratio(self.key1_perc[-1], self.key2_perc[-1]))
        
        
        @staticmethod
        def cal_odd_ratio(p1, p2):
            return (p1/(1-p1))/(p2/(1-p2)) if p2 != 0 and p2 != 1 and p1 != 1 else 0


        def get_latest_logged(self):
            """ Get the string descripting the 3 types of data. """
            return "{}: {:.2f}%; {}:{:.2f}%; odd_r: {:.2f}".format(self.keys[0], self.key1_perc[-1],
                self.keys[1], self.key2_perc[-1], self.key1_key2_odd_ratio[-1])
        

        def get_odd_ratio(self):
            """ Get the list of logged odds ratios. """
            return self.key1_key2_odd_ratio
                

    def __init__(self, args, data_holder: AgentDataHolder, random_seed,
        plotter3d=None, verbose=True) -> None:
        """
        Param:
        - data_holder -> AgentDataHolder:
            the holder handling agents" information.
        - plotter3d -> Plot3DArray:
            pass a Plot3DArray object for plotting location of agents in 3d space
            and ties between agents.
        - verbose -> bool:
            print data of each period.
        """
        super().__init__()
        np.random.seed(random_seed)
        self.args = args
        self.data_holder = data_holder
        self.plotter = plotter3d
        self.verbose = verbose
        
        self.dis_w = np.array([args.w_race, args.w_edu, args.w_inc])
        # the # of adopters in the whole network
        self.adopters_n = 0
        # the logged percentage of adopters of each period
        self.adopters_perc = list()
        self.internet_price = args.p_0
        self.period = 0

        # list of Agent object
        self.agents = None
        self.race_logger = self.Logger(data_holder.get_agent_race_group_ids(),
                                       keys=["white", "black"])
        self.edu_logger = self.Logger(data_holder.get_agent_edu_group_ids(),
                                      keys=["college", "high school"])
        self.inc_logger = self.Logger(data_holder.get_agent_inc_group_ids(),
                                      keys=["high", "low"])
        self.logit_coef = None
        
        if self.verbose:
            print("Args: {}".format(self.args))
        self._preparation_phrase()
    

    def _preparation_phrase(self):
        # 1. Build N Agents
        self.agents, self.agent_n = self._build_agents()

        # 2. Build a network if the identity-specific network is enabled
        if self.args.is_spec_net:
            agent_dis_matrix = self.build_agent_dis_matrix()
            # find ego_net
            if self.verbose:
                print("building ego net for each agent ...")
            for agent_idx, agent in enumerate(self.agents):
                ingroup_n = int(agent.get_net_size()*self.args.scaler)
                sorted_idx = np.argsort(agent_dis_matrix[agent_idx, :])
                ingroup_agent_idx = sorted_idx[:ingroup_n]
                outgroup_agent_idx = sorted_idx[ingroup_n:]
                # prob_to_ingroup = self.args.h + (1-self.args.h)*np.random.uniform()
                prob_to_ingroup = self.args.h
                for _ in range(agent.get_net_size()):
                    prob = np.random.uniform()
                    # tie with out-group
                    # random tie
                    if prob > prob_to_ingroup:
                        # chosen_ag = np.random.choice(outgroup_agent_idx)
                        # outgroup_agent_idx = outgroup_agent_idx[outgroup_agent_idx!=chosen_ag]
                        chosen_ag = np.random.choice(sorted_idx)
                    # tie with in-group
                    elif prob <= prob_to_ingroup:
                        chosen_ag = np.random.choice(ingroup_agent_idx)
                        ingroup_agent_idx = ingroup_agent_idx[ingroup_agent_idx!=chosen_ag] # 不能重複建 tie

                    sorted_idx = sorted_idx[sorted_idx!=chosen_ag] # 不能重複建 tie
                    agent.tie_with(self.agents[chosen_ag])
        
        # 3. Initialize Agents’ reservation price
        for agent in self.agents:
            agent.update_reser_price(self.args)
        
        if self.verbose:
            print("Model finished initialization and preparation.")


    def _build_agents(self):
        agents = list()
        self.agents_data = self.data_holder.get_agent_info()
        for agent_data in self.agents_data:
            agent = Agent(id=agent_data[0],
                          net_size=agent_data[1],
                          agent_data=agent_data[5:8],
                          agent_data_norm=agent_data[2:5])
            agents.append(agent)
        agent_n = len(agents)
        if self.verbose:
            print("{} agents initialized.".format(agent_n))
        
        # social status (normalized value) of every agents
        self.agents_data_norm = np.copy(self.agents_data[:, 2:5])
        # data (original value), used for logistic regression
        self.agents_data_X = np.copy(self.agents_data[:, 5:8])
        ############# 收入加上了擾亂 ########################
        # self.agents_data_X[:, 2] = np.log(self.agents_data_X[:, 2]) 
        self.agents_data_X[:, 2] = np.log([ag.inc for ag in agents]) 
        ##################################################

        return agents, agent_n


    def cal_agents_dis(self, agent1:Agent, agent2:Agent) -> float:
        dis_vector = agent1.get_social_status() - agent2.get_social_status()
        weighted_dis = np.linalg.norm(np.multiply(dis_vector, self.dis_w))
        return weighted_dis
    

    def build_agent_dis_matrix(self):
        if InternetModel.dis_matrix is None:
            print("building distance matrix ...")
            InternetModel.dis_matrix = np.full((self.agent_n, self.agent_n), np.inf)
            for i in range(self.agent_n-1):
                for j in range(i+1, self.agent_n):
                    dis = self.cal_agents_dis(self.agents[i], self.agents[j])
                    InternetModel.dis_matrix[i][j] = dis
                    InternetModel.dis_matrix[j][i] = dis
            
        return InternetModel.dis_matrix
    

    def update_internet_price(self):
        n = self.adopters_n / self.agent_n
        self.internet_price = (self.internet_price + 
            self.args.a/12 * n * (self.args.p_min-self.internet_price))
    

    def get_agent_net_effect(self):
        """ Return: 1d nd.array, pure network effects of every agents. """
        return np.array([ag.net_effect for ag in self.agents])
    

    def get_all_tie(self):
        """
        Return
        - all_ties -> 3d np.array, size=(# of ties, 2, 3)
            Each tie has its own size of array of size (2, 3), which is 
            the social status (location in 3d space) of two relating agents.
        """
        all_ties = None
        for ag in self.agents:
            for ag_tie in ag.spec_net_list:
                tie = np.concatenate((ag.agent_data_norm.reshape((1, 3)), ag_tie.agent_data_norm.reshape((1, 3))), axis=0).reshape((1, 2, 3))
                all_ties = np.concatenate((all_ties, tie), axis=0) if all_ties is not None else tie
        return all_ties


    def simulate_a_period(self):
        if self.agents is None:
            raise ValueError("Call model.preparation_phrase() first.")
        self.period += 1

        if self.plotter is not None:
            agents_data_X, agents_adp_y = self.get_agent_current_data_norm()
            agents_price = self.get_agent_net_effect()
            agents_tie = self.get_all_tie()
            self.plotter.plot_map(agents_data_X, agents_adp_y, agents_price, agents_tie, self.period)

        # 1. Update the Internet price
        self.update_internet_price()
        
        # # 2. Agents adopt the Internet
        # for ag in self.agents:
        #     if not ag.have_bought and ag.want_adopt_internet(self.internet_price):
        #         ag.have_bought = True
        #         self.adopters_n += 1
        #         self.race_logger.log_id(ag.get_id())
        #         self.edu_logger.log_id(ag.get_id())
        #         self.inc_logger.log_id(ag.get_id())

        # 3. Update agent’s percent of adopters
        # 4. Update agent’s reservation price
        if self.args.is_spec_net:
            for ag in self.agents:
                ag.update_spec_net_perc()
                ag.update_reser_price(self.args)
        else:
            general_perc = self.adopters_n / self.agent_n
            for ag in self.agents:
                ag.update_general_net_perc(general_perc)
                ag.update_reser_price(self.args)

        # 2. Agents adopt the Internet
        for ag in self.agents:
            if not ag.have_bought and ag.want_adopt_internet(self.internet_price):
                ag.have_bought = True
                self.adopters_n += 1
                self.race_logger.log_id(ag.get_id())
                self.edu_logger.log_id(ag.get_id())
                self.inc_logger.log_id(ag.get_id())

        self.adopters_perc.append(self.adopters_n / self.agent_n)
        self.race_logger.log_into_list()
        self.edu_logger.log_into_list()
        self.inc_logger.log_into_list()
        coef = self.logistic_reg()
        self.logit_coef = np.concatenate((self.logit_coef, coef), axis=0) if self.logit_coef is not None else coef

        if self.verbose:
            print("period {} || adopters: {}/{}; internet_price: {}".format(self.period,
                self.adopters_n, self.agent_n, self.internet_price))
            print("\t{} || {} || {}".format(self.race_logger.get_latest_logged(),
                                            self.edu_logger.get_latest_logged(),
                                            self.inc_logger.get_latest_logged()))
    

    def simulate(self):
        if self.verbose:
            print("==== START SIMULATION ====")
        for _ in range(self.args.n_period):
            self.simulate_a_period()
        if self.verbose:
            print("==== END SIMULATION ====")
    

    def get_data_for_plotting(self):
        """
        Return
        - data_concat -> 3d np.array, size=(1, n_period, 7):
            last axis: [percentage of adopters,
                        odds ratios of two group in term of race,
                        odds ratios of two group in term of education,
                        odds ratios of two group in term of income,
                        logit coefficient of race,
                        logit coefficient of education,
                        logit coefficient of (logged) income]
        """
        adp_perc = np.array(self.adopters_perc).reshape((1, -1, 1))
        race_odd = np.array(self.race_logger.get_odd_ratio()).reshape((1, -1, 1))
        edu_odd = np.array(self.edu_logger.get_odd_ratio()).reshape((1, -1, 1))
        inc_odd = np.array(self.inc_logger.get_odd_ratio()).reshape((1, -1, 1))
        logit_coef = self.logit_coef.reshape((1, self.args.n_period, 3))
        data_concat = np.concatenate((adp_perc, race_odd, edu_odd, inc_odd, logit_coef), axis=2)
        return data_concat
    
    
    def get_agent_current_data(self):
        """
        Return:
        - agents_data_X -> 2d np.array, size=(# of agents, 3)
            the social status (original values) of each agents.
            Note that the income is logged based on e.
        - agents_adp_y -> 1d np.array, size=(# of agents, )
            1.0 if agents have adopted, else 0.0.
        """
        agents_adp_y = np.array([(1. if ag.have_bought else 0.) for ag in self.agents])
        return self.agents_data_X, agents_adp_y
    

    def get_agent_current_data_norm(self):
        """
        Return:
        - agents_data_X -> 2d np.array, size=(# of agents, 3)
            the social status (normalized values) of each agents.
        - agents_adp_y -> 1d np.array, size=(# of agents, )
            1.0 if agents have adopted, else 0.0.
        """
        agents_adp_y = np.array([(1. if ag.have_bought else 0.) for ag in self.agents])
        return self.agents_data_norm, agents_adp_y


    def logistic_reg(self):
        """
        Return:
        - coef -> 1d np.array, size=(3, )
            the coefficient of logistic regression of the current period.
        """
        agents_data_X, agents_adp_y = self.get_agent_current_data()
        log_model = LogisticRegression(random_state=args.rnd_seed,
                                       class_weight=None)
        log_model.fit(agents_data_X, agents_adp_y)
        coef = log_model.coef_
        return coef


def visualize_3d(agent_data_holder, expNo, suffix):
    """
    Generate the visualization of the experiment expNo.
    An .gif file, an .mp4 file, and a directory containing images of every period is generated.
    Noted that expNo should be in [3, 4, 5, 6, 7].
    """
    args_exp = parser.get_args_by_expNo(expNo=expNo)
    filename_prefix = "{}_expNo({})".format(suffix, expNo)
    plotter = Plot3DArray(filename_prefix=filename_prefix)

    internet_model = InternetModel(args_exp, agent_data_holder, plotter, verbose=True)
    internet_model.simulate()
    plotter.save_gif()
    plotter.save_mp4()


def run_all_exp(args, agent_data_holder, suffix,
    output_dir=os.path.join(CWD, "csvfiles")):
    """
    Run all experiments 1~7.
    The logged data of each period of every experiment is seperately saved into csv files.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    paths_to_csv = list()
    for exp_idx in range(1, 8):
    # for exp_idx in range(1, 3):
        data_all_trail = None
        args_exp = parser.get_args_by_expNo(expNo=exp_idx)
        print("ExpNo {} | Args: {}".format(exp_idx, args_exp))
        for trail_idx in range(args.n_trails):
            internet_model = InternetModel(args_exp, agent_data_holder, random_seed=args.rnd_seed+trail_idx, verbose=False)
            internet_model.simulate()
            data_a_trail = internet_model.get_data_for_plotting()
            print("expNo {} | trail {}/{} | adoption rate: {}%".format(exp_idx, trail_idx+1, args.n_trails, data_a_trail[0, -1, 0]))
            data_all_trail = np.concatenate((data_all_trail, data_a_trail), axis=0) if data_all_trail is not None else data_a_trail
            # if args_exp.expNo == 1 or args_exp.expNo == 2:
            #     break
        data_trail_avg = np.mean(data_all_trail, axis=0)
        filen = "{}_expNo{}_adpPerc_raceOdd_eduOdd_incOdd.csv".format(suffix, exp_idx)
        np.savetxt(os.path.join(output_dir, filen), data_trail_avg, delimiter=",",
            header="adpPerc,raceOdd,eduOdd,incOdd, raceCoef, eduCoef, incCoef")
        paths_to_csv.append(os.path.join(output_dir, filen))
        # print("data saved to {}".format(os.path.join(output_dir, filen)))
        print("data saved.")
    return paths_to_csv


def read_result(path_to_results):
    data_list = list()
    for path in path_to_results:
        data_list.append(pd.read_csv(path).values)
    adp_perc = np.asarray([exp_data[:,0] for exp_data in data_list])
    race_odd = np.asarray([exp_data[:,1] for exp_data in data_list])
    edu_odd = np.asarray([exp_data[:,2] for exp_data in data_list])
    inc_odd = np.asarray([exp_data[:,3] for exp_data in data_list])
    race_coef = np.asarray([exp_data[:,4] for exp_data in data_list])
    edu_coef = np.asarray([exp_data[:,5] for exp_data in data_list])
    inc_coef = np.asarray([exp_data[:,6] for exp_data in data_list])

    return {"adp_perc":adp_perc,
            "race_odd":race_odd,
            "edu_odd":edu_odd,
            "inc_odd":inc_odd,
            "race_coef":race_coef,
            "edu_coef":edu_coef,
            "inc_coef":inc_coef}


def set_axis(fn):
    ax = plt.gca()
    if fn == "adp_perc":
        ax.set_xlim([0, 100])
        plt.xticks(np.arange(0, 101, step=10))
        ax.set_ylim([0.0, 0.7])
        plt.yticks(np.arange(0, 0.71, step=0.1))
    elif fn == "race_odd":
        ax.set_xlim([0, 100])
        plt.xticks(np.arange(0, 101, step=10))
        ax.set_ylim([1, 7])
        plt.yticks(np.arange(1, 8, step=1))
    elif fn == "edu_odd":
        ax.set_xlim([0, 100])
        plt.xticks(np.arange(0, 101, step=10))
        ax.set_ylim([0, 25])
        plt.yticks(np.arange(0, 26, step=5))
    elif fn == "inc_odd":
        ax.set_xlim([0, 100])
        plt.xticks(np.arange(0, 101, step=10))
        ax.set_ylim([0, 350])
        plt.yticks(np.arange(0, 351, step=50))
    elif fn == "race_coef":
        ax.set_xlim([10, 80])
        plt.xticks(np.arange(10, 81, step=10))
        ax.set_ylim([-0.4, 1.6])
        plt.yticks(np.arange(-0.4, 1.61, step=0.2))
    elif fn == "edu_coef":
        ax.set_xlim([10, 80])
        plt.xticks(np.arange(10, 81, step=10))
        ax.set_ylim([-0.02, 0.1])
        plt.yticks(np.arange(-0.02, 0.11, step=0.02))
    elif fn == "inc_coef":
        ax.set_xlim([10, 80])
        plt.xticks(np.arange(10, 81, step=10))
        ax.set_ylim([1.5, 5.5])
        plt.yticks(np.arange(1.5, 5.6, step=0.5))
    

FIG_LENGTH_WIDTH_RATIO = 16.83/21.25
LINE_STYLE = ("k:",
              "k-",
              "k--",
              "k-.",
              "k|-",
              "k^-",
              "ko--")
def plot_lines(data, fn, title, legend_n, suffix, 
               xlabel="Time", ylabel="Odds Ratio", add_no_NE=False,
               figure_size=7, linewidth=1,
               output_dir=os.path.join(CWD, "imgfiles")):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print("fn {} | data_size: {}".format(fn, data.shape))
    plt.figure(figsize=(figure_size, figure_size*FIG_LENGTH_WIDTH_RATIO), dpi=160)
    plt.title(title)
    set_axis(fn)
    if fn == "adp_perc":
        plt.xlabel(xlabel, fontname="Times New Roman", fontweight="bold")
        plt.ylabel(ylabel, fontname="Times New Roman", fontweight="bold")
    else:
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

    if add_no_NE:
        plt.plot(np.arange(1, data.shape[-1]+1), data[0, :],
            LINE_STYLE[0], linewidth=linewidth+1)
    else:
        legend_n = legend_n[1:]
    for i in range(1, 7):
    # for i in range(1, 2):
        plt.plot(np.arange(1, data.shape[-1]+1), data[i, :],
            LINE_STYLE[i], linewidth=linewidth, markersize=2)
    plt.legend(legend_n)
    plt.savefig(os.path.join(output_dir, "{}_{}.png".format(suffix, fn)))
    # print("fig save to {}".format(os.path.join(output_dir, "{}_{}".format(suffix, fn))))
    print("fig saved.")



def plot_result(data_dict, legend_n, suffix):
    plot_lines(data_dict["adp_perc"], "adp_perc", "Proportion of Adopters", 
        legend_n, suffix, ylabel="Proportion of Adopters$", add_no_NE=True)
    plot_lines(data_dict["race_odd"], "race_odd", "Odds Ratios of Race (White-Black)",
        legend_n, suffix)
    plot_lines(data_dict["edu_odd"], "edu_odd", "Odds Ratios of Education (College-High School)",
        legend_n, suffix)
    plot_lines(data_dict["inc_odd"], "inc_odd", "Odds Ratios of Income (Highest-Lowest)",
        legend_n, suffix)
    plot_lines(data_dict["race_coef"], "race_coef", "Estimated Coefficient of Race", 
        legend_n, suffix, ylabel="Logit coefficient")
    plot_lines(data_dict["edu_coef"], "edu_coef", "Estimated Coefficient of Education", 
        legend_n, suffix, ylabel="Logit coefficient")
    plot_lines(data_dict["inc_coef"], "inc_coef", "Estimated Coefficient of (Logged) Income", 
        legend_n, suffix, ylabel="Logit coefficient")



if __name__ ==  "__main__":
    # just plotting
    # files = [os.path.join(CWD, "csvfiles", "04_23_22_00_ntrails_3_rndSeed_1025_expNo{}_adpPerc_raceOdd_eduOdd_incOdd.csv".format(i)) for i in range(1, 8)]
    # legend_n = ["No NE", "Gen NE", "Spe NE (h=0)", "Spe NE (h=0.25)", "Spe NE (h=0.5)", "Spe NE (h=0.75)", "Spe NE (h=1.0)"]
    # data_dict = read_result(files)
    # parser = ArgsModel()
    # args = parser.get_args()
    # suffix = "{}_ntrails_{}_rndSeed_{}".format(datetime.datetime.now().strftime("%m_%d_%H_%M"), args.n_trails, args.rnd_seed)
    # plot_result(data_dict, legend_n, suffix)
    # exit()

    parser = ArgsModel()
    args = parser.get_args()

    path_to_agentInfo = os.path.join(CWD, "agent_info_file.csv")
    agent_data_holder = AgentDataHolder(path_to_agentInfo)

    if args.vis:
        visualize_3d(agent_data_holder, expNo=args.expNo, suffix=datetime.datetime.now().strftime("%m_%d_%H_%M"))

    if args.run_all:
        suffix = "{}_ntrails_{}_rndSeed_{}".format(datetime.datetime.now().strftime("%m_%d_%H_%M"), args.n_trails, args.rnd_seed)
        path_to_results = run_all_exp(args, agent_data_holder, suffix)

        legend_n = ["No NE", "Gen NE", "Spe NE (h=0)", "Spe NE (h=0.25)", "Spe NE (h=0.5)", "Spe NE (h=0.75)", "Spe NE (h=1.0)"]
        data_dict = read_result(path_to_results)
        plot_result(data_dict, legend_n, suffix)