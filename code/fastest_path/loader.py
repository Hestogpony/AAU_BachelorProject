# -*- coding: utf-8 -*-
from haversine import distance

import psycopg2
import roadnetwork
import networkx as nx

class Loader():
    def __init__(self):
        self.conn = psycopg2.connect(database="osmgraph",port='5432', host='172.31.250.5', user="d609f14", password="cocio")
        self.cur = self.conn.cursor()

    def remove_unconnected(self):
        G = nx.connected_components(self.rn)
        for node in self.rn.nodes():
            if node not in G[0]:
                self.cur.execute('delete from edges where node1 = %s or node2 = %s' %(node,node))
                self.cur.execute('delete from nodes where id = %s' % (node))
        self.conn.commit()

    def create_graph(self,lonmin,latmin,lonmax,latmax):
        self.lonmin = lonmin
        self.lonmax = lonmax
        self.latmin = latmin
        self.latmax = latmax
        self.rn = roadnetwork.RoadNetwork()

    def load_graph(self):
        self.cur.execute('select n1.id, n1.lat, n1.lon, n2.id, n2.lat, n2.lon, name, roadtype  from nodes as n1, nodes as n2, edges where n1.id=node1 and n2.id=node2 and n1.lon between {0} and {1} and n2.lon between {0} and {1} and n1.lat between {2} and {3} and n2.lat between {2} and {3};'.format(self.lonmin, self.lonmax, self.latmin, self.latmax))
        nexttuple = self.cur.fetchone()
        while nexttuple is not None:
            dist = distance((float(nexttuple[1]),float(nexttuple[2])),(float(nexttuple[4]),float(nexttuple[5])))
            self.rn.add_edge(nexttuple[0],nexttuple[3],weight=dist, name=nexttuple[6], speed_limit=self.find_speed_limit(nexttuple[7]), t=dist/self.find_speed_limit(nexttuple[7]))
            self.rn.node[nexttuple[0]]['lon'] = str(nexttuple[2])
            self.rn.node[nexttuple[0]]['lat'] = str(nexttuple[1])
            self.rn.node[nexttuple[3]]['lon'] = str(nexttuple[5])
            self.rn.node[nexttuple[3]]['lat'] = str(nexttuple[4])
            nexttuple = self.cur.fetchone()

    def street_node(self,street):
        return [n[0] for n in self.rn.edges_iter(data=True) if n[2]['name'] == street][0]

    def node_street_path(self, p):
        return [self.node_street(n) for n in p]

    def find_speed_limit(self, road_type):
            if road_type == "living_street":
                return 50
            elif road_type == "motorway":
                return 130
            elif road_type == "motorway_link":
                return 80
            elif road_type == "passing_place":
                return 80
            elif road_type == "primary":
                return 80
            elif road_type == "primary_link":
                return 80
            elif road_type == "residential":
                return 50
            elif road_type == "road":
                return 50
            elif road_type == "secondary":
                return 80
            elif road_type == "secondary_link":
                return 80
            elif road_type == "tertiary":
                return 80
            elif road_type == "tertiary_link":
                return 80
            elif road_type == "track":
                return 30
            elif road_type == "trunk":
                return 80
            elif road_type == "trunk_link":
                return 80
            else:
                return 50
