# -*- coding: utf-8 -*-
import loader
import networkx as nx
import os
import time

def main():
    
    loader = loader.Loader()   
    loader.create_graph(9.972153,57.007566,10.005369,57.020594) ##aalborg øst
    loader.load_graph()
    G=loader.graph
    print len(G.nodes()), len(G.edges())
    p = shortest_path_through_all(G,loader.street_node('Selma Lagerløfs Vej'), loader.street_node('Niels Bohrs Vej'))
    for x in xrange(1,10):
        print p[x]
    print len(p)

def fastest_path(G):
	pass

def timecalculator(edges=[]):
	pass


def BFS(G, s):
	loader = loader.Loader()
    	loader.create_graph(9.972153,57.007566,10.005369,57.020594) ##aalborg øst
    	loader.load_graph()
    	G=loader.graph
	return nx.bfs_tree(G, s)

loader = loader.Loader()
loader.create_graph(9.972153,57.007566,10.005369,57.020594) ##aalborg øst
loader.load_graph()
G=loader.graph
s = loader.street_node('Selma Lagerløfs Vej')
print BFS(G, s)
def CR(v):
	return v*v+v 



def shortest_path_through_all(G,s,t):
        shortest_paths = []
        for node in G.nodes():
            if node != s and node != t:
                try:
                    p = nx.shortest_path(G,s,node) + nx.shortest_path(G,node,t)
                    shortest_paths.append(p)
                except: 
                    pass
        return shortest_paths
