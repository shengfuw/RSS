import csv
import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

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

    def get_average_payoff_of_cooperators(self):
        payoff_of_cooperators = [agent.get_payoff(self) for agent in self.agents if agent.strategy == 1]
        return (sum(payoff_of_cooperators) / len(payoff_of_cooperators))
    
    def get_average_payoff_of_defectors(self):
        payoff_of_defectors = [agent.get_payoff(self) for agent in self.agents if agent.strategy == 0]
        return (sum(payoff_of_defectors) / len(payoff_of_defectors))

if __name__ == '__main__':
    random.seed(14)
    np.random.seed(14)

    parameter_b = np.arange(1, 2, 0.05)
    trial_num = 10

    # p = 0
    p_0 = []
    for b in parameter_b:
        print(f'{b:.2f}', end=" ")
        trial_log = []
        for trial in range(trial_num):
            Mylattice = lattice(10000, b=b, p=0)
            for round in range(5):
                Mylattice.one_round()
            apc = Mylattice.get_average_payoff_of_cooperators()
            apd = Mylattice.get_average_payoff_of_defectors()
            trial_log.append(apd-apc)

        p_0.append(sum(trial_log)/len(trial_log))
    print()


    # p = 0.1
    trial_num = 3
    p_zero_point_1 = []
    for b in parameter_b:
        print(f'{b:.2f}', end=" ")
        trial_log = []
        trial_counter = 0
        while trial_counter < trial_num:
            Mylattice = lattice(10000, b=b, p=0.1)
            while not Mylattice.stationary_state:
                Mylattice.one_round()

            if not Mylattice.allD:
                apc = Mylattice.get_average_payoff_of_cooperators()
                apd = Mylattice.get_average_payoff_of_defectors()
                trial_log.append(apd-apc)
                trial_counter += 1

        p_zero_point_1.append(sum(trial_log)/len(trial_log))
    
    # Save data
    data_file_path = 'data2.csv'
    with open(data_file_path, 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(p_0)
        writer.writerow(p_zero_point_1)

    fig, ax = plt.subplots(1, 1, figsize=(9, 8))

    plt.scatter(parameter_b, p_0, marker='*') 
    plt.scatter(parameter_b, p_zero_point_1, marker='s') 

    ax.set_xlim([1, 2])
    ax.set_ylim([-2, 10])
    ax.set_xticks([1, 1.2, 1.4, 1.6, 1.8, 2])
    ax.set_yticks([-2, 0, 2, 4, 6, 8, 10])
    ax.set_xlabel("b", y=0.5, fontsize=15)
    ax.set_ylabel(r'$<\Pi_D - \Pi_C>$', rotation=90, y=0.5, fontsize=15)
    ax.xaxis.set_minor_locator(MultipleLocator(0.1))
    ax.yaxis.set_minor_locator(MultipleLocator(1))
    ax.xaxis.set_major_formatter(lambda x, pos: f'{x:.3f}'.rstrip('0').rstrip('.'))
    ax.tick_params(which='both', direction='in', right=True, top=True)
    fig.set_facecolor('white')
    plt.savefig('FIG4.jpg')

    print("Finished !")