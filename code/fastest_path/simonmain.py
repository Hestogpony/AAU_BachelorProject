
# -*- coding: utf-8 -*-
from vehicle import EV
import rn_algorithms
import time
from roadnetwork import RoadNetwork
import networkx as nx
from experiments import test_utils

def main():
    
    tesla = EV(80, 80, lambda speed: ((0.04602*speed**2 +  0.6591*speed + 173.1174)* 10**(-3)))
    
    print 'loading road network'
    road_network = RoadNetwork(nx.read_gpickle('pickle_experiment'))
    print 'done'
    
    s = road_network.street_node('Fredrik Bajers Vej')
    t = road_network.street_node('Pantheonsgade')
    
    print 'setting charge station density'
    test_utils.charge_station_density(road_network, 30)
    print 'done'
    
    print 'visualizing road network'
    road_network.visualize()
    road_network.visualize_nodes([s, t])

    #path = get_navie_path(road_network, s, loader.street_node('Pantheonsgade'), tesla)
    #road_network.visualize_path(path)
    
    start_time = time.time()
    print 'calculating fastest path'
    path, totaltime = rn_algorithms.fastest_path_greedy(road_network, s, t, 1, tesla)
    end_time = time.time()
    print(path, totaltime)
    road_network.visualize_path(path)
    print "time: ", end_time - start_time, " seconds to find greedy path"
   
main()

