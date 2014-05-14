import importer
import networkx as nx
from path_time_cs_density import charge_station_density
from fastest_path.naive import naive_path
from fastest_path.vehicle import EV
from fastest_path.roadnetwork import RoadNetwork

from test_utils import *


def experiment_driving_dist():
	print 'loading roadnetwork'
	rn = RoadNetwork(nx.read_gpickle('pickle_experiment'))

	print 'reducing cs density'
	charge_station_density(rn, 5)

	v = EV(80, 80, lambda x: ((0.04602*x**2 +  0.6591*x + 173.1174)* 10**(-3)))

	f = open('path_time_length(1-500).csv', 'a')
	f.write('dist,time,fail_rate\n')
	for distance in range(1, 500):
		sum_time, fails = 0,0
		for x in xrange(0,10):
			s,t,dist = s_and_t(rn, distance)
			################ NAIVE
			naive_p, naive_t = naive_path(rn, v, s, t)
			if naive_t == float('inf'):
				fails += 1
			else:
				sum_time += naive_t
			################ GREEDY

			################ LP

			################


			print 'From S:%s to T:%s - Distance:%sKm +-%s - %shours'%(s,t,distance,abs(distance-dist),naive_t)

		f.write('%s,%s,%s\n' % (distance, sum_time/10.0, fails/10.0))
	f.close()
experiment_driving_dist()
