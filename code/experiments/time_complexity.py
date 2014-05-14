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
from fastest_path.haversine import distance
from fastest_path.roadnetwork import RoadNetwork

rn = RoadNetwork(nx.read_gpickle('pickle_experiment'))

#charge_station_density(rn,5)

rn.visualize()

def set_box_size(rn, num_nodes):
	lonmin = 7.91
	latmin = 54.46
	lonmax = 12.89
	latmax = 57.86
	print("number of connected nodes: " + nx.connected_components(rn)) 	 
	while len(nx.connected_components(rn)) > num_nodes:
		latmax -= 0.02
		lonmax -= 0.02
		for node in rn.nodes():
			if not ((latmin <= float(rn.node[node]['lat']) <= latmax) or (lonmin <= float(rn.node[node]['lon']) <= lonmax)):
				rn.remove_node(node)
	return rn


#set_box_size(rn, 50000)
#rn.visualize()

