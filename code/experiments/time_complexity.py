"""
Generate bounding boxes of varying sizes - 10km to Denmark
Produce S and T vertice, at the edge of the problem - something like 100 times
Make sure two execusions generate the same results:
	Use the same bounding box and the same nodes as charge stations with the same charge speeds
return runtime

input box for denmark:
lonmin, latmin, lonmax, latmax
7.91 , 54.46 , 12.89 , 57.86
"""
import importer
import networkx as nx
from fastest_path.haversine import distance
from fastest_path.roadnetwork import RoadNetwork



def bounding_box(rn,lonmin,latmin,lonmax,latmax):
	print rn.number_of_nodes()
	for node in rn.nodes():
		if not ((latmin <= float(rn.node[node]['lat']) <= latmax)\
		and (lonmin <= float(rn.node[node]['lon']) <= lonmax)):
			rn.remove_node(node)
	print rn.number_of_nodes()


def scale_road_network(rn, scale_factor):
	print("scaling distancens by: " + str(scale_factor))
	for edge in rn.edges(data = True):
		new_dist = edge['weight'] * scale_factor
		edge['weight'] = new_dist

def charge_station_density(rn, dist):
	for node in rn.nodes():
		print nx.single_source_dijkstra(rn,node,cutoff=dist,weight='weight')
		break
g = nx.read_gpickle('pickle_experiment')


# rn = RoadNetwork()

# charge_station_density(rn,dist)
