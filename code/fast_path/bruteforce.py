#!/usr/bin/env python
#coding: UTF-8
from networkx import all_simple_paths
from path_utils import optimal_path_traversal
def fastest_path(G, s, t, v):
	"""returns the fastest path in directed graph G, from s to t, given a vehicle"""
	path_generator = all_simple_paths(G, s, t)
	path_times = []
	for P in path_generator:
		path_times.append(optimal_path_traversal(G,P,v))
	return max(path_times)
