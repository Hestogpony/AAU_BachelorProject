import os, sys
lib_path = os.path.abspath(__file__ +'/../../')
sys.path.append(lib_path)
import networkx as nx
import fastest_path.roadnetwork
from fastest_path.haversine import distance
from fastest_path.roadnetwork import RoadNetwork
import time
