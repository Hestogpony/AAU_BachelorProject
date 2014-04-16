# -*- coding: utf-8 -*-
from loader import Loader
import vehicle
from rn_algorithms import *



def main():
    loader = Loader()
    loader.create_graph(9.667917,56.928277,10.205032,57.168636)  
    loader.load_graph()
    road_network = loader.rn
    road_network.generate_charge(10, 20)
    fastest_path_greedy(road_network,road_network.nodes()[0], 0)

main()
    