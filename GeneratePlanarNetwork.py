#!/usr/bin/env python
# coding: utf-8

# In[1]:


import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np
from operator import itemgetter


# In[2]:


def modification(graph, leng, delete=True):
    
    if delete:
        edges = list(graph.edges)
        chosen_edge = random.choice(edges)
        graph.remove_edge(chosen_edge[0], chosen_edge[1])
        
    else:
        nonedges = list(nx.non_edges(graph))
        chosen_nonedge = random.choice(nonedges)
        graph.add_edge(chosen_nonedge[0], chosen_nonedge[1],len=leng)
        b,f = nx.check_planarity(graph)
        if not b:
            graph.remove_edge(chosen_nonedge[0], chosen_nonedge[1])
    
    return graph


# In[55]:


N=15   # number of nodes
E=20

def create_graph(N,E):
    G=nx.Graph()
    G.add_nodes_from(np.arange(N))
    G_nodes=list(G.nodes())
    
    mu, sigma = 40., 1.5 # mean and standard deviation

    link_lengths = np.random.lognormal(mu, sigma, E)
    
    for i in range(E):
        G.add_edge(random.choice(G_nodes), random.choice(G_nodes), len=link_lengths[i] )

        
    b = False
    while not b:
        G = modification(G, mu,delete=True)
        b,f = nx.check_planarity(G)

    G.remove_nodes_from(list(nx.isolates(G)))
    # Delete non-edges

    b = False
    for i in range(len(G.nodes)):
        G = modification(G, mu, delete=False)

        
    nx.draw(G, with_labels=True, font_weight='bold')

    print("Is planar - ",nx.check_planarity(G))
    
    return G


# In[73]:



def lst_to_dict(lst): 
    res_dct = {lst[i][0]: lst[i][1] for i in range(0, len(lst), 1)} 
    return res_dct 

locations_distribution=[0.35,0.45,0.2]  # 45% of locations are hubs, 35% - conflict zones, 20 % camps

# Assign location type as attributes:
G=create_graph(N,E)
def location_types(graph=G, distr=locations_distribution):
    
    dict={}
    
    degree_dict = lst_to_dict(list(G.degree))
    
    sorted_degree_dict = sorted(degree_dict.items(), key=itemgetter(1), reverse=True)
    
    L=len(sorted_degree_dict)
    
    for i in range(L):
        
        if i in np.arange(0,round(L*distr[0]),1):
            dict[sorted_degree_dict[i][0]]="Conflict zone"

        if i in np.arange(round(L*distr[0]),round(L*distr[0])+round(L*distr[1]),1):
            dict[sorted_degree_dict[i][0]]="Hub"

        if i in np.arange(round(L*distr[0])+round(L*distr[1]),L,1):
            dict[sorted_degree_dict[i][0]]="Camp"
        
    nx.set_node_attributes(G, dict, "Location_type" )
                          
    return G


# In[74]:


G=create_graph(N,E)
G2=location_types(graph=G, distr=locations_distribution)


# #ADD colours by attributes 

# In[75]:


node_color = []
# for each node in the graph
for node in G.nodes(data=True):

    # if the node has the attribute group1
    if 'Hub' in node[1]['Location_type']:
        node_color.append('yellow')

    # if the node has the attribute group1
    elif 'Camp' in node[1]['Location_type']:
        node_color.append('green')

    # if the node has the attribute group1
    elif 'Conflict zone' in node[1]['Location_type']:
        node_color.append('red')

 


# In[76]:


nx.draw(G2, with_labels=False,  font_weight='bold', node_color=node_color)
plt.savefig("graph1")

