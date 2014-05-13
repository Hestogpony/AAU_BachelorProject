"""
Bounding box Denmark
Produce at least one S to one T
Remove 0 to 100 procent of charge stations
"""
import importer
import networkx as nx
import fastest_path.roadnetwork
from fastest_path.haversine import distance
from fastest_path.roadnetwork import RoadNetwork
import time

def charge_station_density(rn, dist):
	for node in rn.nodes():
		if (node in rn):
			if (rn.node[node]['charge_rate'] != 0):
				dists = nx.single_source_dijkstra_path_length(rn,node,cutoff=dist,weight='weight')
				for vertex,dval in dists.items():
					if vertex != node:
						rn.node[vertex]['charge_rate'] = 0