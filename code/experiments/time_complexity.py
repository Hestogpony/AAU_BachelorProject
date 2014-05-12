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
import networkx as nx
import roadnetwork
from loader import Loader
from haversine import distance

lonmin = 8.91
lonmax = 11.89
latmin = 55.46
latmax = 56.86

rn = roadnetwork.RoadNetwork(nx.read_gpickle('pickle_experiment'))

def bounding_box(lonmin,latmin,lonmax,latmax,rn):
	print rn.number_of_nodes()
	for node in rn.nodes():
		if not ((latmin <= float(rn.node[node]['lat']) <= latmax)\
		and (lonmin <= float(rn.node[node]['lon']) <= lonmax)):
			rn.remove_node(node)
	print rn.number_of_nodes()

#rn.visualize()