# -*- coding: utf-8 -*-
import importer
import networkx as nx
from fastest_path.haversine import distance
from fastest_path.roadnetwork import RoadNetwork
from fastest_path.loader import Loader

loader = Loader()
loader.create_graph(7.91,54.46,12.89,57.86) #Danmark
loader.load_graph()
rn = loader.rn
rn.generate_charge(10,100,1)

print 'graph loaded'
#rn.visualize()

nx.write_gpickle(rn, "pickle_experiment")

#rn = roadnetwork.RoadNetwork(nx.read_gpickle('picle_experiment2'))
#rn.visualize()
