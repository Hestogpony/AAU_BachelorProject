# -*- coding: utf-8 -*-
import networkx as nx
import vehicle
import naive
import roadnetwork
from loader import Loader

loader = Loader()
loader.create_graph(7.72,54.46,12.96,57.84) # fucking DANMARK
loader.load_graph()

roadnetwork = loader.rn
roadnetwork.generate_charge(10,20)
v = vehicle.ElectricalVehicle(80, 80)

print 'graph loaded'
roadnetwork.visualize()
print nx.shortest_path(roadnetwork,loader.street_node('Danmarksgade'), loader.street_node('Læsøgade'))
print 'driving from %s to %s' %(loader.street_node('Danmarksgade'), loader.street_node('Listedvej'))
path, time = naive.naive_path(roadnetwork, v, loader.street_node('Danmarksgade'), loader.street_node('Læsøgade'))
print path, time
roadnetwork.visualize_path(path)
