import importer
import networkx as nx
import random
from path_time_cs_density import charge_station_density
from fastest_path.naive import naive_path
from fastest_path.vehicle import EV
from fastest_path.roadnetwork import RoadNetwork



def scale_charge_rates(rn, scale_factor):
	for n in rn:
		charge_rate = rn.node[n]['charge_rate']
		if charge_rate > 0:
			rn.node[n]['charge_rate'] = charge_rate * scale_factor

def s_and_t(rn, distance):
	scrambled_nodes = rn.nodes()[:]
	random.shuffle(scrambled_nodes)
	for node in scrambled_nodes:
		i = 0
		distances = nx.single_source_dijkstra_path_length(rn, node, weight='weight')
		for vertex, path_dist in distances.items():
			if (distance * 1.01) > path_dist > (distance * 0.99):
				return node, vertex, path_dist

def scale_road_network(rn, scale_factor):
	print("scaling distancens by: " + str(scale_factor))
	for edge in rn.edges(data = True):
		new_dist = edge['weight'] * scale_factor
		edge['weight'] = new_dist


def charge_station_density(rn, dist):
	for node in rn.nodes():
		if (node in rn):
			if (rn.node[node]['charge_rate'] != 0):
				dists = nx.single_source_dijkstra_path_length(rn,node,cutoff=dist,weight='weight')
				for vertex,dval in dists.items():
					if vertex != node:
						rn.node[vertex]['charge_rate'] = 0

def scale_cons_rate(pct):
	evs = []
	for x in xrange(-pct,pct):
		multiplier = 1+(x/100.0)
		evs.append(EV(80, 80,lambda x, copy=multiplier: ((0.04602*x**2+0.6591*x+173.1174)*10**(-3))*copy))
	return evs


def experiment_driving_dist():
	print 'loading roadnetwork'
	rn = RoadNetwork(nx.read_gpickle('pickle_experiment'))

	print 'reducing cs density'
	charge_station_density(rn, 5)

	v = EV(80, 80, lambda x: ((0.04602*x**2 +  0.6591*x + 173.1174)* 10**(-3)))

	f = open('path_time_length(1-500).csv', 'a')
	f.writeline('dist,time,fail_rate')
	for distance in range(1, 500):
		sum_time, fails = 0,0
		for x in xrange(0,10)
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

		f.writeline('%s,%s,%s' % (distance, sum_time/10.0, fails/10.0))
	f.close()
