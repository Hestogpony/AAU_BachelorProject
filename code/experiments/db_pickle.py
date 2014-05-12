# -*- coding: utf-8 -*-
import networkx as nx
import roadnetwork
from loader import Loader

loader = Loader()
loader.create_graph(7.91,54.46,12.89,57.86) #Danmark
loader.load_graph()
rn = loader.rn
rn.generate_charge(10,100)

print 'graph loaded'
#rn.visualize()

nx.write_gpickle(rn, "pickle_experiment")

#rn = roadnetwork.RoadNetwork(nx.read_gpickle('picle_experiment2'))
#rn.visualize()