"""
Bounding box on Denmark
Produce S and T with varying distance - 10km to something long
	Maybe use Dijkstra's on some S and then select a T with distance x
return the time spend driving every 10km
"""
import importer
import networkx as nx
import random
from path_time_cs_density import charge_station_density
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

print 'loading roadnetwork'
rn = RoadNetwork(nx.read_gpickle('pickle_experiment'))

print 'reducing cs density'
charge_station_density(rn, 40)

v = EV(80, 80, lambda x: ((0.04602*x**2 +  0.6591*x + 173.1174)* 10**(-3)))

f = open('path_time_length(1-500).csv', 'a')
f.write('dist,time\n')
f.close()
for distance in range(1, 500):
	x = 0
	while x <= 10:
		s,t,dist = s_and_t(rn, distance)
		naive_p, naive_t = naive_path(rn, v, s, t)
		if naive_t == 'inf':
			f = open('path_time_length(1-500).csv', 'a')
			f.write('%s,%s\n' % (distance,naive_t))
			f.close()
		# run LP
		# run Greedy
		else:
			sum_time = naive_t
			x += 1
			print 'From S:%s to T:%s - Distance:%sKm +-%s - %shours'%(s,t,distance,abs(distance-dist),naive_t)
	avg_time = sum_time/10
	print avg_time
	f = open('path_time_length(1-500).csv', 'a')
	f.write('%s,%s\n' % (distance,naive_t))
	f.close()
