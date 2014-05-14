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

def scale_charge_rates(rn, scale_factor):
    for n in rn:
        charge_rate = rn.node[n]['charge_rate']
        if charge_rate > 0:
            rn.node[n]['charge_rate'] = charge_rate * scale_factor
            
