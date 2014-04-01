# -*- coding: utf-8 -*-
import psycopg2
import re
import networkx as nx
from operator import itemgetter
from haversine import distance
from time import sleep

class OSMLoader():
    def __init__(self,lonmin,latmin,lonmax,latmax):
        self.lonmin = lonmin
        self.lonmax = lonmax
        self.latmin = latmin
        self.latmax = latmax
        self.conn = self.connect()
        self.cur = self.conn.cursor()
        self.intersection = []

    def connect(self):
        return psycopg2.connect(database="osmgraph",port='5432', host='127.0.0.1', user="mikkel", password="syrlinger")

    def toGraph(self):
        self.graph = nx.Graph()
        self.cur.execute('select n1.id, n1.lat, n1.lon, n2.id, n2.lat, n2.lon, name  from nodes as n1, nodes as n2, edges where n1.id=node1 and n2.id=node2 and n1.lon between {0} and {1} and n2.lon between {0} and {1} and n1.lat between {2} and {3} and n2.lat between {2} and {3};'.format(self.lonmin, self.lonmax, self.latmin, self.latmax))
        nexttuple = self.cur.fetchone()

        while nexttuple is not None:
            dist = distance((float(nexttuple[1]),float(nexttuple[2])),(float(nexttuple[4]),float(nexttuple[5])))
            self.graph.add_edge(nexttuple[0],nexttuple[3],weight=dist, name=nexttuple[6])
            nexttuple = self.cur.fetchone()

    def roadname_from_id(self, id):
        pass

def findpaths(G,s,d):
    paths = []
    for node in G.nodes():
        try:
            toNode = nx.shortest_path(G,s,node)
            fromNode = nx.shortest_path(G,node,d)
            paths.append(toNode.extend(fromNode))
        except:
            osmloader.graph.remove_node(node)
    return paths


osmloader = OSMLoader(12.422791,55.571746,12.702255,55.742187)
osmloader.toGraph()
G=osmloader.graph

print len(nx.all_simple_paths(G,331138613,92920533))

# bfs =  nx.bfs_tree(G,1736564314)  8086156L,2190257445L




# print osmloader.graph.nodes()
#for e in osmloader.graph.edges():
#    print e, osmloader.graph[e[0]][e[1]]['name']
