
from copy import copy, deepcopy
from heapq import heappop, heappush
from inRange import inRange
import subprocess
import networkx as nx
from haversine import distance

# returns the optimal velocity v
# between v_min and v_max
def getV(v_min, v_max, v):
    if v < v_min:
        return v_min
    elif v_max < v:
        return v_max
    else:
        return v

def drange(start, stop, step):
    while start < stop:
        yield start
        start += step


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
    return charge_stations[place:]

def getBestChargeStation(chargeStations):
    if not chargeStations:
        return [[]]
    bestStation = chargeStations[0]
    for chargeStation in chargeStations:
        if chargeStation[1] > bestStation[1]:
            bestStation = chargeStation

    place = chargeStations.index(bestStation)
    return chargeStations[:place]

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

def fastSolveCase1(ev, dist, minSpeed, maxSpeed, curbat):
    best = float('inf')
    for x in drange(minSpeed, maxSpeed+0.1, 0.1):
        if dist*ev.consumption_rate(x) - curbat < 0: #While we have more energy then we consume we update our optimal speed
            best = x
    return best

def fastSolveCase2(dist, minSpeed, maxSpeed, chargeRate, ev):
    v_opt_case2 = float('inf')
    best_time = float('inf')
    for x in drange(minSpeed, maxSpeed+0.1, 0.1):
        temp = dist/x + ((ev.consumption_rate(x)*dist)/chargeRate)
        if temp < best_time:
            best_time = temp
            v_opt_case2 = x
    return v_opt_case2


def travel_time(preCS, myCS, e, ev, nodecurbat):

    dist = e[2]['weight']
    maxSpeed = e[2]['speed_limit']
    minSpeed = e[2]['speed_limit']*0.8
    # Case 1
    v_opt_case1 = fastSolveCase1(ev, dist, minSpeed, maxSpeed, nodecurbat)
    if v_opt_case1 < float('inf'):
        v_opt_case1 = int(v_opt_case1)

    # If we don't have enough energy to drive at the optimal speed the edge cannot be driven with the energy in the battery
    if dist*ev.consumption_rate(v_opt_case1) > nodecurbat: 
        time_case1 = float('inf')
    else: #Otherwice the time is calculated
        time_case1 = dist/v_opt_case1  
    energy_used_case1 = (dist*ev.consumption_rate(v_opt_case1))
    cur_battery_case1 = nodecurbat-energy_used_case1


    if time_case1 < float('inf') and v_opt_case1 == maxSpeed: #If we have the energy needed to drive at max speed we pick case 1 right away.
        chargeStations = getChargeRate(preCS, myCS) #maybe update chargestations here
        return (time_case1, chargeStations , cur_battery_case1, energy_used_case1)
    # Case 2
    chargeStations = getChargeRate(preCS, myCS)
     #If we can't charge or drive with the energy in the battery, we return time = float('inf') because we cannot drive the path
    if (not chargeStations) and time_case1 == float('inf'):
        return float('inf'), [], nodecurbat, float('inf')

    #If we don't have any charge stations, but enough energy in the battery to drive the path we drive the path using the energy
    if not chargeStations:
        chargeStations = getChargeRate(preCS, myCS)
        return time_case1, chargeStations, cur_battery_case1, energy_used_case1

    chargeRate = chargeStations[0][1] #The charge speed of the fastest charge station.
    possible_energy = chargeStations[0][0]
    #finds the optimal way to drive an edge using a chargestation
    v_opt_case2 = fastSolveCase2(dist, minSpeed, maxSpeed, chargeRate, ev)


    #If we can drive the edge using previous charge stations we calculate the time used to drive this way
    time_case2 = dist/v_opt_case2 + (((ev.consumption_rate(v_opt_case2)*dist) - nodecurbat)/chargeRate)
    energy_used_case2 = (ev.consumption_rate(v_opt_case2)*dist)

    if energy_used_case2 > possible_energy:
        del chargeStations[0]
        chargeStations = filterCS(chargeStations)

     #If we can't charge or drive with the energy in the battery, we return time = float('inf') because we cannot drive the path
    if (not chargeStations) and time_case1 == float('inf'):
        return float('inf'), [], nodecurbat, float('inf')

    #If we don't have any charge stations, but enough energy in the battery to drive the path we drive the path using the energy
    if not chargeStations:
        chargeStations = getChargeRate(preCS, myCS)
        return time_case1, chargeStations, cur_battery_case1, energy_used_case1



    cur_battery_case2 = nodecurbat - energy_used_case2

    if cur_battery_case2 < 0:
        cur_battery_case2 = 0

    if time_case1 < time_case2:
        chargeStations = getChargeRate(preCS, myCS)
        return time_case1, chargeStations, cur_battery_case1, energy_used_case1
    else:
        return time_case2, chargeStations, cur_battery_case2, energy_used_case2
       

