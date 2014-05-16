# -*- coding: utf-8 -*-
import networkx as nx
from vehicle import EV
import naive
import roadnetwork
from loader import Loader
import time

loader = Loader()
loader.create_graph(7.96,54.55,12.93,57.81)
loader.load_graph()
rn = loader.rn
rn.generate_charge(10,20, 500)
v = EV(80, 80, lambda x: ((0.04602*x**2 +  0.6591*x + 173.1174)* 10**(-3)))

s = loader.street_node('Fredrik Bajers Vej')
t = loader.street_node('Simmerstedvej')
rn.node[s]['charge_rate'] = 20

#print 'graph loaded'
#rn.visualize()

print 'driving from ', s, ' to ', t
start_time = time.time()
path, pathtime = naive.naive_path(rn, v, s, t)
end_time = time.time()
print("time: ", end_time - start_time, " seconds to find naive path")
print path, pathtime
rn.visualize_path(path)
