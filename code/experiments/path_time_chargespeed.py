"""
Bounding box Denmark
Use multiple S and T's on multiple charge speeds. 
Based on existing charge stations, multiply or divide the charge speeds.
return path time
"""

import importer
import networkx as nx
import fastest_path.roadnetwork
from fastest_path.haversine import distance
from fastest_path.roadnetwork import RoadNetwork

rn = RoadNetwork(nx.read_gpickle('pickle_experiment'))