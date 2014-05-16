import networkx as nx
from inRange import inRange
from haversine import distance


def drive_naive(graph, s, t, ev, battery_procent):
    shortest_path = nx.shortest_path(graph, s, t, 't')
    path = []
    node = s
    closest_cs = None
    for i in range(0, len(shortest_path)-1):
        node = shortest_path[i]
        edge = graph.edge[node][shortest_path[i+1]]
        energy_used = edge['weight']*ev.consumption_rate(edge['speed_limit'])
        path.append(node)
        if graph.node[node]['charge_rate']:
            ev.curbat = ev.battery_capacity
        if ev.curbat - energy_used < ev.battery_capacity*battery_procent:
            print ev.curbat, ev.battery_capacity
            possible_cs = inRange(graph, shortest_path[i], t, ev)
            print possible_cs
            length = float('inf')
            for CS in possible_cs:
                lengthToCS = distance((float(graph.node[node]['lat']),float(graph.node[node]['lon'])), (float(graph.node[CS]['lat']), float(graph.node[CS]['lon'])))
                if length > lengthToCS:
                    length = lengthToCS
                    closest_cs = CS
            return path, node, closest_cs
        ev.curbat -= energy_used
    return path, node, closest_cs


def get_navie_path(graph, s, t, ev):
    total_path = []
    battery_procent = 0.1
    start = s
    path, node, closest_cs = drive_naive(graph, s, t, ev, battery_procent)

    while t not in path:
        total_path += path
        if closest_cs:
            start = closest_cs
            battery_procent = 0.1
            ev.curbat = ev.battery_capacity
            total_path += nx.shortest_path(graph, node, closest_cs, 't')
            path, node, closest_cs = drive_naive(graph, closest_cs, t, ev, battery_procent)
            if closest_cs == t:
                total_path.append(t)
                break
        else:
            battery_procent += 0.1
            ev.curbat = ev.battery_capacity
            path, node, closest_cs = drive_naive(graph, start, t, ev, battery_procent)
            if closest_cs == t:
                total_path.append(t)
                break
        if battery_procent == 1:
            print "unsolvable"
            total_path = []
            break
        #print total_path
    return total_path


