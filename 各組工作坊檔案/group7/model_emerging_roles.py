# A model replicating Eguíluz, V. M., Zimmermann, M. G., Cela-Conde, C. J., & Miguel, M. S. (2005). Cooperation and the emergence of role differentiation in the dynamics of social networks. American journal of sociology, 110(4), 977-1008.

# Implemented in Python 3.9.6
# Please execute the script with the file function_emerging_roles.py in the same folder.

## 0. IMPORT ----------------
from networkx.classes.function import neighbors
import numpy as np
import networkx as nx
import random
import function_emerging_roles as func
import matplotlib.pyplot as plt




## 1. PARAMETERS ----------------

n_agent, iteration = 50, 100
# n_agent, iteration = 10000, 10/1000 # the required time steps for reaching stationary state depends on p, see page 994. In this replication, I don't suggest such large N since it will take a while to complete

T, R, P, S = 1.75, 1, 0, 0 
# parameters are based on the main analyses, see page 993. b = T, and 1<b<2 
# T, R, P, S values for temptation, reward, punishment, and sucker
payoffs = np.array([ [R, S], [T, P] ]) # payoff matrix of the PD game

proportion_cooperator = 0.6
proportion_types = [proportion_cooperator, 1-proportion_cooperator] #  # initial proportion of cooperators and defectors

k = 3 # average links per node of the network, this is different from what paper used (k=8)
p = 0.9 # social plasticity of the agents, see page 987




## 2. DATA ARRAY AND THE NETWORK ----------------

population = np.zeros((n_agent, 2)) # [0] current strategy: cooperate (0) or defect (1); [1] future strategy: cooperate (0) or defect (1)

population[:, 0] = np.random.multinomial(1, proportion_types, n_agent).argmax(1) # initial strategies according to initial proportion of cooperator

utilities = np.zeros((n_agent, 1)) # [0] utilities of the agents

data = np.zeros((iteration, 1))

G = func.poissongraph(n_agent, k) # approximate the network initial condition, see page 993

G.nodes() # gives nodes
G.edges() # gives links between nodes




## 3. STEPS ----------------

for t in range(iteration):

    # STEP 1. Interact (PD games) --------
    for i in G.edges():

        player_1 = i[0]
        player_2 = i[1]

        # play the prisoner's dilemma game:
        utilities[player_1, 0] += payoffs[int(population[player_1, 0]), int(population[player_2, 0])]
        
        utilities[player_2, 0] += payoffs[int(population[player_2, 0]), int(population[player_1, 0])]
    
    

    # STEP 2. Update Strategy --------
    for i in G.nodes():

        # Below code chunks find the neighbors (including self) with the highest utility
        
        # find the neighbors
        neighbors = [n for n in G.neighbors(i)]

        # list the numbers of neighbors and self together
        if neighbors != []:
            neighbors_and_self = np.append(neighbors, i)
        else: 
            neighbors_and_self = [i]
        
        # list the utilities of neighbors and self
        utilities_neighbors_and_self = utilities[neighbors_and_self]
        
        # find the highest utility
        neighbors_and_self_dict = dict(zip(neighbors_and_self, utilities_neighbors_and_self))
        highest_utility = max(neighbors_and_self_dict.values())

        # find the number of node/agent with the highest utility
        all_neighbor_with_highest_utility = [k for k, v in neighbors_and_self_dict.items() if v == highest_utility] # collect all neighbors who have highest utilities 
        neighbor_with_highest_utility = random.choice([i for i in all_neighbor_with_highest_utility])


        if neighbor_with_highest_utility != i: # only unsatisfied agents enact imitation and social plasticity (see page 989)
            
            population[i, 1] = population[neighbor_with_highest_utility, 0] # copy the strategy of the neighbor with highest utility



            # STEP 3. Update Neighborhoods --------
 
            # note: we use asynchronous updating of network evolve rate
            # "the game is played synchronously" (see page 987) & "using an asynchronous updating in our simulations does not change any meaningful qualitative result" (see page 993)
            
            if population[neighbor_with_highest_utility, 0] == 1: # if agent i imitates a defector
                
                if np.random.uniform(0, 1, 1) < p:
                    
                    G.remove_edge(neighbor_with_highest_utility, i) # remove edge with a defector
                    
                    chosen_node = random.choice([j for j in G.nodes() if j != i]) # randomly chosen partner from the whole network. 
                    
                    G.add_edge(chosen_node, i) # establish a tie between new partner and ego            
    
    population[:, 0] = population[:, 1] # future strategies become current strategies
    
    data[t, 0] = 1 - np.mean(population[:, 0]) # record numbers of cooperators




## 4. OUTPUT ----------------

## 4.1 Plot the Network --------

plt.figure(1)

# choose layout:
# pos = nx.circular_layout(G)
pos = nx.kamada_kawai_layout(G)
# pos = nx.random_layout(G)
# pos = nx.shell_layout(G)
# pos = nx.spring_layout(G)
# pos = nx.spiral_layout(G)

nx.draw_networkx_nodes(G, pos, nodelist = list(np.where((population[:, 0] == 0) & (utilities[:, 0] <= 300))[0]), node_color = 'grey', node_size = 50, alpha = 0.8) # mark cooperators (conformists)

nx.draw_networkx_nodes(G, pos, nodelist = list(np.where((population[:, 0] == 0) & (utilities[:, 0] > 300))[0]), node_color = 'red', node_size = 50, alpha = 0.8) # mark cooperators (leaders)

nx.draw_networkx_nodes(G, pos, nodelist = list(np.where(population[:, 0] == 1)[0]), node_color = 'black', node_size = 50, alpha = 0.8) # mark defectors (exploiters)

nx.draw_networkx_edges(G, pos, width = 0.5, alpha = 0.8)

nx.draw_networkx_labels(G, pos, labels={n: utilities[n,0] for n in pos}, font_size=8, alpha = 0.8)

plt.show()



## 4.2 Plot the Proportion of Cooperators --------

plt.figure(2)
# func.plot_line(data)
plt.plot(np.arange(0, iteration), data[:, 0], label='proportion of cooperator')
plt.legend()
plt.title('Proportion of Cooperator over Time')
plt.xlabel('Iteration')
plt.ylabel('Proportion of Cooperator')
plt.grid(True)
plt.ylim([-0.02,1.02])
plt.show()
