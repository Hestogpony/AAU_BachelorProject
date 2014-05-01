
from sympy import *
from operator import itemgetter
from copy import copy, deepcopy

def getV(min_v, max_v, v):
    if v < min_v:
        return min_v
    elif max_v < v:
        return max_v
    else:
        return v

def cleanPreCs(preCS, myCS, curbat):
    myCS[0] -= curbat
    if myCS[1] > preCS[0][1]:
        return [myCS]
    preCS.append(myCS)
    return preCS

def updateCSAfterCharging(chargeStations, usedEnergy):
    for chargeStation in chargeStations:
        if chargeStation:
            chargeStation[0] -= usedEnergy
            
def updateCS(charge_stations):
    
    bestCS = charge_stations[0]
    
    for CS in charge_stations:
        if CS[1] >= bestCS[1]:
            bestCS = CS
                            
    place = charge_stations.index(bestCS)
    return charge_stations[:place]

def getBestChargeStation(chargeStations):
    if not chargeStations:
        print "found a bad path"
        return [[]]
    bestStation = chargeStations[0]
    for chargeStation in chargeStations:
        if chargeStation[1] > bestStation[1]:
            bestStation = chargeStation

    place = chargeStations.index(bestStation)
    return chargeStations[:place]

# Function checks if newly added charge station (currentCS)
# is faster than all of the previous charge stations (preCS)
# returns currentCS if true else returns preCS 
def getChargeRate(preCS, currentCS):
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
    
def consumption_rate(v):
    return ((0.0286 * v**2 + 0.4096 * v + 107.57) * 10**(-3))


def travel_time(preCS, myCS, e, cur_battery):

    dist = e[2]['weight']
    maxSpeed = e[2]['speed_limit']
    minSpeed = e[2]['speed_limit']*0.8
    
    # Case 1
    x = Symbol('x')
    try:
        v_opt_points_case1 = solve( dist*((0.0286 * x**2 + 0.4096 * x + 107.57) * 10**(-3)) - cur_battery)
        v_opt_case1 = getV(minSpeed, maxSpeed, v_opt_points_case1[1])
    except:
        v_opt_case1 = float('inf')
        
    if dist*consumption_rate(v_opt_case1) > cur_battery:
        time_case1 = float('inf')
    else:
        time_case1 = dist/v_opt_case1    
    cur_battery_case1 = cur_battery-(dist*consumption_rate(v_opt_case1))
    
    if time_case1 < float('inf') and v_opt_case1 == maxSpeed: #If we have the energy needed to drive at max speed we pick case 1 right away.
        return (time_case1, preCS , cur_battery_case1)
    
    # Case 2
    chargeStations = getChargeRate(preCS, myCS) # 
    if chargeStations[0]:
        time_case2 = float('inf')
        if time_case1 < time_case2:
            return (time_case1, preCS, cur_battery_case1)
        else:
            return (time_case2, chargeStations, cur_battery)
    
    chargeRate = chargeStations[0][1] #The charge speed of the fastest charge station.
    possible_energy = chargeStations[0][0]
    edge_time = dist/x + ((((0.0286 * x**2 + 0.4096 * x + 107.57) * 10**(-3))*dist)/chargeRate)
    edge_time_prime = edge_time.diff()
    v_opt_points_case2 = solve(edge_time_prime)
    v_opt_case2 = getV(minSpeed, maxSpeed, v_opt_points_case2[0])
    additional_time = 0
    
    while (consumption_rate(v_opt_case2)*dist) - cur_battery > possible_energy:  
        cur_battery += possible_energy
        additional_time += (possible_energy / chargeRate)
        chargeStations.remove(0)
        chargeStations = updateCS(chargeStations)
        possible_energy = chargeStations[0][0]
        chargeRate = chargeStations[0][1] 
         
    time_case2 = dist/v_opt_case2 + (((consumption_rate(v_opt_case2)*dist) - cur_battery)/chargeRate) + additional_time
    cur_battery_case2 = cur_battery - (consumption_rate(v_opt_case2)*dist) 
    
    if time_case1 < time_case2:
        preCS.append(myCS)
        chargeStations = updateCS(preCS)
        return (time_case1, chargeStations, cur_battery_case1)
    else:
        return (time_case2, chargeStations, cur_battery_case2)

def fastest_path_greedy(graph, s, t, ev, init_battery, battery_cap):
    G = copy(graph)

    for id, data in G.nodes(data=True):
        data['time'] = float('inf')
        data['path'] = [id]
        data['preCS'] = []
        data['myCS'] = [battery_cap, data['charge_rate']]
        data['curbat'] = 0
    G.node[s]['time'] = 0
    G.node[s]['path'] = [s]
    G.node[s]['curbat'] = init_battery
    open_nodes = sorted(G.nodes(data=True), key=lambda x: x[1]['time'])
    while open_nodes:
        node_id, node_data = open_nodes[0]
        open_nodes.remove(open_nodes[0])
        if node_data['time'] == float('inf'):
            print "The graph is not connected"
            break
        for e in G.edges([node_id], data=True):
            time, preCS, curbat = travel_time(deepcopy(node_data['preCS']), node_data['myCS'], e, node_data['curbat'])
            if time == float('inf'):
                print "The path is not possible"
                break
            node = G.node[e[1]]
            if node['time'] > node_data['time'] + time:
                node['time'] = time + node_data['time']
                node['path'] = node_id
                node['curbat'] = curbat
                if preCS:
                    node['preCS'] = cleanPreCs(preCS, node['myCS'], curbat)
                else:
                    node['preCS'] = [node['myCS']]
                open_nodes.sort(key=lambda x: x[1]['time'])
# print open_nodes
    print G.node[t]