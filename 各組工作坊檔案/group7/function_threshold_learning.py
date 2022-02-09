import numpy as np
import matplotlib.pyplot as plt

def initialize_population(population, resource_distribution):

    n_agent = len(population)

    if resource_distribution == 'equality':
        population[:, 0] = 1 / n_agent

    # CHECK THIS LATER;
    elif resource_distribution == 'normality':
        rj = np.random.randint(0, 2, n_agent)
        rj = np.clip(rj, 0, None)            
        population[:, 0] = rj / np.sum(rj)
    
    population[:, 1] = np.random.normal(1, 0.2, n_agent) # "the mean interest is one", but not specified sd, see page 738
    population[:, 1] = np.clip(population[:, 1], -2 * 0.2, 2 * 0.2) # bounded by 2 sd

    population[:, 2] = 1 # "The simulation begins with Tij = 1", see page 740
    # population[:, 2] = np.random.uniform(0, 1, n_agent)

    population[:, 7] = np.random.normal(0.5, 0.15, n_agent) # "0 <= ej <= 1", but not specified sd, see page 739
    population[:, 7] = np.clip(population[:, 1], -2 * 0.2, 2 * 0.2) # bounded by 2 sd

    return population


def volunteer(population, participation_rate, slope_logistic):
    '''the cumulative logistic function (equation 1, page 736)'''
    
    number_agents = len(population)
    
    population[:, 3] = 1 / (1 + np.exp((population[:, 2] - participation_rate) * slope_logistic))

    draw = np.random.uniform(0, 1, number_agents)
    population[population[:, 3] > draw, 4] = 1
    population[population[:, 3] <= draw, 4] = 0

    return population


def produce(rate_contribution, range_production, type_collective_action): 
    '''the S-shape production function (equation 3, page 737)'''

    if type_collective_action == 'cost_reduction':
        range_production = -1
    elif type_collective_action == 'mixed_outcome':
        range_production = 0

    production = 1 / (1 + np.exp(-(rate_contribution - 0.5) * 10)) - (1 - range_production) / 2
    
    return production


def share(production, total_resource, jointness_supply, population):
    '''the share of public goods as a function of the jointness of supply (equation 4, page 738)'''

    share_public_goods = (production * total_resource * population[:, 1]) / (total_resource ** (1 - jointness_supply)) - population[:, 5]

    return share_public_goods


def calculate_outcome(population, outcome, share_public_goods, time):
    '''the standardized outcome (equation 5, page 739)'''

    previous_return = np.empty((len(population), 1))

    if time == 0:
        previous_return[:, 0] = population[:, 0]
    elif time > 0:
        previous_return[:, 0] = share_public_goods[:, time]
    
    sMax = max(population[:, 6]) # NOT SURE ABOUT THIS; ATTENDED THE OFFICE HOUR AND THE FACULTY SAID WE CAN ADDRESS THIS IN THE PRESENTATION

    new_outcome = (population[:, 7] * (2 * population[:, 6] - previous_return[:, 0])) / 3 * abs(sMax)

    return new_outcome


def adjust_threshold(population, outcome, t):
    '''the threshold (equation 6, page 739)'''

    reward = outcome[:, t] * (1 - ((1 - population[:, 2]) ** (1 / abs (outcome[:, t])))) * population[:, 4]

    punishment = outcome[:, t] * (1 - ((1 - population[:, 2]) ** (1 / abs (outcome[:, t])))) * ( 1 - population[:, 4])
    
    new_threshold = np.clip(population[:, 2] - reward + punishment, 0, 1)

    return new_threshold


def plot_line(data):
    T = data.shape[0]
    x = np.arange(0, T)
    plt.figure(1)
    # plt.subplot(111)
    mylabel = ['Parallel Choice', 'Serial Choice']
    
    for i in range(len(mylabel)):
        plt.plot(x, data[:, i], label=mylabel[i])
    
    plt.legend()
    plt.title('Level of Contribution over Time')
    plt.xlabel('Iteration')
    plt.ylabel('Level of Contribution')
    plt.grid(True)
    plt.ylim([-0.02,1.02])
    
    plt.show()