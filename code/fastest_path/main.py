# -*- coding: utf-8 -*-

import networkx as nx
from loader import Loader
import roadnetwork
from rn_algorithms import fastest_path_greedy

def main():
    
#     rn = roadnetwork.RoadNetwork()
#     rn.add_edge(1,2,weight=100, name="Edge 1", speed_limit=90, t=100.0/90.0)
#     rn.add_edge(1,3,weight=51, name="Edge 2", speed_limit=70, t=50.0/90.0)
#     rn.add_edge(3,2,weight=51, name="Edge 3", speed_limit=70, t=51.0/90.0)
#     rn.generate_charge(10, 20)
#     rn.node[3]['charge_rate'] = 30 
#     for node in rn.nodes(data="True"):
#         print node
#         
#     print nx.shortest_path(rn,1, 2,"t")
    
    loader = Loader()
    loader.create_graph(7.9761,54.7627,10.5908,57.1482)
    loader.load_graph()
    road_network = loader.rn
    road_network.generate_charge(10, 20)
    
    print "1"
    print road_network.edges()
    print road_network.nodes()[0]
    print road_network.nodes()[-1]
  
    s = loader.street_node('Fredrik Bajers Vej')
    road_network.node[s]['charge_rate'] = 20
    nx.shortest_path(road_network, source=s, target=None, weight="t")
    
    print "2"
    path = fastest_path_greedy(road_network, s, loader.street_node('Pantheonsgade'), 1, 0, 80)
    road_network.visualize_path(path)
    
main()

