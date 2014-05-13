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
import fastest_path.roadnetwork
from fastest_path.loader import Loader
from fastest_path.haversine import distance

lonmin = 8.91
lonmax = 11.89
latmin = 55.46
latmax = 56.86

rn = roadnetwork.RoadNetwork(nx.read_gpickle('pickle_experiment'))

s_and_t(rn)

#rn.visualize()
def s_and_t(rn):
	node_count = rn.number_of_nodes()
	number = random.randint(1, node_count)
	print number

def bounding_box(lonmin,latmin,lonmax,latmax,rn):
	print rn.number_of_nodes()
	for node in rn.nodes():
		if not ((latmin <= float(rn.node[node]['lat']) <= latmax)\
		and (lonmin <= float(rn.node[node]['lon']) <= lonmax)):
			rn.remove_node(node)
	print rn.number_of_nodes()