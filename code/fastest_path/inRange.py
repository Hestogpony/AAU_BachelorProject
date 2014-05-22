from copy import deepcopy
from heapq import heappop, heappush
def inRange(graph, s, t, ev):
    G = graph
    nodes = set()
    #print "Here: " , ev.curbat
    for node_id, data in G.nodes(data=True):
        data['batcur'] = float('inf')
    G.node[s]['batcur'] = 0
    open_nodes = []
    heappush(open_nodes, (0, s))
    while open_nodes:
        node_id = heappop(open_nodes)[1]
        node_data = G.node[node_id]
#print "now working on: ", node_id
        if node_data['batcur'] == float('inf'):
            #           print "The graph is not connected"
            break
        nodes.add(node_id)
        for e in G.edges([node_id], data=True):
            node = G.node[e[1]]
            newcurbat = node_data['batcur'] + ev.consumption_rate(e[2]['speed_limit'])*e[2]['weight']
#print newcurbat, ev.curbat
            if newcurbat > ev.curbat:
                continue
            if node['batcur'] > newcurbat:
                node['batcur'] = newcurbat
                heappush(open_nodes, (newcurbat, e[1]))
    for n in list(nodes):
        if n == t:
            return [t]
        if G.node[n]['charge_rate'] == 0:
            nodes.remove(n)
    return nodes
