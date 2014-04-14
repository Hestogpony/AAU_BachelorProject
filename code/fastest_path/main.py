import loader
import networkx as nx
import os

loader = loader.Loader()   
loader.create_graph(6.02,53.7,14.99,57.96)
loader.load_graph()
G=loader.graph
p = nx.shortest_path(G,loader.street_node('Elmegade'), loader.street_node('Kristianiagade'))
loader.visualize_path(p)