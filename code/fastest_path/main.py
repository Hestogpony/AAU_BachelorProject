# -*- coding: utf-8 -*-
from vehicle import EV
from naivedrol import get_navie_path
import math
import rn_algorithms
import inRange
import loader as LD
import time


def main():
    
    tesla = EV(80, 80, lambda speed: ((0.04602*speed**2 +  0.6591*speed + 173.1174)* 10**(-3)))
    #===========================================================================
    # 
    # tesla_worse = vehicle(40, 40, lambda speed: ((0.0350 * math.pow(speed, 2) + 0.8096 * speed + 107.57) * 10**(-3)))
    # tesla_better = vehicle(120, 120, lambda speed: ((0.0190 * math.pow(speed, 2) + 0.2096 * speed + 107.57) * 10**(-3)))
    # 
    # rn = roadnetwork.RoadNetwork()
    # rn.add_edge(1,2,weight=100, name="Edge 1", speed_limit=90, t=100.0/90.0)
    # rn.add_edge(1,3,weight=51, name="Edge 2", speed_limit=70, t=50.0/90.0)
    # rn.add_edge(3,2,weight=51, name="Edge 3", speed_limit=70, t=51.0/90.0)
    # rn.generate_charge(10, 20)
    # rn.node[3]['charge_rate'] = 30 
    # for node in rn.nodes(data="True"):
    #     print node
    #      
    # print nx.shortest_path(rn,1, 2,"t")
    #===========================================================================
    
    loader = LD.Loader()
    loader.create_graph(7.96,54.55,12.93,57.81)
    loader.load_graph()
    road_network = loader.rn

    road_network.generate_charge(10, 20, 500)

    print road_network.nodes()[0]
    print road_network.nodes()[-1]
    
    s = loader.street_node('Fredrik Bajers Vej')

    #print inRange.inRange(road_network, 308352913, loader.street_node('Pantheonsgade'), tesla)
    #road_network.node[s]['charge_rate'] = 20
    #nodes = inRange.inRange(road_network, s, loader.street_node('Pantheonsgade'), tesla)
    path = get_navie_path(road_network, s, loader.street_node('Pantheonsgade'), tesla)
    #print len(nodes)
#print len(road_network.nodes())
#path = rn_algorithms.fastest_path_greedy(road_network, s, loader.street_node('Pantheonsgade'), 1, tesla)
# print path
    road_network.visualize_path(path)
    '''t = loader.street_node('Simmerstedvej')
    road_network.node[s]['charge_rate'] = 20
    
    start_time = time.time()
    path, totaltime = rn_algorithms.fastest_path_greedy(road_network, s, t, 1, tesla)
    end_time = time.time()
    print(path, totaltime)
    road_network.visualize_path(path)
    print "time: ", end_time - start_time, " seconds to find greedy path"'''


main()

