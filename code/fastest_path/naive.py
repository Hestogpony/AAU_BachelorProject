import importer
import networkx as nx
from fastest_path.vehicle import EV
from fastest_path.roadnetwork import RoadNetwork
import operator

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

def getPathTime(rn, path, ev):
    initial_battery = ev.curbat
    charge_rate = 0
    time = 0
    for i in range(0, len(path)-1):
        node = path[i]
        nextnode = path[i+1]
        edge = rn.edge[node][nextnode]
        energy_consumed = edge['weight']*ev.consumption_rate(edge['speed_limit'])
        if rn.node[node]['charge_rate'] != 0:
            charge_rate = rn.node[node]['charge_rate']
        if energy_consumed <= initial_battery:
            time += edge['t']
        else:
            time += edge['t']
            charge_time = (energy_consumed)/charge_rate
            time += charge_time
        initial_battery -= energy_consumed
    return time

def naive_path(rn,s,t,v):
    bat = v.curbat
    driven_path = [s]
    sp = nx.shortest_path(rn,s,t,weight='t')
    time = 0
    while driven_path[-1] != t:
        x = 0
        while bat > (v.battery_capacity * 0.4):
            edge = rn[sp[x]][sp[x+1]]
            bat -= edge['weight']*v.consumption_rate(edge['speed_limit'])
            driven_path.append(sp[x+1])
            if driven_path[-1] == t:
                break
            x+=1
        if driven_path[-1] == t:
            continue
        d,p = nx.single_source_dijkstra(rn,sp[x+1],weight='t', cutoff=(bat*v.consumption_rate(100)))
        sorted_d = sorted(d.iteritems(), key=operator.itemgetter(1))
        next_guy = sorted_d[0][0]
        while not ((rn.node[next_guy]['charge_rate'] != 0) and reachable(rn,p[next_guy],v,bat)):
            if sorted_d:
                del sorted_d[0]
            next_guy = sorted_d[0][0]
        if len(sorted_d)!=0:
            driven_path += p[next_guy]
            bat = v.battery_capacity
            sp = nx.shortest_path(rn,next_guy,t,weight='t')
        else:
            return ([],float('inf'))
    return (driven_path, getPathTime(rn,driven_path,v))
