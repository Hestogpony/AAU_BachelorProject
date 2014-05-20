
from copy import copy, deepcopy
from heapq import heappop, heappush
from inRange import inRange
import subprocess
import networkx as nx
from haversine import distance

def drange(start, stop, step):
    while start < stop:
        yield start
        start += step

def filterCS(chargeStations):
    best = 0
    station = None
    for cs in chargeStations:
        if cs[1] >= best:
            station = cs
            best = cs[1]
    if station:
        index = chargeStations.index(station)
        chargeStations = chargeStations[index:]
    return chargeStations

# Function checks if newly added charge station (currentCS)
# is faster than all of the previous charge stations (preCS)
# returns currentCS if true else returns preCS
def getChargeStations(preCS, currentCS):
    current_rate = currentCS[1]
    if current_rate == 0:
        return preCS
    if len(preCS) == 0:
        return [currentCS]
    max_rate = preCS[0][1]

    if max_rate > current_rate:
        preCS.append(currentCS)
        return preCS
    else:
        return [currentCS]

def fastSolveCase1(ev, dist, minSpeed, maxSpeed, curbat):
    optimal_speed = float('inf')
    for speed in drange(minSpeed, maxSpeed+0.1, 0.1):
        if curbat - dist*ev.consumption_rate(speed) >= 0: #While we have more energy then we consume we update our optimal speed
            optimal_speed = speed
    return optimal_speed

def fastSolveCase2(dist, minSpeed, maxSpeed, chargeRate, ev, curbat):
    v_opt_case2 = float('inf')
    best_time = float('inf')  
    for x in drange(minSpeed, maxSpeed+0.1, 0.1):
        if (ev.consumption_rate(x)*dist - curbat >= 0):
            temp = dist/x + ((ev.consumption_rate(x)*dist - curbat) /chargeRate)
            if temp < best_time:
                best_time = temp
                v_opt_case2 = x
    return v_opt_case2

def travel_time(preCS, myCS, edge_data, ev, nodecurbat):

    dist = edge_data['weight']
    maxSpeed = edge_data['speed_limit']
    minSpeed = edge_data['speed_limit']*0.7
    
    # Case 1: There's enough energy on curbat to drive without charging
    v_opt_case1 = fastSolveCase1(ev, dist, minSpeed, maxSpeed, nodecurbat)

    # If we don't have enough energy to drive at the optimal speed the edge cannot be driven with the energy in the battery
    if v_opt_case1 == float('inf'):
        time_case1 = float('inf')
    else: #Otherwice the time is calculated
        time_case1 = dist/v_opt_case1
        energy_needed_case1 = (dist*ev.consumption_rate(v_opt_case1))
        cur_battery_case1 = nodecurbat-energy_needed_case1
    
    # Case 2: 
    chargeStations = getChargeStations(preCS, myCS)
    
    #If we can't charge or drive with the energy in the battery, we return time = float('inf') because we cannot drive the path
    if (not chargeStations) and time_case1 == float('inf'):
        return float('inf'), [], nodecurbat, float('inf')

    #If we don't have any charge stations, but enough energy in the battery to drive the path we drive the path using the energy
    if not chargeStations:
        return time_case1, chargeStations, cur_battery_case1, energy_needed_case1

    chargeRate = chargeStations[0][1] #The charge speed of the fastest charge station.
    possible_energy = chargeStations[0][0]
    v_opt_case2 = fastSolveCase2(dist, minSpeed, maxSpeed, chargeRate, ev, nodecurbat)

    #If we can drive the edge using previous charge stations we calculate the time used to drive this way
    time_case2 = dist/v_opt_case2 + (((ev.consumption_rate(v_opt_case2)*dist) - nodecurbat)/chargeRate)
    energy_needed_case2 = (ev.consumption_rate(v_opt_case2)*dist)
    additional_energy = 0
    additional_time = 0
    
    while energy_needed_case2 > possible_energy + additional_energy:
        additional_energy += possible_energy
        additional_time += possible_energy / chargeRate
        del chargeStations[0]
        chargeStations = filterCS(chargeStations)
        if (not chargeStations) and time_case1 == float('inf'):
            return float('inf'), [], nodecurbat, float('inf')
        if not chargeStations:
            return time_case1, chargeStations, cur_battery_case1, energy_needed_case1
        
        chargeRate = chargeStations[0][1] #The charge speed of the fastest charge station.
        possible_energy = chargeStations[0][0]
        v_opt_case2 = fastSolveCase2(dist, minSpeed, maxSpeed, chargeRate, ev, nodecurbat+additional_energy)
        time_case2 = dist/v_opt_case2 + (((ev.consumption_rate(v_opt_case2)*dist) - (nodecurbat+additional_energy))/chargeRate)
        energy_needed_case2 = (ev.consumption_rate(v_opt_case2)*dist)
    
    cur_battery_case2 = additional_energy + nodecurbat - energy_needed_case2
    time_case2 += additional_time
     
    if time_case1 < time_case2:
        return time_case1, chargeStations, cur_battery_case1, energy_needed_case1
    else:
        return time_case2, chargeStations, cur_battery_case2, energy_needed_case2

def update_possible_energy(charge_stations, energy):
    for cs in charge_stations:
        if cs[0] <= energy:
            charge_stations.remove(cs)
        else:
            cs[0] -= energy
    return filterCS(charge_stations)
         

def fastest_path_greedy(G, s, t, algorithm, ev):
    #shortest_path_time = nx.shortest_path_length(G, s, t, weight = 'weight') * 1.5

    for node_id, data in G.nodes(data=True):
        data['time'] = float('inf')
        data['path'] = None
        data['preCS'] = []
        data['myCS'] = [ev.battery_capacity, data['charge_rate']]
        data['curbat'] = 0
    G.node[s]['time'] = 0
    G.node[s]['path'] = 0
    G.node[s]['curbat'] = ev.curbat
    open_nodes = []
    heappush(open_nodes, (0, s))
    while open_nodes:
        node_id = heappop(open_nodes)[1] 
        node_data = G.node[node_id]
        for _, neighbour_id, edge_data in G.edges([node_id], data=True):
            neighbour_data = G.node[neighbour_id]

            if (neighbour_data['time'] <= node_data['time']+edge_data['t'])\
                and ((neighbour_data['preCS'] or neighbour_data['myCS'][1] > 0) or not (node_data['preCS'] or node_data['myCS'][1] > 0)):
                continue

            time, preCS, curbat, energyUsed = travel_time(deepcopy(node_data['preCS']), deepcopy(node_data['myCS']), edge_data, ev, node_data['curbat'])
            totalTime = node_data['time'] + time

            if neighbour_data['time'] > totalTime:
                neighbour_data['time'] = totalTime
                neighbour_data['path'] = node_id
                neighbour_data['curbat'] = curbat
                if preCS:
                    neighbour_data['preCS'] = update_possible_energy(preCS, energyUsed)
                neighbour_data['myCS'][0] = ev.battery_capacity - curbat
                heappush(open_nodes, (totalTime, neighbour_id))

    driven_path = []
    path =  G.node[t]['path']

    totaltime =  G.node[t]['time']
    if totaltime == float('inf'):
        return ([], totaltime)
    
    driven_path.append(t)
    while path !=s:
        driven_path.append(path)
        path = G.node[path]['path']
    driven_path.append(s)
    driven_path.reverse()
    return (driven_path, totaltime)
