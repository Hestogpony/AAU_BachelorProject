# -*- coding: utf-8 -*-
import networkx as nx
import vehicle
import naive
import road_network
from loader import Loader

loader = Loader()
loader.create_graph(8.009,56.0843,11.1182,57.7979) # 7.43,54.47,12.94,57.74 <- danmark nord+midt -> 8.009,56.0843,11.1182,57.7979  
loader.load_graph()
road_network = loader.rn
road_network.generate_charge(10,20)
v = vehicle.ElectricalVehicle(80, 80)

print 'removing non-connected nodes'
G = nx.connected_components(road_network)
for node in road_network.nodes():
    if node not in G[0]:
	    road_network.remove_node(node

print 'graph loaded'
#bfs = nx.bfs_edges(road_network,loader.street_node('Selma Lagerløfs Vej'))
path = naive.naive_path(road_network, v, loader.street_node('Brettevillesgade'), loader.street_node('Bethaniagade'))
print path