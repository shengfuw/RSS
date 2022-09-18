import csv
import numpy as np

def corr(x, y):
    return np.corrcoef(x, y)[0][1]


class AgentDataHolder(object):

    def __init__(self, path_to_agentInfo, verbose=True) -> None:
        super().__init__()
        self.verbose = verbose

        self.agents_data = self._pre_processing(path_to_agentInfo, self.verbose)
        self.race, self.edu, self.inc = self._getID_group_by_race(path_to_agentInfo)
    

    @staticmethod
    def _pre_processing(path_to_info, verbose):
        """
        Return
        - agent_row -> 2d np.array, size=(# of agents, 6):
            [np.array([id, network_size, race_norm, education_norm, income_norm, race, education, income]),
             np.array([id, network_size, race_norm, education_norm, income_norm, race, education, income]),
             ....]
        """
        info_f = open(path_to_info, newline="")
        agent_rows = csv.reader(info_f)
        agents_data = None
        for row_idx, agent_row in enumerate(agent_rows):
            if row_idx == 0:
                col_names = agent_row
                continue
            agent_dict = {col_n:col_val for col_n, col_val in zip(col_names, agent_row)}
            data = list()
            
            # id
            data.append(int(agent_dict["Respondent id number"]))
            
            # network_size
            net_str = agent_dict["How many friends close to discuss problems"]
            if net_str == "96 or higher":
                net_str = 96
            data.append(int(net_str))
            
            # race
            if agent_dict["Race of respondent"] == "White":
                race = 1
            elif agent_dict["Race of respondent"] == "Black":
                race = 0
            data.append(float(race))
            
            # education
            data.append(float(agent_dict["Highest year of school completed"]))

            # income
            inc_str = agent_dict["Total family income"]
            if inc_str == "Under 1000":
                inc_lower_bound, inc_upper_bound = 1, 999
            elif inc_str == "110000 or over":
                ############# 上界矛盾的問題？？？ #####################
                # inc_lower_bound, inc_upper_bound = 110000, 650000
                inc_lower_bound, inc_upper_bound = 110000, 388000
                ####################################################
            else:
                inc_lower_bound, inc_upper_bound = inc_str.split("to")
                inc_lower_bound, inc_upper_bound = int(inc_lower_bound), int(inc_upper_bound)
            inc = np.random.randint(inc_lower_bound, inc_upper_bound+1) # the upper bound shold plus one
            data.append(float(inc))

            # data
            data = np.array([data])
            agents_data = np.concatenate((agents_data, data), axis=0) if agents_data is not None else data
        
        # cal correlation
        # race v.s. log income
        if verbose:
            print("race v.s. edu: {}".format(corr(agents_data[:, 2], agents_data[:, 3])))
            print("race v.s. log income: {}".format(corr(agents_data[:, 2], np.log(agents_data[:, 4]))))
            print("race v.s. income: {}".format(corr(agents_data[:, 2], agents_data[:, 4])))
            print("edu v.s. log income: {}".format(corr(agents_data[:, 3], np.log(agents_data[:, 4]))))
            print("edu v.s. income: {}".format(corr(agents_data[:, 3], agents_data[:, 4])))
            inc = agents_data[:, 4]
            print("income >= 360k: {}".format(inc[inc>=360000].shape))

        # normalize race, education, income
        data_ori = np.copy(agents_data[:, 2:5]).reshape((-1, 3))
        for idx in range(2, 5):
            fea_arr = np.copy(agents_data[:, idx])
            #agents_data[:, idx] = (fea_arr-np.mean(fea_arr))/np.std(fea_arr)
            agents_data[:, idx] = fea_arr / np.max(fea_arr)
        agents_data = np.concatenate((agents_data, data_ori), axis=1)

        if verbose:
            print("agents_data size: {}".format(agents_data.shape))
        return agents_data


    @staticmethod
    def _getID_group_by_race(path_to_info):
        """
        """
        white, black = list(), list()
        college, high_school = list(), list()
        high, low = list(), list()

        info_f = open(path_to_info, newline="")
        agent_rows = csv.reader(info_f)
        for row_idx, agent_row in enumerate(agent_rows):
            if row_idx == 0:
                col_names = agent_row
                continue
            else:
                agent_dict = {col_n:col_val for col_n, col_val in zip(col_names, agent_row)}

            agent_id = int(agent_dict["Respondent id number"])
            
            # race: black v.s. white
            if agent_dict["Race of respondent"] == "White":
                white.append(agent_id)
            elif agent_dict["Race of respondent"] == "Black":
                black.append(agent_id)
            
            # edu: college v.s. high school
            edu_yr = int(agent_dict["Highest year of school completed"])
            if edu_yr >= 16:
                college.append(agent_id)
            if edu_yr < 12:
                high_school.append(agent_id)
            
            # inc: high (>$55000) v.s. low (<$30000)
            inc_str = agent_dict["Total family income"]
            if inc_str == "Under 1000":
                inc_lower_bound, inc_upper_bound = 1, 999
            elif inc_str == "110000 or over":
                # inc_lower_bound, inc_upper_bound = 110000, 650000
                inc_lower_bound, inc_upper_bound = 110000, 388000
            else:
                inc_lower_bound, inc_upper_bound = inc_str.split("to")
                inc_lower_bound, inc_upper_bound = int(inc_lower_bound), int(inc_upper_bound)
            if inc_lower_bound >= 55000:
                high.append(agent_id)
            if inc_upper_bound < 30000:
                low.append(agent_id)
        
        race = {"white":white, "black":black}
        edu = {"college":college, "high school":high_school}
        inc = {"high": high, "low":low}
        return race, edu, inc


    def get_agent_info(self):
        return np.copy(self.agents_data)
    

    def get_agent_race_group_ids(self):
        return self.race
    

    def get_agent_edu_group_ids(self):
        return self.edu
    

    def get_agent_inc_group_ids(self):
        return self.inc
