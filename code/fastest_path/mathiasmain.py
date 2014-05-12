# -*- coding: utf-8 -*-
import networkx as nx
from vehicle import EV
import naive
import roadnetwork
from loader import Loader

loader = Loader()
loader.create_graph(7.9761,54.7627,10.5908,57.1482)
loader.load_graph()
roadnetwork = loader.rn
roadnetwork.generate_charge(10,20)
v = EV(80, 80, lambda x: ((0.04602*x**2 +  0.6591*x + 173.1174)* 10**(-3)))

print 'graph loaded'
roadnetwork.visualize()

print 'driving from %s to %s' %(loader.street_node('Fredrik Bajers Vej'), loader.street_node('Pantheonsgade'))
path, time = naive.naive_path(roadnetwork, v, loader.street_node('Fredrik Bajers Vej'), loader.street_node('Pantheonsgade'))

print path, time
roadnetwork.visualize_path(path)
