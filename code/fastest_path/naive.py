import vehicle
from haversine import distance
import networkx as nx
import time


def naive_path(rn, v, s, t):
    bat = v.curbat #kwh
    car_range = bat / v.consumption_rate(70) # car_range in crow flight, based on average speed (70) on roads
    shortest_through_path = []
    driven_path = [s]
    cur_node = s
    route_plan_time = 0
    while cur_node != t:
        shortest_through_path = []
        shortest_through = float('inf')
        look_at= []
        for node in rn.nodes(): #find all charge stations within car_range as the crows flies
            if node == t:
                sp_t = nx.shortest_path(rn, cur_node, t, weight='weight')
                if reachable(rn, sp_t, v, bat):
                    shortest_through_path = sp_t
                    break
            elif rn.node[node]['charge_rate'] != 0 and\
            distance((float(rn.node[node]['lat']),float(rn.node[node]['lon'])),
                     (float(rn.node[cur_node]['lat']),float(rn.node[cur_node]['lon']))) <= car_range and node != cur_node:
                look_at.append(node)
                try:
                    if (shortest_through != float('inf')):
                        sp_char = nx.shortest_path(rn, cur_node, node, weight='weight', cutoff=shortest_through)
                    else:
                        sp_char = nx.shortest_path(rn, cur_node, node, weight='weight')
                except:
                    continue
                if reachable(rn, sp_char, v, bat):
                    sp_t = nx.shortest_path(rn, node, t, weight='weight')
                    del sp_t[0]
                    combine_path = sp_char + sp_t
                    if shortest_through > path_length(rn, sp_t):
                        shortest_through = path_length(rn, combine_path)
                        shortest_through_path = sp_char
        rn.visualize_nodes(look_at[:500])
        if shortest_through_path:
            route_plan_time += path_time(rn, shortest_through_path) + charge_time(rn, shortest_through_path, v) #add time spend driven and charging for this sub-path
            print 'cur: ',cur_node, 'next:',shortest_through_path[-1]
            cur_node = shortest_through_path[-1]
            del shortest_through_path[0]
            driven_path += shortest_through_path
        else:
            return [],float('inf')
    return driven_path, route_plan_time

def path_length(rn, P):
    """returns the length of the path"""
    return sum([rn[P[x]][P[(x+1)]]['weight'] for x in xrange(len(P)-1)])

def charge_time(rn, P, v):
    """returns the time spend charging"""
    needed_energy = 0
    edge_distance = 0
    for x in xrange(len(P)-1): # for each edge
        edge = rn[P[x]][P[(x+1)]]
        edge_distance = edge['weight']
        speed_limit = edge['speed_limit']
        needed_energy += (edge_distance*v.consumption_rate(speed_limit))
    if rn.node[P[-1]]['charge_rate'] == 0: #case: target node, no need to charge
        return 0
    return needed_energy/rn.node[P[-1]]['charge_rate']

def path_time(rn, P):
    """returns the time spent travelling the path P given """
    return sum([(rn[P[x]][P[(x+1)]]['weight'])*1.0/(rn[P[x]][P[(x+1)]]['speed_limit']) for x in xrange(len(P)-1)])

def reachable(rn, P, v, energy):
    """returns subpath of P if nodes are reachable given energy"""
    edge_distance = 0
    needed_energy = 0
    for x in xrange(len(P)-1): # for each edge
        edge = rn[P[x]][P[(x+1)]]
        edge_distance = edge['weight']
        speed_limit = edge['speed_limit']
        needed_energy += (edge_distance*v.consumption_rate(speed_limit))
    return needed_energy <= energy
