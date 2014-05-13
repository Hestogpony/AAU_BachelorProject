"""
Bounding box on Denmark
Produce S and T with varying distance - 10km to something long
	Maybe use Dijkstra's on some S and then select a T with distance x
return the time spend driving every 10km
"""
import importer
import networkx as nx
import fastest_path.roadnetwork
from fastest_path.haversine import distance
from fastest_path.roadnetwork import RoadNetwork

rn = RoadNetwork(nx.read_gpickle('pickle_experiment'))

def s_and_t(rn):
	node_count = rn.number_of_nodes()
	number = random.randint(1, node_count)
	print number

def scale_road_network(rn, scale_factor):
	print("scaling distancens by: " + str(scale_factor))
	for edge in rn.edges(data = True):
		new_dist = edge['weight'] * scale_factor
		edge['weight'] = new_dist