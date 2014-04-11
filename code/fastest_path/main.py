import loader
import networkx as nx
import os

loader = loader.Loader()   
loader.create_graph(12.422791,55.571746,12.702255,55.742187)
loader.load_graph()
G=loader.graph
p = nx.shortest_path(G,loader.street_node('Elmegade'), loader.street_node('Kristianiagade'))
loader.visualize_path(p)