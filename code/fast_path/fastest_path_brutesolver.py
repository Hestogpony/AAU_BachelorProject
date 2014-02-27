#!/usr/bin/env python
#coding: UTF-8
import networkx as nx
from time import sleep

class Vehicle():
	def __init__(self, max_capacity, current_energy, kmpkwh):
		self.max_capacity=max_capacity
		self.current_energy=current_energy
		self.kmpkwh=kmpkwh

def bruteforce_fastest_path(G, s, t, vehicle):
	"""returns the fastest path in directed graph G, from s to t, given a vehicle"""
	path_generator = nx.all_simple_paths(G, s, t)
	path_times = []
	for P in path_generator:
		path_times.append(fast_path(G,P,v))
	return max(path_times)

def path_length(G, P):
	"""returns the length of the path"""
	return sum([G[P[x]][P[(x+1)]]['weight'] for x in xrange(len(P)-1)])

def path_time(G, P):
	"""returns the time spent travelling the path P given """
	return sum([(G[P[x]][P[(x+1)]]['weight'])*1.0/(G[P[x]][P[(x+1)]]['speed_limit']) for x in xrange(len(P)-1)])


def max_charge_node(G, nodes):
	"""returns the node containing the best charging station given a list of nodes"""
	max_charge = 0
	result= ''
	for vtx in nodes:
		if G.node[vtx]['charge'] > max_charge:
			max_charge = G.node[vtx]['charge']
			result = vtx
	return result

def optimal_path_traversal(G, P, vehicle):
	"""returns the optimal path traversal time given a path P and a vehicle v"""
	s = P[1]
	t = P[-1]
	time_spent_driving =  path_time(G,P)
	time_spent_charging = 0
	path_left = P[:]

	current_energy = v.current_energy
	charge_amount = 0
	next_node = path_left[0]	
	print
	print 'Path is:' + str(P)	
	while path_left[0] is not t:
		max_reach = reachable_nodes(G,path_left,v, v.max_capacity)
		current_reach = reachable_nodes(G,path_left,v, current_energy)
		print 'Path left:' + str(path_left)
		if current_energy == v.max_capacity:
			next_node = max_charge_node(G, max_reach)
			current_energy = current_energy - (path_length(G, path_left[0:path_left.index(next_node)+1]) / (v.kmpkwh * 1.0))
			path_left = path_left[path_left.index(next_node):]
			print 'Full energy, I drove to %s' % next_node
		elif current_reach and max_charge_node(G, current_reach) != path_left[0]:
			next_node = max_charge_node(G, current_reach)
			current_energy = current_energy - (path_length(G, path_left[0:path_left.index(next_node)+1]) / (v.kmpkwh * 1.0))
			path_left = path_left[path_left.index(next_node):]
			print 'I drove to charge station %s' % next_node
		else: # Bedste reachable ladestation er nuværende node:
			next_node = max_charge_node(G, max_reach)
			energy_needed = (path_length(G, path_left[0:path_left.index(next_node)+1])  / v.kmpkwh )
			charge_amount = energy_needed - current_energy
			time_spent_charging += charge_amount / G.node[next_node]['charge'] * 1.0
			print 'I needed %s energy to reach %s with my current battery of %s i need to charge %s' % (energy_needed, next_node, current_energy, charge_amount)


			current_energy += charge_amount
			# print 'I needed %s energy to reach %s with my current battery of %s i need to charge %s' % (energy_needed, next_node, current_energy, charge_amount)


	return (time_spent_charging + time_spent_driving)

def reachable_nodes(G, P, v, energy): 
	"""returns subpath of P of reachable nodes given energy"""
	result = []	
	edge_distance = 0
	for x in xrange(len(P)-1): # for each edge
		edge = G[P[x]][P[(x+1)]]
		edge_distance += edge['weight']		
		if (edge_distance/v.kmpkwh) <= energy:
			result.append(P[x+1])
		else:
			break
	return result
			
def example():
	v = Vehicle(max_capacity=80, current_energy=40, kmpkwh=5)
	G=nx.DiGraph()#Weight=tid

	#Ladestationer
	G.add_node('s', charge=5.0)
	G.add_node('1', charge=1.0)
	G.add_node('2', charge=3.0)
	G.add_node('3', charge=2.0)
	G.add_node('t', charge=9999)
	#Roads
	G.add_edge('s','1',weight=200, speed_limit=20)
	G.add_edge('s','3',weight=50, speed_limit=30)
	G.add_edge('1','3',weight=70, speed_limit=30)
	G.add_edge('3','2',weight=80, speed_limit=60)
	G.add_edge('1','2',weight=50, speed_limit=30)
	G.add_edge('2','t',weight=110, speed_limit=49)
	G.add_edge('3','t',weight=130, speed_limit=30)

	print fastest_path(G, 's', 't', v)










