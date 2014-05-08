# -*- coding: utf-8 -*-
import networkx as nx
import vehicle
import naive
import roadnetwork
from loader import Loader

loader = Loader()
loader.create_graph(9.913101,57.038115,9.965286,57.052682) # fucking Aalborg
loader.load_graph()

roadnetwork = loader.rn
roadnetwork.generate_charge(10,20)
v = vehicle.ElectricalVehicle(80, 80)

print 'graph loaded'
print 'driving from %s to %s' %(loader.street_node('Danmarksgade'), loader.street_node('Læsøgade'))
path, time = naive.naive_path(roadnetwork, v, loader.street_node('Danmarksgade'), loader.street_node('Læsøgade'))
print path, time