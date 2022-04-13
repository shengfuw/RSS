import csv
import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

class agent:
    def __init__(self, strategy, neighbors):
        # Current time (t)
        self.strategy = strategy # C = 1, D = 0
        self.neighbors = neighbors # List of the agent's neighbors' index

        # Next time (t+1)
        self.future_strategy = strategy
        self.future_neighbors = [n for n in self.neighbors] # deep coop

    def get_payoff(self, lattice):
        u = sum([lattice.agents[n].strategy for n in self.neighbors])
        s = self.strategy
        total_individual_payoff = s*u + (1-s)*u*lattice.b
        return total_individual_payoff 
                
class lattice: 
    def __init__(self, size, b, p, K=8):
        self.size = size # Number of agents / size of nerwork (N)
        self.b = b # Incentive to defect (T in PD payoff matrix)
        self.p = p # Social plasticity
        self.K = K # Average degree per agent
        self.t = 0 # Time
        self.agents = []
        self.stationary_state = False
        self.allD = False
        
        self.G = nx.gnm_random_graph(self.size, self.size*self.K/2)
        cooperator_index = random.sample(list(range(self.size)), int(self.size*0.6)) # Choose who to become a cooperator

        for n in range(self.size):
            if n in cooperator_index:
                self.agents.append(agent(1, list(self.G.neighbors(n)))) # C-agent
            else:
                self.agents.append(agent(0, list(self.G.neighbors(n)))) # D-agent
            
    def check_stationary_state(self):
        self.stationary_state = True
        for agent in self.agents:
            if agent.future_strategy != agent.strategy or agent.future_neighbors != agent.neighbors:
                self.stationary_state = False
                break

        strategy_set = set([n.future_strategy for n in self.agents])
        if strategy_set == {0}:
            self.allD = True

    def one_round(self):
        self.t += 1

        # Step 1: Interact
        payoff_for_each_agent = []
        for i in range(self.size):
            u_i = sum([self.agents[n].strategy for n in self.agents[i].neighbors])
            s_i = self.agents[i].strategy
            total_individual_payoff = s_i*u_i + (1-s_i)*u_i*self.b
            payoff_for_each_agent.append(total_individual_payoff)
        payoff_for_each_agent = np.array(payoff_for_each_agent)

        for i in range(self.size): 
            neighbors = [n for n in self.agents[i].neighbors]
            neighbors_payoff = payoff_for_each_agent[neighbors]       

            if len(neighbors) == 0:
                continue
            
            # Unsatisfied agent
            if neighbors_payoff.max() > payoff_for_each_agent[i]:         
                # Step 2: Update strategy
                neighbors_with_highest_payoff = np.where(neighbors_payoff == neighbors_payoff.max())[0]
                if len(neighbors_with_highest_payoff) > 1:
                    target = neighbors[random.choice(neighbors_with_highest_payoff)]
                else:
                    target = neighbors[neighbors_with_highest_payoff[0]]
                target_strategy = self.agents[target].strategy
                self.agents[i].future_strategy = target_strategy
    
                # Step 3: Update neighborhood
                if target_strategy == 0: # imitate a D-agent
                    change_neighbor = random.choices([True, False], weights=[self.p, 1-self.p])[0]
                    if change_neighbor:
                        # Break link with with the imitated D neighbor
                        self.agents[i].future_neighbors.remove(target)
                        self.agents[target].future_neighbors.remove(i)
    
                        # Randomly choose partner from the whole neteork
                        candidate = list(range(self.size))
                        
                        candidate.remove(i)
                        for j in self.agents[i].future_neighbors:
                            candidate.remove(j)
                        for j in self.agents[i].neighbors:
                            if j in candidate:
                                candidate.remove(j)

                        new_neighbor = random.choice(candidate) 
                        self.agents[i].future_neighbors.append(new_neighbor)
                        self.agents[new_neighbor].future_neighbors.append(i)

        self.check_stationary_state()
        
        # Move to t+1
        for agent in self.agents:
            agent.strategy = agent.future_strategy
            agent.neighbors = [n for n in agent.future_neighbors] # deep copy    

    def get_fraction_of_cooperator(self):
        return (sum([agent.strategy for agent in self.agents]) / self.size)

if __name__ == '__main__':
    random.seed(14)
    np.random.seed(14)

    parameters_b = [1.2, 1.4, 1.6, 1.8]
    parameters_p = [0, 0.01, 0.1, 1]
    trial_num = 10

    outcome = [] 

    for p in parameters_p:
        for_each_b = []
        for b in parameters_b:
            trials_log = []
            for trial in range(trial_num):
                Mylattice = lattice(10000, b=b, p=p)
                if p != 0:
                    while not Mylattice.stationary_state:
                        Mylattice.one_round()
                    if not Mylattice.allD:
                        fc = Mylattice.get_fraction_of_cooperator()
                        trials_log.append(fc) 
                else:
                    fc_log = []
                    for t in range(1000):
                        Mylattice.one_round()
                        fc_log.append(Mylattice.get_fraction_of_cooperator())
                        fc = sum(fc_log[-100:])/len(fc_log[-100:])
                    trials_log.append(fc) 
            for_each_b.append(sum(trials_log)/len(trials_log))
        outcome.append(for_each_b)

    # Plotting
    x = np.arange(len(parameters_b))
    p_0 = outcome[0]
    p_1 = outcome[1]
    p_2 = outcome[2]
    p_3 = outcome[3]

    fig, ax = plt.subplots(1, 1, figsize=(8, 5))

    width = 0.175
    plt.bar(x + width*0, p_0, width, edgecolor='black', linewidth='1.25', color='black', label='p=0')
    plt.bar(x + width*1, p_1, width, edgecolor='black', linewidth='1.25', color='grey', label='p=0.01')
    plt.bar(x + width*2, p_1, width, edgecolor='black', linewidth='1.25', color='silver', label='p=0.1')
    plt.bar(x + width*3, p_1, width, edgecolor='black', linewidth='1.25', color='white', label='p=1')
    plt.yticks(np.arange(0, 1.01, step=0.1))
    plt.xticks(x + width*(3/2), parameters_b)
    plt.legend(bbox_to_anchor=(1,0.5), loc='center left')
    plt.grid(axis='y', linewidth=.75)

    ax.set_axisbelow(True)
    ax.set_ylim(0, 1)
    ax.set_xlabel("b", fontsize=15)
    ax.set_ylabel("Fraction of cooperaters: fc", rotation=90, y=0.5, fontsize=15)
    ax.yaxis.set_major_formatter(lambda x, pos: f'{x:.3f}'.rstrip('0').rstrip('.'))
    fig.set_facecolor('white')

    plt.savefig('FIG3.jpg')

    # Save data
    data_file_path = 'data.csv'
    with open(data_file_path, 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        for data in outcome:   
            writer.writerow(data)

    print("Finished !")