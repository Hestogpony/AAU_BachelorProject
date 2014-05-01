# -*- coding: utf-8 -*-
import networkx as nx
import vehicle
import naive
import roadnetwork
from loader import Loader

loader = Loader()
loader.create_graph(7.43,54.47,12.94,57.74) 
loader.load_graph()

roadnetwork = loader.rn
roadnetwork.generate_charge(10,20)
v = vehicle.ElectricalVehicle(80, 80)

print 'graph loaded'
path = naive.naive_path(roadnetwork, v, loader.street_node('Brettevillesgade'), loader.street_node('Bethaniagade'))