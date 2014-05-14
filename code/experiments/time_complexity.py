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
from fastest_path.haversine import distance
from fastest_path.roadnetwork import RoadNetwork

rn = RoadNetwork(nx.read_gpickle('pickle_experiment'))

#charge_station_density(rn,5)

#rn.visualize()

def bounding_box(rn,lonmin,latmin,lonmax,latmax):
	print rn.number_of_nodes()
	for node in rn.nodes():
		if not ((latmin <= float(rn.node[node]['lat']) <= latmax)\
		and (lonmin <= float(rn.node[node]['lon']) <= lonmax)):
			rn.remove_node(node)
	print rn.number_of_nodes()