def getSlope(lowerX, higherX, lowerY, higherY):
    return (higherY-lowerY)/(higherX-lowerX)

def LPprinter(ChargeConstants, edgeDists, edgeSpeeds, Precision, ev, curbat):
    n = "param n := {0};\n".format(len(edgeDists))
    m = "param m := {0}; \n".format(Precision)
    initialBat = "param initialBat := {0};\n".format(curbat)
    batCap = "param batCap := {0}; \n".format(ev.battery_capacity)
    points = "param points: \n"
    points2 = "param points2: \n"
    linesA = "param linesA: \n"
    linesB = "param linesB: \n"
    speedDists = "param speedDistanceRelation: \n 1		2 := \n"
    edgeDist = "param edgeDist := "
    chargeConstants = "param chargeConstants := "
    rangeList = ""
    for i in range(0, len(edgeDists)-1):
        edgeDist += "%s %s, " % ((i+1), edgeDists[i])
        chargeConstants += "%s %s, " % ((i+1), ChargeConstants[i])
    edgeDist += "%s %s" % ((len(edgeDists)), edgeDists[-1])
    chargeConstants += "%s %s " % ((len(edgeDists)), ChargeConstants[-1])

    for i in range(1, Precision+1):
        rangeList += "%s " % (i)
    rangeList += ":= \n"
    points += rangeList
    points2 += rangeList
    linesA += rangeList
    linesB += rangeList

    for i in range(0, len(edgeDists)):
        minSpeed = edgeSpeeds[i]*0.8
        maxSpeed = edgeSpeeds[i]
        stepSize = (maxSpeed-minSpeed)/Precision
        speedSlope = getSlope(maxSpeed, minSpeed, edgeDists[i]/maxSpeed, edgeDists[i]/minSpeed)
        speedDist = "%s %s %s" % ((i+1), speedSlope, (edgeDists[i]/minSpeed)-(minSpeed*speedSlope))
        lowerXes = "%s " % (i+1)
        higherXes = "%s " % (i+1)
        lineA = "%s " % (i+1)
        lineB = "%s " % (i+1)
        while maxSpeed-stepSize+1 > minSpeed:
            lowerX = minSpeed
            lowerXes += "%s " % lowerX
            higherX = minSpeed + stepSize
            higherXes += "%s " % higherX
            slope = getSlope(lowerX, higherX, ev.consumption_rate(lowerX), ev.consumption_rate(higherX))
            lineA += "%s " % slope
            lineB += "%s " % (ev.consumption_rate(higherX)-slope*higherX)
            minSpeed += stepSize
    
        points += lowerXes + "\n"
        points2 +=  higherXes + "\n"
        speedDists += speedDist + "\n"
        linesA += lineA + "\n"
        linesB += lineB + "\n"
    
    output_file = open("LPData.dat", "w")
    output_file.write(n)
    output_file.write(m)
    output_file.write(initialBat)
    output_file.write(batCap)
    output_file.write(points + ";\n")
    output_file.write(points2 + ";\n")
    output_file.write(speedDists + ";\n")
    output_file.write(linesA + ";\n")
    output_file.write(linesB + ";\n")
    output_file.write(edgeDist + ";\n")
    output_file.write(chargeConstants + ";\n")

    output_file.close()
    proc = subprocess.Popen("glpsol  --model fastestPathLinearization.mod --data LPData.dat", stdout=subprocess.PIPE, shell=True)

    pathTime = float('inf')
    pathCurbat = 0
    for line in iter(proc.stdout.readline, ''):
        print line
        try:
            num = float(line.rstrip())
            if pathTime == float('inf'):
                pathTime = num
            else:
                pathCurbat = num
        except:
            pass
    return pathTime, pathCurbat
