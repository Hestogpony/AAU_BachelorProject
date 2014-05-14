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
from path_time_cs_density import charge_station_density
from fastest_path.haversine import distance
from fastest_path.roadnetwork import RoadNetwork

rn = RoadNetwork(nx.read_gpickle('pickle_experiment'))
charge_station_density(rn,25)

def set_roadnetwork_complexity(rn, num_nodes):
	lonmax = 12.89
	#latmax = 57.86
	connected_components = nx.connected_components(rn)	
	sorted(connected_components, key=len)
	
	while len(connected_components[0]) > num_nodes:
		
		print(len(connected_components[0]))
		#latmax -= 0.02
		lonmax -= 0.02
		for node in rn.nodes():
			if (float(rn.node[node]['lon']) >= lonmax):
				rn.remove_node(node)
		connected_components = nx.connected_components(rn)	
		sorted(connected_components, key=len)
		
	for list_of_nodes in connected_components[1:]:
		for node in list_of_nodes:
			rn.remove_node(node)
	return rn




