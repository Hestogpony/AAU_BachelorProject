"""
some text
"""
import importer
import networkx as nx
import fastest_path.roadnetwork
from fastest_path.roadnetwork import RoadNetwork
from fastest_path.vehicle import EV

import time

def scale_cons_rate(pct):
    """
     Scales consumption rate of teslas cons rate  by -pct to pct in steps of 1
     e.g. 40%: scale_cons_rate(40)
     returns: 80 EV objects
    """
    evs = []
    for x in xrange(-pct,pct):
        multiplier = 1+(x/100.0)
        evs.append(EV(80, 80,lambda x, copy=multiplier: ((0.04602*x**2+0.6591*x+173.1174)*10**(-3))*copy))
    return evs
