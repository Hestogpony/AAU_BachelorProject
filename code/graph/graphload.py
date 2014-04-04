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
        self.graph = nx.Graph()
        self.cur.execute('select n1.id, n1.lat, n1.lon, n2.id, n2.lat, n2.lon, name  from nodes as n1, nodes as n2, edges where n1.id=node1 and n2.id=node2;')
        nexttuple = self.cur.fetchone()

        while nexttuple is not None:
            dist = distance((float(nexttuple[1]),float(nexttuple[2])),(float(nexttuple[4]),float(nexttuple[5])))
            self.graph.add_edge(nexttuple[0],nexttuple[3],weight=dist, name=nexttuple[6])
            nexttuple = self.cur.fetchone()



osmloader = OSMLoader(9.931589,57.014727,10.013458,57.049189)
osmloader.toGraph()
from time import sleep
for a in abe:
    print a
    sleep(0.01)


