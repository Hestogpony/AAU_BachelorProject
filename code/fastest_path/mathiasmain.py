# -*- coding: utf-8 -*-
import networkx as nx
import vehicle
import naive
import roadnetwork
from loader import Loader

loader = Loader()
loader.create_graph(7.5256,54.4125,12.7881,57.6336) #Aalborg
loader.load_graph()

roadnetwork = loader.rn
roadnetwork.generate_charge(10,20)
v = vehicle.ElectricalVehicle(80, 80)

print 'graph loaded'
path = naive.naive_path(roadnetwork, v, loader.street_node('Humlebakken'), loader.street_node('Algade'))