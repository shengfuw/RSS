import argparse
import csv
import itertools
import multiprocessing
from random import random
import numpy as np
import os
import pandas as pd

from args import ArgsConfig
from plot import PlotLinesHandler
from plot_scatter import plot_scatter_pop, plot_scatter_turn
 
def truncated_normal() -> float:
    rnt = np.random.normal(loc=0.5, scale=1)
    while rnt > 1.0 or rnt < 0.0:
        rnt = np.random.normal(loc=0.5, scale=1)
    return rnt

def draw(p) -> bool:
    return True if np.random.uniform() < p else False

class Consultant:
    _ids = itertools.count(0)

    def __init__(self, inno_init) -> None:
        self.id = next(self._ids)
        
        self.inno = inno_init
        self.quality = truncated_normal()
        # initial values???
        self.r_last = 0
        self.r_cur = 0
        self.a_h_last = 0

        self.clients = []
        self.o_avg_list = []  

    def __str__(self) -> str:
        return "Con {} | inno: {} return: {:.3f} | clients: {}".format(self.id, self.inno, self.r_cur, [f.id for f in self.clients])


class Firm:
    _ids = itertools.count(0)

    def __init__(self, inno_init) -> None:
        self.id = next(self._ids)

        # initial values???
        self.inno = inno_init
        self.o_last = 0
        self.o_cur = 0
        self.a_h_last = 0

        self.consultant = None

    def __str__(self) -> str:
        return "Firm {} | inno: {} outcome: {:.3f} | con: {}".format(self.id, self.inno, self.o_cur, self.consultant.id)
    


