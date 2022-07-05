import random
import numpy as np
import networkx as nx
from datetime import datetime

class Agent:
    def __init__(self, index, neighbors, fixed_num, flex_num):
        self.index = index
        self.neighbors = np.array(neighbors)
        self.fixed_array = np.array(random.choices([0, 1], k=fixed_num)) # static attributes
        self.flex_array = np.array(random.choices([0, 1], k=flex_num)) # dynamic attributes
    
    def update_an_opinion(self, lattice):
        rand_dim = random.randint(0, lattice.flex_num-1)

        wieghts = np.array([lattice.weight_of_two_agent(self.index, j) for j in self.neighbors])
        probabilitys = abs(wieghts) / sum(abs(wieghts))

        urn = []
        for i, n in enumerate(self.neighbors):
            if random.uniform(0, 1) <= probabilitys[i]:
                nbr_opinion = lattice.agents[n].flex_array[rand_dim]
                # negative influence
                if wieghts[i] < 0 and random.uniform(0, 1) <= 0.1: 
                    urn.append(1-nbr_opinion)
                else:
                    urn.append(nbr_opinion)
        if len(urn) > 0:
            self.flex_array[rand_dim] = random.choice(urn)
    
class Lattice:
    def __init__(self, agent_num, fixed_num=5, flex_num=20):
        self.agent_num = agent_num # network size
        self.fixed_num = fixed_num 
        self.flex_num = flex_num

        # Create network
        k = 99
        G = nx.connected_caveman_graph(int(agent_num/(k+1)), k+1)
        self.edge_num = len(G.edges()) * 2 # 作者原始 code 中的 edge_count，把 (i, j) 和 (j, i) 視為兩條 edges。

        # Rewire edges by Maslov-Sneppen procedure
        rewire_ratio = 0.1
        rewired_edge_num = int(rewire_ratio * len(G.edges()))
        for i in range(rewired_edge_num):
            G = nx.double_edge_swap(G)
        self.G = G

        # Convert network to adjacency list
        adjacency_list = [list(neighbors.keys()) for _, neighbors in G.adjacency()]

        self.agents = [] # list storing agent objects
        for i in range(agent_num):
            self.agents.append(Agent(i, adjacency_list[i], self.fixed_num, self.flex_num))

        # Calculate the expected distance E(d) at iteration 0
        self.NormedDistance = 0
        for i in range(agent_num):
            for j in self.agents[i].neighbors:
                self.NormedDistance += self.distance_of_two_agent(i, j)
        self.NormedDistance /= self.edge_num

    def distance_of_two_agent(self, i, j):
        distance = sum(abs(self.agents[i].fixed_array - self.agents[j].fixed_array)) 
        distance += sum(abs(self.agents[i].flex_array - self.agents[j].flex_array)) # 平方等同於取絕對值
        return distance**0.5

    def weight_of_two_agent(self, i, j): 
        return self.NormedDistance - self.distance_of_two_agent(i, j)
    
    def one_round(self):
        sampled_agent_index = random.randint(0, self.agent_num-1)
        self.agents[sampled_agent_index].update_an_opinion(self)

    def start_simulate(self):
        max_iterations = self.agent_num*self.flex_num*1000
        current_energy, previous_energy = 0, 0
        sample_size = 100 # used for equilibrium test
        sample1 = [0]*sample_size
        sample2 = [0]*sample_size
        drop = False # initial drop in the equilibrium test
        
        self.equil = False # state of equilibrium
        self.iteration = 0 # number of iteration
        while(self.equil == False and self.iteration < max_iterations):
            self.one_round()

            if (self.iteration%10000 == 0 & drop == False):
                current_energy = self.get_energy()
                if previous_energy-current_energy == 0: self.equil=True
                previous_energy = current_energy
                if current_energy < -0.1: drop=True

            if (self.iteration%10000 == 0 & drop == True):
                current_energy = self.get_energy()
                sample1[int((self.iteration/10000)%sample_size)] = current_energy
                if int((self.iteration/10000)%sample_size) == sample_size - 1:
                    if self.ttest(sample1, sample2) == False and self.iteration > 10000*100: self.equil = True
                    sample2 = [i for i in sample1]

            self.iteration += 1

    def ttest(self, sample1, sample2):
        size = len(sample1)
        sample1_arr = np.array(sample1)
        sample2_arr = np.array(sample2)
        m1 = np.mean(sample1_arr)
        m2 = np.mean(sample2_arr)
        s1 = np.var(sample2_arr)
        s2 = np.var(sample2_arr)
        t = (m1-m2)/((s1/size+s2/size)**2)
        return (t > 2.576 or t <= 2.576)

    def get_corr_of_flex(self):
        warning = ""
        mean_pairwise_corr_magnitude = 0
        counter = 0
        for i in range(self.flex_num):
            for j in range(self.fixed_num):
                if i != j:
                    counter += 1
                    dimension1 = [a.flex_array[i] for a in self.agents]
                    dimension2 = [a.flex_array[j] for a in self.agents]
                    if len(np.unique(dimension1)) == 1 or len(np.unique(dimension2)) == 1:
                        warning += "!"
                        corr = 1
                    else:
                        corr = np.corrcoef(dimension1, dimension2)[0, 1]
                    mean_pairwise_corr_magnitude += abs(corr)
        mean_pairwise_corr_magnitude /= counter

        print(self.agent_num, warning)
        return mean_pairwise_corr_magnitude
    
    def get_energy(self): # structrual_dissonance
        energy = 0
        for i in range(self.agent_num):
            oi = self.agents[i].flex_array
            for j in self.agents[i].neighbors:
                w = self.weight_of_two_agent(i, j)
                oj = self.agents[j].flex_array
                energy += w * sum(2*abs(oi-oj)-1)
        return energy / (self.edge_num*self.flex_num)


def one_trial(netsize, log_data):
    start_time = datetime.now()
    Mylattice = Lattice(netsize)
    Mylattice.start_simulate()
    log_data.append((netsize, Mylattice.get_corr_of_flex(), Mylattice.get_energy(), Mylattice.equil, Mylattice.iteration, str(datetime.now()-start_time).split('.')[0]))
