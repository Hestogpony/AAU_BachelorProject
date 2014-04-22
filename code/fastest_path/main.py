# -*- coding: utf-8 -*-
import loader
import networkx as nx
import os
import time
import allsimplepathdist

loader = loader.Loader()   
loader.create_graph(7.5256,54.4125,12.7881,57.6336) #aalborg
loader.load_graph()
G=loader.graph
start = time.time()

print len(G.nodes()), len(G.edges())
P = nx.dijkstra_predecessor_and_distance(G,loader.street_node('Oxholmvej'), cutoff=None, weight='weight')

#shortpath = nx.shortest_path(G,loader.street_node('Oxholmvej'), loader.street_node('Naurve#j'), 'weight')
#cut = allsimplepathdist.path_time(G, shortpath)
#print cut
#p = allsimplepathdist.all_simple_paths(G,loader.street_node('Oxholmvej'), loader.street_node('Naurvej'), cutoff=cut)
print P[0]
#print allsimplepathdist.path_time(G, p)
print time.time() - start
print 'end'