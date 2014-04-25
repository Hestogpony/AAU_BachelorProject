# -*- coding: utf-8 -*-
import networkx as nx
import vehicle
import naive
from loader import Loader

loader = Loader()
loader.create_graph(8.009,56.0843,11.1182,57.7979) # 7.43,54.47,12.94,57.74 <- danmark nord+midt -> 8.009,56.0843,11.1182,57.7979  
loader.load_graph()
road_network = loader.rn
road_network.generate_charge(10,20)
v = vehicle.ElectricalVehicle(80, 80)

print 'graph loaded'
#bfs = nx.bfs_edges(road_network,loader.street_node('Selma Lagerløfs Vej'))
path = naive.naive_path(road_network, v, loader.street_node('Brettevillesgade'), loader.street_node('Bethaniagade'))
print path