class Market:

    def __init__(self, args: argparse.ArgumentParser, verbose=True) -> None:
        np.random.seed(args.rnd_seed)
        self.args = args
        self.verbose = verbose

        # consultant
        self.cons = [Consultant(inno) for inno in np.random.randint(low=0, high=self.args.n_innovation, size=self.args.n_consultant)]
        self.inno_to_con = [{"con": [], "prob_w": []} for _ in range(self.args.n_innovation)]
        for con in self.cons:
            self.inno_to_con[con.inno]["con"].append(con)
            self.inno_to_con[con.inno]["prob_w"].append(0 + self.args.c)
        
        # firm
        self.firms = [Firm(inno) for inno in np.random.choice(self.get_inno_pool(), size=self.args.n_firm)]
        self.inno_to_firm_n = [0 for _ in range(self.args.n_innovation)]
        for firm in self.firms:
            self.inno_to_firm_n[firm.inno] += 1
        
        # value of innovations
        self.inno_V = [truncated_normal() for _ in range(self.args.n_innovation)]

        # record
        self.firm_adp_rate = list()
        self.firm_most_inno = list()
        self.con_adp_rate = list()
        self.con_most_inno = list()
        self.turnover = 0
        self.popularity = None

        # initial matches
        for firm in self.firms:
            selected_con = self.select_con_by_inno(inno_id=firm.inno)
            firm.consultant = selected_con
            selected_con.clients.append(firm)

    
    def select_con_by_inno(self, inno_id) -> Consultant:
        prob = np.array(self.inno_to_con[inno_id]["prob_w"])
        prob = prob / np.sum(prob)
        prob[np.argmax(prob)] += 1 - np.sum(prob) # adjust it to make its sum be exactly 1.0
        selected_con_id = np.random.choice(np.arange(len(self.inno_to_con[inno_id]["con"])), p=prob)
        return self.inno_to_con[inno_id]["con"][selected_con_id]
    

    def get_inno_pool(self) -> list:
        """ Return a list of all innovation that at least one consultant supplies. """
        return np.array([inno for inno in range(self.args.n_innovation) if self.inno_to_con[inno]["con"]])


    def simulate_step(self) -> None:
        # 1: consultants have an innovation to supply
        # 2: firms have an innovation to demand
        # 3: a firm select a consultant

        ## 4: the consultant recieves a return
        for con in self.cons:
            con_return = self.args.eta * len(con.clients) * \
                         (self.inno_to_firm_n[con.inno]/len(self.inno_to_con[con.inno]["con"]))
            con.r_cur = con_return
            
            # Because average otucome is calculated from "previous clients"
            if con.clients:
                con.o_avg_list.append([firm.o_cur for firm in con.clients])
                if len(con.o_avg_list) > self.args.window:
                    del con.o_avg_list[0]
                assert len(con.o_avg_list) <= self.args.window

        # 5: the firm recieves an outcome
        for firm in self.firms:
            firm_outcome = self.args.alpha * self.inno_V[firm.inno] + \
                           self.args.beta * firm.consultant.quality + \
                           (1-self.args.alpha-self.args.beta) * truncated_normal()
            firm.o_cur = firm_outcome


        # 4: the consultant recieves a return
        # for con in self.cons:
        #     con_return = self.args.eta * len(con.clients) * \
        #                  (self.inno_to_firm_n[con.inno]/len(self.inno_to_con[con.inno]["con"]))
        #     con.r_cur = con_return
        #     if con.clients:
        #         con.o_avg_list.append([firm.o_cur for firm in con.clients])
        #         if len(con.o_avg_list) > self.args.window:
        #             del con.o_avg_list[0]
        #         assert len(con.o_avg_list) <= self.args.window

        # 6: consultants decide whether to make a change
        r_cur_arr = np.array([con.r_cur for con in self.cons])
        ## just-completed round?
        # best_con_idx = np.argmax(r_cur_arr)

        r_last_arr = np.array([con.r_last for con in self.cons])  
        best_con_idx = np.argmax(r_last_arr)
        ##
        best_con_inno = self.cons[best_con_idx].inno
        sum_r_cur = np.sum(r_cur_arr)

        for con in self.cons:
            aspi_history = (1-self.args.xi_c) * con.a_h_last + self.args.xi_c * con.r_last
            aspi_social = (sum_r_cur - con.r_cur) / (self.args.n_consultant - 1)
            aspi_total = self.args.gamma_c * aspi_history + (1-self.args.gamma_c) * aspi_social
            prob_change = 1 / (1 + np.exp(self.args.a_c + self.args.b_c*(con.r_cur - aspi_total)))
              
            # if prob_change > .9 and draw(.7):
            #     prob_change = 0.0
            #     print("!", end=" ")
            # if prob_change < .1 and draw(.7):
            #     prob_change = 0.9999
                # print("*", end=" ")
            # print("c", f"{prob_change:.3f}", f"{self.args.a_c + self.args.b_c*(con.r_cur - aspi_total):0.3f}", f"{con.r_cur:.3f}", f"{aspi_total:.3f}", f"{aspi_history:.3f}", f"{aspi_social :.3f}","|", len(con.clients), self.inno_to_firm_n[con.inno], len(self.inno_to_con[con.inno]["con"]), "|", con)

            # find the index of con in self.inno_to_con[con.inno]["con"]
            con_index = 0
            while self.inno_to_con[con.inno]["con"][con_index].id != con.id:
                con_index += 1
                assert con_index < len(self.inno_to_con[con.inno]["con"])

            if draw(prob_change):
                # remove from the original inno
                self.inno_to_con[con.inno]["con"].pop(con_index)
                self.inno_to_con[con.inno]["prob_w"].pop(con_index)

                if draw(self.args.p_mimic_c):
                    con.inno = best_con_inno
                else:
                    con.inno = np.random.randint(self.args.n_innovation)

                # add to new inno
                self.inno_to_con[con.inno]["con"].append(con)
                self.inno_to_con[con.inno]["prob_w"].append(0 + self.args.c)

                con.o_avg_list = []
                con_ori_clients = con.clients.copy()
                con.clients = []

                # its clients reselect other consultants with same inno
                for firm in con_ori_clients:
                    if not self.inno_to_con[firm.inno]["con"]:
                        self.inno_to_firm_n[firm.inno] -= 1
                        firm.inno = np.random.choice(self.get_inno_pool())
                        self.inno_to_firm_n[firm.inno] += 1
                    firm.consultant = self.select_con_by_inno(inno_id=firm.inno)
                    firm.consultant.clients.append(firm)
            
            else:
                all_o = []
                for l in con.o_avg_list:
                    all_o += l
                o_avg = sum(all_o) / len(all_o) if all_o else 0
                self.inno_to_con[con.inno]["prob_w"][con_index] = o_avg + self.args.c
            
            # update consultant data
            con.a_h_last = aspi_history
            con.r_last = con.r_cur
            con.r_cur = 0

        # 7: firms decide whether to make a change
        ## just-completed round? 
        # best_firm_sort = sorted(self.firms, key=lambda f: f.o_cur, reverse=True)
        best_firm_sort = sorted(self.firms, key=lambda f: f.o_last, reverse=True)
        ##
        while len(self.inno_to_con[best_firm_sort[0].inno]["con"]) == 0:
            del best_firm_sort[0]
        best_firm_inno = best_firm_sort[0].inno
        best_firm_con = best_firm_sort[0].consultant
        sum_o_cur = np.sum([firm.o_cur for firm in self.firms])
        inno_pool_con = self.get_inno_pool()

        for firm in self.firms:
            aspi_history = (1-self.args.xi_f) * firm.a_h_last + self.args.xi_f * firm.o_last
            aspi_social = (sum_o_cur - firm.o_cur) / (self.args.n_firm - 1)
            aspi_total = self.args.gamma_f * aspi_history + (1-self.args.gamma_f) * aspi_social
            prob_change = 1 / (1 + np.exp(self.args.a_f + self.args.b_f*(firm.o_cur - aspi_total)))


            # print("f", f"{prob_change:.3f}", f"{self.args.a_f + self.args.b_f*(firm.o_cur - aspi_total):.3f}", f"{firm.o_cur:.3f}", f"{aspi_total:.3f}", "|", firm)
            # prob_change = min(prob_change*5, 1)

            if draw(prob_change):
                # consultant lose a client
                for cli_idx, cli in enumerate(firm.consultant.clients):
                    if cli.id == firm.id:
                        firm.consultant.clients.pop(cli_idx)
                self.inno_to_firm_n[firm.inno] -= 1

                ## ! 如果已經是best innovation，隨機抽一個
                # if draw(self.args.p_mimic_f):
                if draw(self.args.p_mimic_f) and firm.inno != best_firm_inno:
                ##
                    firm.inno = best_firm_inno
                    ##
                    # firm.consultant = best_firm_con
                    ##
                else:
                    ## ！ 不能選到原本的 innovation
                    # firm.inno = np.random.choice(inno_pool_con)
                    firm.inno = np.random.choice(inno_pool_con[inno_pool_con != firm.inno])
                    ##
                    # firm select a new consultant supplying firm.inno
                    # firm.consultant = self.select_con_by_inno(inno_id=firm.inno)
                # Why firm.consultant = best_firm_con?
                firm.consultant = self.select_con_by_inno(inno_id=firm.inno)
                ##
                firm.consultant.clients.append(firm)
                self.inno_to_firm_n[firm.inno] += 1
            
            # update firm data
            firm.a_h_last = aspi_history
            firm.o_last = firm.o_cur
            firm.o_cur = 0
    

    def get_firm_turnover(self) -> int:
        return self.turnover
    
    
    def get_firm_popularity(self) -> float:
        return sum(self.firm_adp_rate) / len(self.firm_adp_rate)
    
    
    def simulate(self):
        for step in range(self.args.n_periods):

            if self.verbose and step > 1:
                print("step {:3d} | firm: {:.4f}; most_inno: {:2d} | con: {:.4f}; most_inno: {:2d}".format(step,
                    self.firm_adp_rate[-1], self.firm_most_inno[-1], self.con_adp_rate[-1], self.con_most_inno[-1]))

            self.simulate_step()

            firm_len = np.array(self.inno_to_firm_n)
            assert np.sum(firm_len) == self.args.n_innovation
            ##
            # self.firm_adp_rate.append(np.max(firm_len)/self.args.n_innovation)
            self.firm_adp_rate.append(np.max(firm_len)/self.args.n_firm)
            ##
            self.firm_most_inno.append(np.argmax(firm_len))
            self.turnover += 1 if len(self.firm_most_inno) == 1 or self.firm_most_inno[-1] != self.firm_most_inno[-2] else 0

            con_len = np.array([len(d["con"]) for d in self.inno_to_con])
            assert np.sum(con_len) == self.args.n_innovation
            ##
            # self.con_adp_rate.append(np.max(con_len)/self.args.n_innovation)
            self.con_adp_rate.append(np.max(con_len)/self.args.n_consultant)
            ##
            self.con_most_inno.append(np.argmax(con_len))

            if self.verbose:
                print("step {:3d} | firm: {:.4f}; most_inno: {:2d} | con: {:.4f}; most_inno: {:2d}".format(step,
                    self.firm_adp_rate[-1], self.firm_most_inno[-1], self.con_adp_rate[-1], self.con_most_inno[-1]))

