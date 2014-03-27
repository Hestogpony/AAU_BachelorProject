# -*- coding: utf-8 -*-
import psycopg2
import re
import networkx as nx
from operator import itemgetter
from haversine import distance

class OSMLoader():
    def __init__(self,xmin,ymin,xmax,ymax):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.conn = self.connect()
        self.cur = self.conn.cursor()
        self.intersection = []

    def connect(self):
        return psycopg2.connect(database="osmgraph",port='5432', host='127.0.0.1', user="mikkel", password="syrlinger")

    def toGraph(self):
        self.graph = nx.DiGraph()
        self.cur.execute('select n1.id, n1.lat, n1.lon, n2.id, n2.lat, n2.lon, name  from nodes as n1, nodes as n2, edges where n1.id=node1 and n2.id=node2 and n1.lon between {0} and {1} and n2.lon between {0} and {1} and n1.lat between {2} and {3} and n2.lat between {2} and {3};'.format(self.xmin, self.xmax, self.ymin, self.ymax))
        nexttuple = self.cur.fetchone()

        while nexttuple is not None:
            dist = distance((float(nexttuple[1]),float(nexttuple[2])),(float(nexttuple[4]),float(nexttuple[5])))
            self.graph.add_edge(nexttuple[0],nexttuple[3],weight=dist, name=nexttuple[6])
            nexttuple = self.cur.fetchone()

def findpaths(G,s,d):
    paths = []
    for node in G.nodes():
        toNode = nx.shortest_path(G,s,node)
        fromNode = nx.shortest_path(G,node,d)
        paths.append(toNode.extend(fromNode))
    return paths


osmloader = OSMLoader(12.33619, 55.67397, 12.56292, 55.74944)
osmloader.toGraph()
print osmloader.graph.nodes()
import pylab
nx.draw(osmloader.graph) 
pylab.show()



# abe = nx.shortest_path(osmloader.graph, 118792, 1589573142, weight='weight')
# print findpaths(osmloader.graph, 118792, 1589573142)


