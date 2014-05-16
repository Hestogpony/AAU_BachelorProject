import importer
import networkx as nx
from path_time_cs_density import charge_station_density
from fastest_path.naive import naive_path
from fastest_path.vehicle import EV
from fastest_path.roadnetwork import RoadNetwork
from fastest_path.rn_algorithms import fastest_path_greedy
from test_utils import *
import time

def experiment_cs_density():
	### PARAMETERS ###
	number_of_itterations = 10
	path_distance = 100 #km
	file_name = 'cs_density_dist1-100km_path100_itt10.csv'
	v = EV(80, 80, lambda x: ((0.04602*x**2 +  0.6591*x + 173.1174)* 10**(-3)))
	fails = 0

	f = open(file_name, 'a')
	f.write('CS dist,path time,fail rate\n')
	f.close()

	for cs_dist in range(0,100):
		print 'loading graph'
		rn = RoadNetwork(nx.read_gpickle('pickle_experiment'))
		print 'reducing charge stations'
		charge_station_density(rn, cs_dist)
		sum_of_time_naive = 0
		f = open(file_name, 'a')
		for itteration in range(0,number_of_itterations):
			s,t,dist = s_and_t(rn, path_distance)
			### naive
			print 'running naive'
			naive_p, naive_t = naive_path(rn, v, s, t)
			if naive_t == float('inf'):
				fails += 1
				print 'fail'
			else:
				sum_of_time_naive += naive_t
				print 'CS dist:%s - Hours:%s'%(cs_dist, naive_t)
			

			### LP

			### Greedy
		print 'CS dist:%s - Hours:%s - Fail rate:%s'%(cs_dist, sum_of_time_naive/number_of_itterations, fails/number_of_itterations)
		f.write('%s,%s,%s\n' % (cs_dist, sum_of_time_naive/number_of_itterations, fails/number_of_itterations))
		f.close()			




def experiment_runtime_compexity():
	### PARAMETERS ###
	itterations = 1
	print 'loading graph'
	rn = RoadNetwork(nx.read_gpickle('pickle_experiment'))
	print 'reducing charge stations'
	charge_station_density(rn, 40)
	path_distance = 200 #km
	number_of_experiments = 100
	number_of_nodes = rn.number_of_nodes()
	itteration_size = number_of_nodes/number_of_experiments
	file_name = 'complexity_size500k_itt100_csd40.csv'
	v = EV(80, 80, lambda x: ((0.04602*x**2 +  0.6591*x + 173.1174)* 10**(-3)))
	
	f = open(file_name, 'a')
	f.write('problem size,time\n')
	f.close()

	while number_of_nodes > 0:
		rn, real_num_nodes = set_roadnetwork_complexity(rn,number_of_nodes)
		f = open(file_name, 'a')
		dijkstra_time_sum = 0
		greedy_time_sum = 0
		for x in range(0, itterations):
			s,t,dist = s_and_t(rn, path_distance)
			print s, t
			print 'running Dijkstras'
			start_time = time.time()
			nx.single_source_dijkstra_path_length(rn, s, weight='weight')
			dijkstra_time_sum += time.time() - start_time
		
			### LP

			### Greedy
			print 'running greedy'
			start_time = time.time()
			greedy_return = fastest_path_greedy(rn, s, t, 1, v)
			if greedy_return[0]:
				greedy_time_sum += time.time() - start_time
			else:
				print 'greedy returns empty path'
		print '%s,%s,%s\n' % (real_num_nodes, dijkstra_time_sum/itterations, greedy_time_sum/itterations)
		f.write('%s,%s,%s\n' % (real_num_nodes, dijkstra_time_sum/itterations, greedy_time_sum/itterations))
		f.close()


		number_of_nodes -= itteration_size

def experiment_ev_consumption():
	### PARAMETERS ###
	number_of_itterations = 10
	path_distance = 50
	con_variance_pct = 40
	file_name = 'ev_con_40pct_50km_10itt.csv'
	list_of_paths = []
	sum_of_time = 0
	fails = 0

	print 'loading graph'
	rn = RoadNetwork(nx.read_gpickle('pickle_experiment'))
	print 'reducing charge stations'
	charge_station_density(rn, 40)

	f = open(file_name, 'a')
	f.write('con pct,time,fail rate\n')
	f.close()

	print 'chosing paths'
	for x in range(0,number_of_itterations):
		s,t,dist = s_and_t(rn, path_distance)
		list_of_paths.append((s,t))	

	print 'generating evs'	
	list_evs = scale_cons_rate(con_variance_pct)

	print 'running naive'	
	ev_number = -con_variance_pct
	for ev in list_evs: #from -40pct to +40pct
		f = open(file_name, 'a')
		for path in list_of_paths:
			naive_p, naive_t = naive_path(rn, ev, path[0], path[1])

			if naive_t == float('inf'):
				fails += 1
				print 'fail'
			else:
				sum_of_time += naive_t
				print 'EV:%s - Hours:%s'%(ev_number, naive_t)
		print 'EV_number:%s - Hours:%s - Fail rate:%s'%(ev_number, sum_of_time/number_of_itterations, fails/number_of_itterations)
		f.write('%s,%s,%s\n' % (ev_number, sum_of_time/number_of_itterations, fails/number_of_itterations))
		ev_number += 1
		f.close()

			### LP
			### Greedy

def experiment_charge_rate():
	list_of_paths = []
	sum_of_time = 0
	v = EV(80, 80, lambda x: ((0.04602*x**2 +  0.6591*x + 173.1174)* 10**(-3)))
	print 'loading graph'
	rn = RoadNetwork(nx.read_gpickle('pickle_experiment'))
	print 'reducing charge stations'
	charge_station_density(rn, 40)
	
	f = open('charge_rate(0.6-1.4).csv', 'a')
	f.write('scale factor,time\n')

	print 'chosing paths'
	for x in range(1,10):
		s,t,dist = s_and_t(rn, 50)
		list_of_paths.append((s,t))	

	print 'running naive'
	for scale_factor in range(1,40):
		scale_charge_rates(rn, 1+(scale_factor/100.0))
		for path in list_of_paths:
			naive_p, naive_t = naive_path(rn, v, path[0], path[1])
			print path[0], path[1]
			sum_of_time += naive_t
		f.write('%s,%s\n' % (1+(scale_factor/100.0), sum_of_time/10))
		print 'Scale factor:%s - Hours:%s'%(1+(scale_factor/100.0), sum_of_time/10)
	f.close()

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

#experiment_driving_dist()
#experiment_charge_rate()
#experiment_ev_consumption()
experiment_runtime_compexity()
#experiment_cs_density()


