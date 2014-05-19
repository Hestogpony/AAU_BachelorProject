import networkx as nx
from inRange import inRange
from haversine import distance


def drive_naive(rn, s, t, ev, battery_procent):
    shortest_path = nx.shortest_path(rn, s, t, 't')
    path = []
    node = s
    closest_cs = None
    for i in range(0, len(shortest_path)-1):
        node = shortest_path[i]
        edge = rn.edge[node][shortest_path[i+1]]
        energy_used = edge['weight']*ev.consumption_rate(edge['speed_limit'])
        path.append(node)
        if ev.curbat - energy_used < ev.battery_capacity*battery_procent:
            possible_cs = inRange(rn, shortest_path[i], t, ev)
            length = float('inf')
            for CS in possible_cs:
                lengthToCS = distance((float(rn.node[node]['lat']),float(rn.node[node]['lon'])), (float(rn.node[CS]['lat']), float(rn.node[CS]['lon'])))
                if length > lengthToCS:
                    length = lengthToCS
                    closest_cs = CS
            return path, node, closest_cs
        ev.curbat -= energy_used
    return path, node, closest_cs


def find_common_node(totalpath, newpath):
    node = None
    for n in newpath:
        if n in totalpath:
            node = n
        else:
            break
    return node


def pathconcat(totalpath, newpath):
    common_node = find_common_node(totalpath, newpath)
    if not common_node:
        return totalpath + newpath
    index_totalpath = totalpath.index(common_node)
    p1 = totalpath[:index_totalpath]
    p1.append(common_node)
    index_newpath = newpath.index(common_node)
    p2 = newpath[index_newpath:]

    return p1+p2

def getPathTime(rn, path, charge_stations, ev):
    initial_battery = ev.curbat
    charge_rate = 0
    time = 0
    for i in range(0, len(path)-1):
        node = path[i]
        nextnode = path[i+1]
        try:
            edge = rn.edge[node][nextnode]
            energy_consumed = edge['weight']*ev.consumption_rate(edge['speed_limit'])
            if node in charge_stations:
                charge_rate = rn.node[node]['charge_rate']
            if energy_consumed < initial_battery:
                time += edge['t']
            else:
                time += edge['t']
                charge_time = energy_consumed/charge_rate
                time += charge_time
            initial_battery -= energy_consumed
        except:
            continue

    return time



def naive_path(rn, s, t, ev):
    total_path = []
    initial_battery = ev.curbat
    battery_procent = 0.1
    start = s
    path, node, closest_cs = drive_naive(rn, s, t, ev, battery_procent)
    charge_stations = []

    while t not in total_path and t not in path:
        if closest_cs:
            charge_stations.append(closest_cs)
            total_path = pathconcat(total_path, path)
            start = closest_cs
            battery_procent = 0.1
            ev.curbat = ev.battery_capacity
            total_path = pathconcat(total_path,nx.shortest_path(rn, node, closest_cs, 't'))
            path, node, closest_cs = drive_naive(rn, closest_cs, t, ev, battery_procent)
        else:
            battery_procent += 0.1
            ev.curbat = ev.battery_capacity
            path, node, closest_cs = drive_naive(rn, start, t, ev, battery_procent)
        if battery_procent == 1:
            total_path = []
            break
    ev.curbat = initial_battery
    total_path += path
    total_path = total_path
    return (total_path, getPathTime(rn, total_path, charge_stations, ev))
