'''
Created on 2012-1-21
**access_network.py**
 @ agent based computational model for network autocorrelation
 DellaPosta, Daniel, Yongren Shi and Michael W. Macy. Why do Liberals Drink Lattes?
 If you have any comment or question about the code, please contact Yongren Shi at ys334@cornell.edu 
 note: the code need to have the network structure prepared before it can be run.
 Terms might be confusing in the code: dynamic==flexible==opinion; static==fixed==demographic trait.
The code creates networks with specified number of caves and rewiring conditions. It needs to be run before the main simulation starts, if the network files are not existent. 
For MS_rewiring_500_10.0.txt, it means the total number of nodes are 500, composed of 5 100-node caves. 10% of all the pre-existed edges are rewired through the Maslov-Sneppen procedure. It is similar to double_edge_swap function in networkx package.
'''

import random
import networkx as nx
import matplotlib.pyplot as plt

class access_network:
    def __init__(self):
        pass
        
    def old_complete_graph(self, N):
        return nx.complete_graph(N)
    
    def new_complete_graph(self, nlist):
        G=nx.Graph()
        for i in nlist:
            for j in nlist:
                if i!=j:
                    G.add_edge(i,j)
        return G
    
    #parameters: number of caves, size of cave
    def caveman_network(self, n_caves, cave_size):
        G=nx.Graph()
        for c in range(n_caves):
            l=[i for i in range(c*cave_size,cave_size*(c+1))]
            G_cave=self.new_complete_graph(l)
            G= nx.union(G,G_cave)
        for edg in G.edges():
            G[edg[0]][edg[1]]['intact']=True
        URE=[]
        for edg in G.edges():
            URE.append(edg)
        n_total = len(URE)
        #MS_rewiring
        iteration=0
        percent = 0.
        
        netsize=n_caves*cave_size
        g = open(str(netsize)+".txt",'w')
        saved=False
        p_saved=0
        while True:
            if saved == True and round(percent,3)*1000/50>p_saved:
                saved=False
            # whenever the percentage of ties have been rewired is at every 5% interval, the network structure will be saved as an adjcent matrix.
            if round(percent,3)*1000%50==0 and saved==False: 
                print round(percent,3), iteration
                
                cc= nx.average_clustering(G)
                #print iteration, nswap, cc
                g.write(str(round(percent,3)*100)+" "+str(cc)+"\n")
                Gc=G.copy()
                Gc=nx.DiGraph(Gc)
                f = open('MS_rewiring_'+str(netsize)+'_'+str(round(percent,2)*100)+'.txt','w')
                comments="# "+str(round(percent,3)*100)+" "+str(cc)+" "
                nx.write_adjlist(Gc, f, comments=comments)
                f.close()
                p_saved = round(percent,3)*1000/50
                saved = True
                
            connected=False

            
            edge1=random.choice(URE)
            URE.remove(edge1)
            neighbors = G.neighbors(edge1[0])+G.neighbors(edge1[1])+[edge1[0],edge1[1]]
            #print edge1
            while connected==False:
                iteration+=1
                edge2 = random.choice(G.edges())
                
                if (edge2[0] not in neighbors) and (edge2[1] not in neighbors):
                    connected=True
                    if random.random()<0.5:
                        G.add_edge(edge1[1],edge2[0], intact=False)
                        G.add_edge(edge1[0],edge2[1], intact=False)
                    else:
                        G.add_edge(edge1[1],edge2[1], intact=False)
                        G.add_edge(edge1[0],edge2[0], intact=False)
                    if G[edge2[0]][edge2[1]]['intact']==True:
                         URE.remove(edge2)
                    G.remove_edge(edge1[0],edge1[1])
                    G.remove_edge(edge2[0],edge2[1])

            n_intact = len(URE)-1
            percent = 1. - float(n_intact)/n_total
            
        g.close()
       	
        return G



network = access_network()
G = network.caveman_network(10,100) # will produce and save networks with 10 100-node caves with different levels of random rewiring at every 5% interval.


