#!/usr/bin/env python
#coding: UTF-8
from networkx import DiGraph
from bruteforce import fastest_path
from vehicle import Vehicle
v = Vehicle(max_capacity=80, current_energy=40, kmpkwh=5)

G=DiGraph()

#Ladestationer
G.add_node('s', charge=5.0)
G.add_node('1', charge=1.0)
G.add_node('2', charge=3.0)
G.add_node('3', charge=2.0)
G.add_node('t', charge=9999)

#Roads, weight=distance
G.add_edge('s','1',weight=200, speed_limit=20)
G.add_edge('s','3',weight=50, speed_limit=30)
G.add_edge('1','3',weight=70, speed_limit=30)
G.add_edge('3','2',weight=80, speed_limit=60)
G.add_edge('1','2',weight=50, speed_limit=30)
G.add_edge('2','t',weight=110, speed_limit=49)
G.add_edge('3','t',weight=130, speed_limit=30)


print fastest_path(G, 's', 't', v)
