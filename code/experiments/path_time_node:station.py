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

rn = RoadNetwork(nx.read_gpickle('pickle_experiment'))


def charge_station_density(rn, dist):
	for node in rn.nodes():
		print nx.single_source_dijkstra(rn,node,cutoff=dist,weight='weight')