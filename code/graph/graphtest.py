import pylab as p
import networkx as nx


class Node(object):
    nodes = []

    def __init__(self, label):
        self._label = label

    def __str__(self):
        return self._label

nodes = [Node(l) for l in ["A","B","C","C","D","H"]]
edges = [(0,1),(0,5),(5,2),(1,3),(1,4)]

G = nx.Graph()
for i,j in edges:
    G.add_edge(nodes[i], nodes[j])

nx.draw(G)
p.show()
