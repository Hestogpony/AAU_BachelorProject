# -*- coding: utf-8 -*-
import networkx as nx
import vehicle
import naive
import roadnetwork
from loader import Loader

loader = Loader()
loader.create_graph(8.3965,55.1256,9.8402,56.4818)
loader.load_graph()
roadnetwork = loader.rn
roadnetwork.generate_charge(10,20)
v = vehicle.ElectricalVehicle(80, 80)

print 'graph loaded'
roadnetwork.visualize()
print 'driving from %s to %s' %(loader.street_node('Prins Buris Vej'), loader.street_node('Lænkebjerg'))
path, time = naive.naive_path(roadnetwork, v, loader.street_node('Prins Buris Vej'), loader.street_node('Lænkebjerg'))
print path, time
roadnetwork.visualize_path(path)