def simulate_trails(args, alpha, beta, rnd_seed, log_data, fix_alpha):
    args.alpha = alpha
    args.beta = beta
    turn, pop = [], []
    for trail_idx in range(args.n_trails):
        args.rnd_seed = rnd_seed + trail_idx
        m = Market(args, verbose=False)
        m.simulate()
        turn.append(m.get_firm_turnover())
        pop.append(m.get_firm_popularity()*100)
        print("alpha, beta: ({:.2f}, {:.2f}) | trail {}/{} | turn: {:3d} pop: {:.2f}".format( \
            args.alpha, args.beta, trail_idx+1, args.n_trails, turn[-1], pop[-1]))
    log_data.append([args.alpha, args.beta, 
                     np.mean(turn), np.std(turn),
                     np.mean(pop), np.std(pop), (1 if fix_alpha else 0)])
    



if __name__ == "__main__":
    args_config = ArgsConfig()
    args = args_config.get_args()

    # figure 2 single trial
    m = Market(args)
    m.simulate()

    plh_firm = PlotLinesHandler(xlabel="Iterations", ylabel="Adoption", ylabel_show="% Adoption",
                                x_lim=args.n_periods+15, y_lim=101)
    plh_con = PlotLinesHandler(xlabel="Iterations", ylabel="Adoption", ylabel_show="% Adoption",
                               x_lim=args.n_periods+15, y_lim=101)
    
    plh_firm.plot_line(np.array(m.firm_adp_rate), color="black")
    plh_firm.plot_changes(m.firm_most_inno, m.firm_adp_rate, color="black")
    plh_firm.save_fig(title_param="rndSeed_{}_firm".format(args.rnd_seed))

    plh_con.plot_line(np.array(m.con_adp_rate), color="black")
    plh_con.plot_changes(m.con_most_inno, m.con_adp_rate, color="black")
    plh_con.save_fig(title_param="rndSeed_{}_con".format(args.rnd_seed))

    # figure 3, 4
    RANDOM_SEED = args.rnd_seed
    manager = multiprocessing.Manager()
    log_data = manager.list()

    args_list = list()
    for val in range(0, 101, 10):
        args_list.append([args, val/100, 0, RANDOM_SEED, log_data, False])
        args_list.append([args, 0, val/100, RANDOM_SEED, log_data, True])

    n_cpus = multiprocessing.cpu_count()
    print("cpu count: {}".format(n_cpus))
    pool = multiprocessing.Pool(n_cpus+2)
    pool.starmap(simulate_trails, args_list)
        
    # write to csv
    out_fn = "alpha_beta_rndSeed_{}_trail_{}_firm.csv".format(RANDOM_SEED, args.n_trails)
    out_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), out_fn)
    out_file = open(out_file_path, "w", newline="")
    out_writer = csv.writer(out_file)
    out_writer.writerow(["alpha", "beta", "turn_mean", "turn_std", "pop_mean", "pop_std", "fix_alpha"])
    for row in log_data:
        out_writer.writerow(row)
    out_file.close()
    
    # plot
    file_df = pd.read_csv(out_file_path)
    alpha_df = file_df[file_df.fix_alpha == 0]
    alpha_df.sort_values(by=["alpha"], ascending=[True],
                         ignore_index=True, inplace=True)
    beta_df = file_df[file_df.fix_alpha == 1]
    beta_df.sort_values(by=["beta"], ascending=[True],
                        ignore_index=True, inplace=True)
    plot_scatter_pop(alpha_df, beta_df, RANDOM_SEED, args.n_trails)
    plot_scatter_turn(alpha_df,beta_df, RANDOM_SEED, args.n_trails)
    
    
        
        
        

