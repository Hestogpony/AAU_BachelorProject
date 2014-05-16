from copy import copy, deepcopy
from heapq import heappop, heappush
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

def update_possible_energy(preCS, energyUsed):
    for CS in preCS:
        CS[0] -= energyUsed

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
    print currentCS
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

def fastSolveCase1(ev, dist, minSpeed, maxSpeed):
    best = float('inf')
    for x in drange(minSpeed, maxSpeed+0.1, 0.1):
        if dist*ev.consumption_rate(x) - ev.curbat < 0:
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


def travel_time(preCS, myCS, e, ev):
    print "Pre and my CS", preCS, myCS
    dist = e[2]['weight']
    maxSpeed = e[2]['speed_limit']
    minSpeed = e[2]['speed_limit']*0.8
    # Case 1
    v_opt_case1 = fastSolveCase1(ev, dist, minSpeed, maxSpeed)
    if v_opt_case1 < float('inf'):
        v_opt_case1 = int(v_opt_case1)
    print v_opt_case1
    if dist*ev.consumption_rate(v_opt_case1) > ev.curbat:
        time_case1 = float('inf')
    else:
        time_case1 = dist/v_opt_case1
    energy_used_case1 = (dist*ev.consumption_rate(v_opt_case1))
    cur_battery_case1 = ev.curbat-energy_used_case1
    print maxSpeed, v_opt_case1, ev.curbat
    if time_case1 < float('inf') and v_opt_case1 == maxSpeed: #If we have the energy needed to drive at max speed we pick case 1 right away.
        chargeStations = getChargeRate(preCS, myCS)
        print chargeStations
        print "returning from 1"
        return (time_case1, chargeStations , cur_battery_case1, energy_used_case1)
    # Case 2
    chargeStations = getChargeRate(preCS, myCS)
    print chargeStations, preCS, myCS
    if (not chargeStations) and time_case1 == float('inf'):
        return (float('inf'), [], ev.curbat, float('inf'))
    if (not chargeStations):
        chargeStations = getChargeRate(preCS, myCS)
        print chargeStations
        print "Returned from 1.2"
        return (time_case1, chargeStations , cur_battery_case1, energy_used_case1)
    chargeRate = chargeStations[0][1] #The charge speed of the fastest charge station.
    possible_energy = chargeStations[0][0]
    v_opt_case2 = fastSolveCase2(dist, minSpeed, maxSpeed, chargeRate, ev)
    additional_time = 0
    print v_opt_case2
    while (ev.consumption_rate(v_opt_case2)*dist) - ev.curbat > possible_energy:
        print "in while"
        ev.curbat += possible_energy
        additional_time += (possible_energy / chargeRate)
        try:
            chargeStations.remove(0)
            chargeStations = updateCS(chargeStations)
            possible_energy = chargeStations[0][0]
            chargeRate = chargeStations[0][1]
        except:
            return (float('inf'), [], ev.curbat, float('inf'))

    time_case2 = dist/v_opt_case2 + (((ev.consumption_rate(v_opt_case2)*dist) - ev.curbat)/chargeRate) + additional_time
    energy_used_case2 = (ev.consumption_rate(v_opt_case2)*dist)
    cur_battery_case2 = ev.curbat

    if time_case1 < time_case2:
        chargeStations = getChargeRate(preCS, myCS)
        return (time_case1, chargeStations, cur_battery_case1, energy_used_case1)
    else:
        return (time_case2, chargeStations, cur_battery_case2, energy_used_case2)


def getSlope(lowerX, higherX, lowerY, higherY):
    return (higherY-lowerY)/(higherX-lowerX)

def LPprinter(ChargeConstants, edgeDists, edgeSpeeds, Precision, ev):
    n = "param n := {0};\n".format(len(edgeDists))
    m = "param m := {0}; \n".format(Precision)
    batCap = "param batCap := {0}; \n".format(ev.battery_capacity)
    
    points = "param points: \n"
    
    points2 = "param points2: \n"
    
    linesA = "param linesA: \n"
    
    linesB = "param linesB: \n"
    
    speedDists = "param speedDistanceRelation: \n 1	 2 := \n"
    
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
    
    output_file.write(batCap)
    
    output_file.write(points + ";")
    
    output_file.write(points2 + ";")
    
    output_file.write(speedDists + ";")
    
    output_file.write(linesA + ";")
    
    output_file.write(linesB + ";")
    
    output_file.write(edgeDist + ";")
    
    output_file.write(chargeConstants + ";")
    
    output_file.close()
    
    proc = subprocess.Popen("glpsol  --model fastestPathLinearization.mod --data LPData.dat", stdout=subprocess.PIPE, shell=True)
    
    print "Test :"
    
    pathTime = float('inf')
    
    for line in iter(proc.stdout.readline,''):
        
        try:
            
            num = float(line.rstrip())
            
            pathTime = num
            
            print num
        
        except:
            
            pass
    
    return pathTime

# print line.rstrip()



def linearProgramming(G, preNode, curNode):
    
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
    
    print ChargeConstants, len(ChargeConstants)
    
    print edgeSpeeds, len(edgeSpeeds)
    
    print edgeDists, len(edgeDists)
    
    time = LPprinter(ChargeConstants, edgeDists, edgeSpeeds, 5, 50)
    
    return time

# print G.node[preNode]['charge_rate'], G.node[curNode]['charge_rate']



def fastest_path_greedy(graph, s, t, algorithm, ev):
    G = copy(graph)
    for node_id, data in G.nodes(data=True):
        data['time'] = float('inf')
        data['path'] = [node_id]
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
        print "now working on: ", node_id, "Nodes left: ", len(open_nodes)
        if node_data['time'] == float('inf'):
            print "The graph is not connected"
            break
        for e in G.edges([node_id], data=True):
            #print "look here ", node_data['myCS']
            node = G.node[e[1]]
            #print e, node_data, node_id
            if node_data['time'] > node['time']:
                continue
            if algorithm == 1:
                time, preCS, curbat, energyUsed = travel_time(deepcopy(node_data['preCS']), deepcopy(node_data['myCS']), e, ev)
                totalTime = node_data['time'] + time
            elif algorithm == 0:
                totalTime = node_data['time'] + e[2]["t"]
                curbat = 0
                preCS = []
                time = 0
            else:
                #totalTime = 1
                totalTime = linearProgramming(G, node_id, e[1])
                curbat = 0
                preCS = []
                time = 0
            if time == float('inf'):
                print "The path is not possible"
                break
            if node['time'] > totalTime:
                print "node updated"
                node['time'] = totalTime
                node['path'] = node_id
                node['curbat'] = curbat
                print preCS
                if preCS:
                    print "in pre    \n \n \n \n \n \n"
                    node['preCS'] = preCS
                    update_possible_energy(node['preCS'], energyUsed)
                node['myCS'][0] = ev.battery_capacity - curbat
                heappush(open_nodes, (totalTime, e[1]))
    # print open_nodes
    Path = []
    path =  G.node[t]['path']
    totaltime =  G.node[t]['time']
    if totaltime == float('inf'):
        return ([], totaltime)
    print "Path: "
    Path.append(t)
    while path !=s:
        Path.append(path)
        path = G.node[path]['path']
    Path.append(s)
    Path.reverse()
    return (Path, totaltime)