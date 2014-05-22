import importer
import networkx as nx
from fastest_path.naive import naive
from fastest_path.vehicle import EV
from fastest_path.roadnetwork import RoadNetwork
from fastest_path.rn_test import fastest_path_greedy
from test_utils import *
import time

def experiment_driving_dist(ev, CS_density, max_distance):
print 'loading roadnetwork'
rn = RoadNetwork(nx.read_gpickle('pickle_experiment'))

print 'reducing cs density'
charge_station_density(rn, CS_density)

f = open('path_time_length(1-500).csv', 'a')
f.write('dist,time,fail_rate\n')
for distance in range(1, max_distance, 50):
    naive_sum_time, greedy_sum_time, lp_sum_time, naive_fails, greedy_fails, lp_fails = 0,0,0,0,0,0
    for x in xrange(0,10):
s,t,dist = s_and_t(rn, distance)

################ NAIVE
naive_p, naive_t = naive_path(rn, ev, s, t)
if naive_t == float('inf'):
naive_fails += 1
else:
naive_sum_time += naive_t

################ GREEDY

if greedy_return == float('inf'):
greedy_fails += 1
else:
greedy_sum_time += greedy_return

################ LP

if lp_return == float('inf'):
lp_fails += 1
else:
lp_sum_time += lp_return

print 'From S:%s to T:%s - Distance:%sKm +-%s - %shours'%(s,t,distance,abs(distance-dist),naive_t)

f.write('%s,%s,%s,%s,%s,%s,%s\n' % (distance,
    naive_sum_time/10.0,
    naive_fails/10.0,
    greedy_sum_time/10.0,
    greedy_fails/10.0,
    lp_sum_time/10.0,
    lp_fails/10.0))
    f.close()

ev = EV(80, 80, lambda x: ((0.04602*x**2 + 0.6591*x + 173.1174)* 10**(-3)))

