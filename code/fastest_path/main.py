# -*- coding: utf-8 -*-
import os
import time
import naive
import allsimplepathdist

#loader = loader.Loader()
#loader.create_graph(7.5256,54.4125,12.7881,57.6336) #aalborg
#loader.load_graph()
#G=loader.graph
#start = time.time()

#print len(G.nodes()), len(G.edges())
#P = nx.dijkstra_predecessor_and_distance(G,loader.street_node('Oxholmvej'), cutoff=None, weight='weight')

#shortpath = nx.shortest_path(G,loader.street_node('Oxholmvej'), loader.street_node('Naurve#j'), 'weight')
#cut = allsimplepathdist.path_time(G, shortpath)
#print cut
#p = allsimplepathdist.all_simple_paths(G,loader.street_node('Oxholmvej'), loader.street_node('Naurvej'), cutoff=cut)
#print P[0]
#print allsimplepathdist.path_time(G, p)


import networkx as nx
from loader import Loader
import vehicle
import roadnetwork
from rn_algorithms import fastest_path_greedy

def main():
    loader = Loader()
    loader.create_graph(7.9761,54.7627,10.5908,57.1482)
    loader.load_graph()
    road_network = loader.rn
    road_network.generate_charge(100, 150)
    rn = roadnetwork.RoadNetwork()
    rn.add_edge(1,2,weight=100, name="Edge 1", speed_limit=90, t=100.0/90.0)
    rn.add_edge(1,3,weight=51, name="Edge 2", speed_limit=70, t=50.0/90.0)
    rn.add_edge(3,2,weight=51, name="Edge 3", speed_limit=70, t=51.0/90.0)
    rn.generate_charge(100, 200)
    #rn.node[3]['charge_rate'] = 30
    print "1"

    print "2"
    #print road_network.edges()
    print road_network.nodes()[0]
    print road_network.nodes()[-1]
        #for edge in road_network.edges(data="True"):
        #if edge[2]['speed_limit'] == 130 or edge[2]['speed_limit'] == 110:
        #    print edge
    
        #  print nx.shortest_path(rn,1, 2,"t")
    s = loader.street_node('Fredrik Bajers Vej')
    road_network.node[s]['charge_rate'] = 20
    #nx.shortest_path(road_network, source=s, target=None, weight="t")
    print "3"
    path = fastest_path_greedy(road_network, s, loader.street_node('Pantheonsgade'), 1, 0, 80)
    print path
    road_network.visualize_path(path)
main()

'''
def shortest_path_through_all(G,s,t):
        shortest_paths = []
        for node in G.nodes():
            if node != s and node != t:
                try:
                    p = nx.shortest_path(G,s,node) + nx.shortest_path(G,node,t)
                    shortest_paths.append(p)
                except:
                    pass
        return shortest_paths

def fastest_path(G):
	pass
 
def timecalculator(edges=[]):
	pass
 
 
def BFS(G, s):
    loader = loader.Loader()
    loader.create_graph(9.972153,57.007566,10.005369,57.020594) ##aalborg øst
    loader.load_graph()
    G=loader.graph
    return nx.bfs_tree(G, s)
 
loader = Loader()
loader.create_graph(9.972153,57.007566,10.005369,57.020594) ##aalborg øst
loader.load_graph()
G=loader.graph
s = loader.street_node('Selma Lagerløfs Vej')
print BFS(G, s)
 
def CR(v):
	return v*v+v 

main()
'''
