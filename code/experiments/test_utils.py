import networkx as nx
import random
from fastest_path.vehicle import EV

def scale_charge_rates(rn, scale_factor):
    for n in rn:
        charge_rate = rn.node[n]['charge_rate']
        if charge_rate > 0:
            rn.node[n]['charge_rate'] = charge_rate * scale_factor

def s_and_t(rn, distance):
    scrambled_nodes = rn.nodes()[:]
    random.shuffle(scrambled_nodes)
    for node in scrambled_nodes:
        i = 0
        distances = nx.single_source_dijkstra_path_length(rn, node, weight='weight')
        for vertex, path_dist in distances.items():
            if (distance * 1.01) > path_dist > (distance * 0.99):
                return node, vertex, path_dist

def scale_road_network(rn, scale_factor):
    print("scaling distancens by: " + str(scale_factor))
    for edge in rn.edges(data = True):
        new_dist = edge['weight'] * scale_factor
        edge['weight'] = new_dist


def charge_station_density(rn, dist):
    for node in rn.nodes():
        if (node in rn):
            if (rn.node[node]['charge_rate'] != 0):
                rn.node[node]['charge_rate'] = 60
                dists = nx.single_source_dijkstra_path_length(rn,node,cutoff=dist,weight='weight')
                for vertex,dval in dists.items():
                    if vertex != node:
                        rn.node[vertex]['charge_rate'] = 0

def scale_cons_rate(pct):
    evs = []
    for x in xrange(-pct,pct):
        multiplier = 1+(x/100.0)
        evs.append(EV(80, 80,lambda x, copy=multiplier: ((0.04602*x**2+0.6591*x+173.1174)*10**(-3))*copy))
    return evs

def set_roadnetwork_complexity(rn, num_nodes):
    lonmax = 12.89
    #latmax = 57.86
    connected_components = nx.connected_components(rn)
    sorted(connected_components, key=len)

    while len(connected_components[0]) > num_nodes:

        #print(len(connected_components[0]))
        #latmax -= 0.02
        lonmax -= 0.02
        for node in rn.nodes():
            if (float(rn.node[node]['lon']) >= lonmax):
                rn.remove_node(node)
        connected_components = nx.connected_components(rn)
        sorted(connected_components, key=len)

    for list_of_nodes in connected_components[1:]:
        for node in list_of_nodes:
            rn.remove_node(node)
    return rn.number_of_nodes()