# print line.rstrip()

def linearProgramming(G, preNode, curNode, ev, curbat):
    print "here:::::: ", preNode, curNode
    ChargeConstants = []
    edgeDists = []
    edgeSpeeds = []
    nodes = []
    print G.edge[preNode][curNode]
    
    nodes.append(curNode)
    nodes.append(preNode)
    path = G.node[preNode]['path']
    while path != 0:
        nodes.append(path)
        path = G.node[path]['path']
    nodes.reverse()
    for i in range(0,len(nodes)-1):
        ChargeConstants.append(G.node[nodes[i]]['charge_rate'])
        edge = G.edge[nodes[i]][nodes[i+1]]
        edgeSpeeds.append(edge['speed_limit'])
        edgeDists.append(edge['weight'])
    #print edge
    #ChargeConstants.append(G.node[nodes[-1]]['charge_rate'])
    #print ChargeConstants, len(ChargeConstants)
    #print edgeSpeeds, len(edgeSpeeds)
    #print edgeDists, len(edgeDists)
    time, newcurbat = LPprinter(ChargeConstants, edgeDists, edgeSpeeds, 5, ev, curbat)
    return time, newcurbat
    # print G.node[preNode]['charge_rate'], G.node[curNode]['charge_rate']

def age(charge_stations, energy):
    for i in range(0, len(charge_stations)):
        charge_stations[i][0] -= energy


def pathEnergy(G, preNode, ev):
    path_energy = 0
    nodes = []
    batcap = 0
    path = G.node[preNode]['path']
    while path != 0 and G.node[path]['myCS'][1] == 0:
        nodes.append(path)
        path = G.node[path]['path']
    nodes.reverse()
    for i in range(0,len(nodes)-1):
        edge = G.edge[nodes[i]][nodes[i+1]]
        path_energy += edge['weight']*ev.consumption_rate(edge['speed_limit']*0.8)
    return batcap - path_energy


def fastest_path_greedy(graph, s, t, algorithm, ev):
    G = deepcopy(graph)
    print "Started"
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
        #print node_id
        if node_data['time'] == float('inf'):
            print "NO PATH FOUND", len(open_nodes)
            break
        for e in G.edges([node_id], data=True):
            node = G.node[e[1]]

            if node['time'] <= node_data['time']+e[2]['t']:
                continue

            if algorithm == 1:
                time, preCS, curbat, energyUsed = travel_time(deepcopy(node_data['preCS']), deepcopy(node_data['myCS']), e, ev, node_data['curbat'])
                totalTime = node_data['time'] + time
            elif algorithm == 0:
                totalTime = node_data['time'] + e[2]["t"]
                curbat = 0
                preCS = []
            else:
                time, preCS, curbat, energyUsed = travel_time(deepcopy(node_data['preCS']), deepcopy(node_data['myCS']), e, ev, node_data['curbat'])
                if time == float('inf'):
                    ev.curbat = pathEnergy(graph, node_id, ev)
                    if inRange(graph, s, t, ev):
                        totalTime, curbat = linearProgramming(G, node_id, e[1], ev, ev.curbat)
                        preCS = []
                    else:
                        totalTime = float('inf')
                else:
                    totalTime = node_data['time'] + time

            if node['time'] > totalTime:
                node['time'] = totalTime
                node['path'] = node_id
                node['curbat'] = curbat
                if preCS:
                    node['preCS'] = preCS
                    age(node['preCS'], energyUsed)
                node['myCS'][0] = ev.battery_capacity - curbat
                heappush(open_nodes, (totalTime, e[1]))

    # print open_nodes
    Path = []
    path =  G.node[t]['path']
        
    totaltime =  G.node[t]['time']
    if totaltime == float('inf'):
        return ([], totaltime)

    Path.append(t)
    while path !=s:
        Path.append(path)
        path = G.node[path]['path']
    Path.append(s)
    Path.reverse()
    return (Path, totaltime)


# fix, make sure that all but aging of the charging stations work, then make sure charge stations work propperly