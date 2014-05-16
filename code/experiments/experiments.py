import importer
import networkx as nx
from fastest_path.naive import naive
from fastest_path.vehicle import EV
from fastest_path.roadnetwork import RoadNetwork
from fastest_path.rn_algorithms import fastest_path_greedy
from test_utils import *
import time


def experiment_cs_density(ev, num_iterations, path_distance):
	file_name = 'cs_density_dist1-100km_path100_itt10.csv'
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
		for iteration in range(0, num_iterations):
			s, t, dist = s_and_t(rn, path_distance)
			
			### naive
			print 'running naive'
			naive_p, naive_t = naive_path(rn, ev, s, t)
			if naive_t == float('inf'):
				fails += 1
				print 'fail'
			else:
				sum_of_time_naive += naive_t
				print 'CS dist:%s - Hours:%s'%(cs_dist, naive_t)
			

			### LP

			### Greedy
			print 'running Greedy'
			greedy_path = fastest_path_greedy(rn, s, t, 1, ev)
			
		print 'CS dist:%s - Hours:%s - Fail rate:%s'%(cs_dist, sum_of_time_naive/num_iterations, fails/num_iterations)
		f.write('%s,%s,%s\n' % (cs_dist, sum_of_time_naive/num_iterations, fails/num_iterations))
		f.close()			

def experiment_runtime_compexity(ev, num_iterations, num_experiments, path_distance, CS_density):
	print 'loading graph'
	rn = RoadNetwork(nx.read_gpickle('pickle_experiment'))
	print 'reducing charge stations'
	charge_station_density(rn, CS_density)
	#rn.visualize()
	number_of_nodes = 500000
	iteration_size = number_of_nodes/num_experiments
	
	file_name = 'complexity_size500k_itt100_csd40.csv'
	f = open(file_name, 'a')
	f.write('problem size,time\n')
	f.close()

	while number_of_nodes > 0:
		rn, real_num_nodes = set_roadnetwork_complexity(rn, number_of_nodes)
		f = open(file_name, 'a')
		dijkstra_time_sum = 0
		greedy_time_sum = 0
		for x in range(1, num_iterations+1):
			s,t,dist = s_and_t(rn, path_distance)
		
			### Dijksras
			print 'running Dijkstras'
			start_time = time.time()
			nx.single_source_dijkstra_path_length(rn, s, weight='weight')
			dijkstra_time_sum += time.time() - start_time
			#if greedy_return[1] == float('inf'):
			### LP

			### Greedy
			print 'running greedy'
			start_time = time.time()
			greedy_return = fastest_path_greedy(rn, s, t, 1, ev)
			if greedy_return[1] == float('inf'):
				print 'greedy returns empty path'
			else:
				print greedy_return[1]
				rn.visualize_path(greedy_return[0])
				greedy_time_sum += time.time() - start_time
			print '%s,%s,%s\n' % (real_num_nodes, dijkstra_time_sum, greedy_time_sum)
		f.write('%s,%s,%s\n' % (real_num_nodes, dijkstra_time_sum/num_iterations, greedy_time_sum/num_iterations))
		f.close()

		number_of_nodes -= iteration_size

def experiment_ev_consumption(num_iterations, path_distance, CS_density):
	### PARAMETERS ###
	con_variance_pct = 40
	file_name = 'ev_con_40pct_50km_10itt.csv'
	list_of_paths = []
	sum_of_time = 0
	fails = 0

	print 'loading graph'
	rn = RoadNetwork(nx.read_gpickle('pickle_experiment'))
	print 'reducing charge stations'
	charge_station_density(rn, CS_density)

	f = open(file_name, 'a')
	f.write('con pct,time,fail rate\n')
	f.close()

	print 'chosing paths'
	for x in range(0,num_iterations):
		s,t,dist = s_and_t(rn, path_distance)
		list_of_paths.append((s,t))	

	print 'generating evs'	
	list_evs = scale_cons_rate(con_variance_pct)

	ev_number = -con_variance_pct
	for ev in list_evs: #from -40pct to +40pct
		f = open(file_name, 'a')
		for path in list_of_paths:
			
			print 'running naive'	
			naive_p, naive_t = naive_path(rn, ev, path[0], path[1])

			if naive_t == float('inf'):
				fails += 1
				print 'fail'
			else:
				sum_of_time += naive_t
				print 'EV:%s - Hours:%s'%(ev_number, naive_t)
		print 'EV_number:%s - Hours:%s - Fail rate:%s'%(ev_number, sum_of_time/num_iterations, fails/num_iterations)
		f.write('%s,%s,%s\n' % (ev_number, sum_of_time/num_iterations, fails/num_iterations))
		ev_number += 1
		f.close()

			### LP
			### Greedy

def experiment_charge_rate(road_network, ev, CS_density, path_distance, charge_rate_variance):
	list_of_paths = []
	sum_of_time = 0
	naive_fails = 0
	print 'reducing charge stations'
	charge_station_density(road_network, CS_density)
	
	f = open('charge_rate(0.6-1.4).csv', 'a')
	f.write('scale factor,time\n')

	print 'chosing paths'
	for x in range(0,10):
		s,t,dist = s_and_t(road_network, path_distance)
		list_of_paths.append((s,t))	
		
	for scale_factor in range(-charge_rate_variance, charge_rate_variance):
		temp_rn = road_network
		scale_charge_rates(temp_rn, 1+(scale_factor/100.0))
		
		for path in list_of_paths:
			naive_p, naive_t = naive_path(temp_rn, ev, path[0], path[1])
			
			if naive_t == float('inf'):
				naive_fails += 1
				print 'fail'
			else:
				print path[0], path[1]
				sum_of_time += naive_t
				
		f.write('%s,%s\n' % (1+(scale_factor/100.0), sum_of_time/10))
		print 'Scale factor:%s - Hours:%s'%(1+(scale_factor/100.0), sum_of_time/10)
	f.close()

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

#experiment_cs_density(ev, 10, 100)

experiment_runtime_compexity(ev, 1, 100, 150, 40)

#experiment_ev_consumption(10, 100, 40)

#print 'loading road network'
#road_network = RoadNetwork(nx.read_gpickle('pickle_experiment'))
#experiment_charge_rate(road_network, ev, 10, 100, 50)

#experiment_driving_dist(ev, 20, 500)


