import numpy as np
import networkx as nx
from scipy.stats import poisson
import matplotlib.pyplot as plt

def poissongraph(n,k):
    z= np.zeros(n) # n is number of nodes
    for i in range(n):
        z[i]=poisson.rvs(k) # k is the expected value (connectivity)
    G=nx.expected_degree_graph(z, selfloops = False, seed = 123)
    return G

def plot_network(G):
    G.remove_nodes_from(list(nx.isolates(G)))
    nx.draw(G)
    plt.show()

def plot_line(data):
    plt.figure(2)
    plt.plot(np.arange(0, iteration), data[:, 0], label='proportion of cooperator')
    
    plt.legend()
    plt.title('Proportion of Cooperator over Time')
    plt.xlabel('Iteration')
    plt.ylabel('Proportion of Cooperator')
    plt.grid(True)
    plt.ylim([-0.02,1.02])
    
    plt.show()