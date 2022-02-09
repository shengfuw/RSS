# A model replicating Macy, M. W. (1991). Chains of cooperation: Threshold effects in collective action. American Sociological Review, 730-747.

# Implemented in Python 3.9.6.
# Please execute the script with the file function_threshold_learning.py in the same folder.

## 0. IMPORT ----------------
import numpy as np
import function_threshold_learning as func




## 1. PARAMETERS AND TREATMENTS ----------------

n_agent, iteration = 200, 50
list_slope_logistic = [0, 5] # parameter M in the article
total_resource = 100 # parameter N in the article
range_production = 0 # parameter X in the article, ranges from -1 to 1
jointness_supply = 0.25 # parameter J in the article; J = 0.25, 0.5, or 1
initial_participation_rate = 0.5

# treatments
list_choice_threshold = ['parallel_decision', 'groupwise_serial']

# choose the initial distribution of resource here:
resource_distribution = 'normality'
# resource_distribution = 'equality'

# choose the type of collective action here:
type_collective_action = 'cost_reduction' 
# cooperation merely reduces public bads, X = -1, see page 738 in the article
# type_collective_action = 'mixed_outcome' # cooperation reduces public bads and acquires public goods, X = 0 and -0.5 < L < 0.5, see page 738 in the article




## 2. DATA ARRAY----------------

population = np.empty((n_agent, 8)) # population array, recording attributes of agents: [0] share of resource (parameter R_j in the article); [1] interest in the public goods; [2] threshold of participation; [3] probability to volunteer; [4] volunteer or not (1 vs 0, parameter V_j in the article); [5] contribution; [6] share of public goods (parameter S_j in the article); [7] learning rate (parameter E_j in the article)


share_public_goods = np.empty((n_agent, iteration)) # record agents' shares of public good over time

outcome = np.empty((n_agent, iteration)) # record each individual's outcome over time, parameter O_ij in equation 5, page 739

data_number_volunteer = np.empty((iteration, 1)) # record numbers of volunteers over time

data_contribution = np.empty((iteration, 2)) # record contribution levels in the conditions: [0] parallel choice; [1] serial choice

data_threshold = np.empty((iteration, 2)) # [0] mean threshold for volunteers; [1] mean threshold for free-riders

data_participation = np.empty((iteration + 1, 1)) # record the participation rate over time
data_participation[0, 0] = initial_participation_rate # set the initial participation rate

population = func.initialize_population(population, resource_distribution) # initialize the population array




## 3. STEPS ----------------

for i in range(len(list_choice_threshold)):
    choice_threshold = list_choice_threshold[i]
    slope_logistic = list_slope_logistic[i]

    for t in range(iteration):
        
        # STEP 1. Decision --------
        
        # update probability to volunteer and volunteer or not
        population = func.volunteer(population, data_participation[t, 0], slope_logistic)

        # record number of volunteers
        data_number_volunteer[t, 0] = np.sum(population[:, 4])
        
        # update participation rate
        data_participation[t+1, 0] = np.sum(population[:, 4]) / n_agent
        
        # contribution by each individual
        population[:, 5] = population[:, 0] * total_resource * population[:, 4] # equation 2 in page 737 of the article

        data_contribution[t, i] = np.sum(population[:,5]) / total_resource



        # STEP 2: Production --------
        L = func.produce(data_participation[t+1, 0], range_production, type_collective_action) # see page 738

        population[:, 6] = func.share(L, total_resource, jointness_supply, population) # see equation 4, page 738

        share_public_goods[:, t] = population[:, 6] # record agents' shares of public goods over time



        # STEP 3: Learning --------
        outcome[:, t] = func.calculate_outcome(population, outcome, share_public_goods, t)
        
        if choice_threshold == 'groupwise_serial':
            population[:, 2] = func.adjust_threshold(population, outcome, t)




## 4. OUTPUT ----------------

func.plot_line(data_contribution)