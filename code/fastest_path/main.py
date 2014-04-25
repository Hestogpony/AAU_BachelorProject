# -*- coding: utf-8 -*-
import os
import time
import networkx as nx
from loader import Loader
import vehicle
from rn_algorithms import fastest_path_greedy




def main():
    loader = Loader()
    loader.create_graph(9.95842,57.007187,10.002193,57.022981)
    loader.load_graph()
    road_network = loader.rn
    road_network.generate_charge(10, 20)
    G = nx.connected_components(road_network)
    for node in road_network.nodes():
        if node not in G[0]:
            road_network.remove_node(node)
                #print nx.shortest_path(road_network, road_network.nodes()[0], road_network.nodes()[-1])
    
    for e in road_network.edges():
        if e[0] == e[1]:
            road_network.remove_edge(e[0], e[1])

    print road_network.edges()
    print road_network.nodes()[0]
    print road_network.nodes()[-1]
    for e in road_network.edges([1394577375L], data=True):
        print e
    
    fastest_path_greedy(road_network,road_network.nodes()[0], road_network.nodes()[-1], 0)
#road_network.visualize_roadnetwork()
    
    #===========================================================================
    # print len(G.nodes()), len(G.edges())
    # p = shortest_path_through_all(G,loader.street_node('Selma LagerlÃ¸fs Vej'), loader.street_node('Niels Bohrs Vej'))
    # for x in xrange(1,10):
    #     print p[x]
    # print len(p)
    #===========================================================================
    
main()

    
