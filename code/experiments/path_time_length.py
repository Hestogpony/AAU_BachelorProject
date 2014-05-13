"""
Bounding box on Denmark
Produce S and T with varying distance - 10km to something long
	Maybe use Dijkstra's on some S and then select a T with distance x
return the time spend driving every 10km
"""
import importer
import networkx as nx
import random
from fastest_path.naive import naive_path
from fastest_path.vehicle import EV
from fastest_path.roadnetwork import RoadNetwork

def s_and_t(rn, distance): #max distance 500km
	scrambled_nodes = rn.nodes()[:]
	random.shuffle(scrambled_nodes)
	for node in scrambled_nodes:
		#print node
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

rn = RoadNetwork(nx.read_gpickle('pickle_experiment'))

v = EV(80, 80, lambda x: ((0.04602*x**2 +  0.6591*x + 173.1174)* 10**(-3)))

for distance in range(1, 500):
	print 'finding s and t'
	s,t,dist = s_and_t(rn, distance)
	print 'finding a naive path'
	naive_p, naive_t = naive_path(rn, v, s, t)
	print 'from S:%s to T:%s - Distance:%sKm -  %shours'%(s,t,dist,naive_t)
	# run LP
	# run Greedy
