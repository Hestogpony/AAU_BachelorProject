import vehicle
from haversine import distance
import networkx as nx
import time

def naive_path(G, v, s, t):
    consumption = 
    bat = v.curbat #kwh
    car_range = bat * v.consumption_rate(70) # car_range in crow flight, based on average speed (70) on roads
    shortest_through = float('inf')
    shortest_through_path = []
    driven_path = [s]
    cur_node = s
    combined_path = 0
    path_time = 0

    while cur_node is not t:
        for node in G.nodes(): #find all charge stations within car_range as the crows flies
            
            if G.node[node] == t: #can the car reach t from s
                sp_t = nx.shortest_path(G, cur_node)
                if reachable(G, sp_t, v, bat):
                    shortest_through_path = sp_t 
                    break

            elif G.node[node]['charge_rate'] != 0 and\
            distance((float(G.node[node]['lat']),float(G.node[node]['lon'])), 
                     (float(G.node[cur_node]['lat']),float(G.node[cur_node]['lon']))) <= car_range:
                sp_char = nx.shortest_path(G, cur_node, node) # can the car reach a charge station with roads

                if reachable(G, sp_char, v, bat):
                    sp_t = nx.shortest_path(G, node, t)
                    del sp_t[0] 
                    combined_path = path_length(G, sp_char + sp_t)
                    if shortest_through > path_length:
                        shortest_through = path_length
                        shortest_through_path = sp_char
        #path_time += cal_path_time(G, shortest_through_path) +  #add time spend driven and charging for this sub-path
        cur_node = shortest_through_path[-1]
        del shortest_through_path[0]
        driven_path += shortest_through_path
        print G.node[cur_node]['name'], driven_path
    return driven_path

def path_length(G, P):
    """returns the length of the path"""
    return sum([G[P[x]][P[(x+1)]]['weight'] for x in xrange(len(P)-1)])

def cal_path_time(G, P):
    """returns the time spent travelling the path P given """
    return sum([(G[P[x]][P[(x+1)]]['weight'])*1.0/(G[P[x]][P[(x+1)]]['speed_limit']) for x in xrange(len(P)-1)])

def reachable(G, P, v, energy): 
    """returns subpath of P of reachable nodes given energy"""
    result = [] 
    edge_distance = 0
    for x in xrange(len(P)-1): # for each edge
        edge = G[P[x]][P[(x+1)]]
        edge_distance += edge['weight']
        speed_limit = edge['speed_limit']    
        if (edge_distance/v.consumption_rate(speed_limit)) <= energy:
            result.append(P[x+1])
        else:
            break
    if not result:
        return False
    return P[-1] == result[-1]

def bfs_edges(G,source, dist):
    """Produce edges in a breadth-first-search starting at source."""
    # Based on http://www.ics.uci.edu/~eppstein/PADS/BFS.py
    # by D. Eppstein, July 2004.
    visited=set([source])
    stack = [(source,iter(G[source]))]
    while stack:
        parent,children = stack[0]
        try:
            child = next(children)
            if child not in visited:
                yield parent,child
                visited.add(child)
                stack.append((child,iter(G[child])))
        except StopIteration:
            stack.pop(0)


                
