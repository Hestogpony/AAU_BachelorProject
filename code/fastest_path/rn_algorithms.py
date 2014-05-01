from copy import copy
from sympy import *
from operator import itemgetter

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

#Start
def UpdateCSAfterCharging(chargeStations, usedEnergy):
    for chargeStation in chargeStations:
        if chargeStation:
            chargeStation[0] -= usedEnergy

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

def getChargeRate(chargeStations, maxEnergy):
    if len(chargeStations) == 0:
        print "No charging Stations"
        return ([[]], 0, 0)
    max_energy = chargeStations[0][0]
    max_rate = chargeStations[0][1]
    if max_energy > maxEnergy:
        return (chargeStations, 0, 0)
    else:
        timeUsed = max_energy/max_rate
        addedBat = max_energy
        chargeStations.remove(chargeStations[0])
        UpdateCSAfterCharging(chargeStations, addedBat)
        chargeStations = updateChargeStation(chargeStations)
        return (chargeStations, timeUsed, addedBat)
#End

def f(v):
    return ((0.0286 * v**2 + 0.4096 * v + 107.57) * 10**(-3))


def travel_time(charge_rates, e, ev):
#print charge_rates
#Works
    dist = e[2]['weight']
    maxSpeed = e[2]['speed_limit']
    minSpeed = e[2]['speed_limit']-10
    
    x = Symbol('x')
    try:
        v_dont = solve( dist*((0.0286 * x**2 + 0.4096 * x + 107.57) * 10**(-3)) - ev)
        v_dont = getV(minSpeed, maxSpeed, v_dont[1])
    except:
        v_dont = float('inf')
    if dist*f(v_dont) > ev:
        t_dont = float('inf')
    else:
        t_dont = dist/v_dont
    ev_dont = ev-(dist*f(v_dont))
    if t_dont < float('inf') and v_dont == maxSpeed: #If we have the energy needed to drive at max speed we do so.
        #print "returned from 1: ", t_dont, charge_rates, ev_dont
        return (t_dont, charge_rates , ev_dont)
#End of works :)
#Start
    print charge_rates
    chargeStations, addedTime, addedEnergy = getChargeRate(charge_rates, dist*f(maxSpeed)) # kald indtil addedTime eller addedEnergy not eq 0.
    if not chargeStations[0]:
        t_do = float('inf')
        if t_dont < t_do:
            print "returned from 2: ", t_dont, charge_rates, ev_dont
            return (t_dont, charge_rates , ev_dont)
        else:
            print "returned from 3: ", t_do, chargeStations, ev
            return (t_do, chargeStations, ev)


    UpdateCSAfterCharging(chargeStations, addedEnergy)
    i = 0
    while (not addedTime ==  0) and i < 10000: #fix i morgen pls
        chargeStations, time, energy = getChargeRate(chargeStations, charge_rate, dist*f(maxSpeed))
        addedTime += time
        addedEnergy += energy
        if not chargeStations[0]:
            t_do = float('inf')
            if t_dont < t_do:
                print "returned from 4: ", t_dont, charge_rates, ev_dont, i
                return (t_dont, charge_rates , ev_dont)
            else:
                print "returned from 5: ", t_do, chargeStations, ev
                return (t_do, chargeStations, ev)
        UpdateCSAfterCharging(chargeStations, energy)
        if time == 0:
            break
        i += 1


    chargeRate = chargeStations[0][1] #The charging speed of the selected charging station.
    #  print dist
    y = dist/x + ((((0.0286 * x**2 + 0.4096 * x + 107.57) * 10**(-3))*dist)/chargeRate)
    yprime = y.diff()
    v_do = solve(yprime)
    v_do = getV(minSpeed, maxSpeed, v_do[0])
    t_do = dist/v_do + ((f(v_do)*dist)/chargeRate) + addedTime
    ev_do = ev + addedEnergy
#Update all charge rates by subtracting the amount of energy used from amount on all other charging stations.
    UpdateCSAfterCharging(chargeStations, dist*f(v_do))
    if t_dont < t_do:
        print "returned from 6: ", t_dont, charge_rates, ev_dont
        return (t_dont, charge_rates , ev_dont)
    else:
        print "returned from 7: ", t_do, chargeStations, ev_do
        return (t_do, chargeStations, ev_do)
#end

def fastest_path_greedy(G, s, t, ev):
    G = copy(G)

    for id,data in G.nodes(data=True):
        data['dist'] = float('inf')
        data['path'] = None
        data['preCS'] = []
        data['myCS'] = [80, data['charge_rate']]
        data['curbat'] = 0
    G.node[s]['dist'] = 0
    G.node[s]['path'] = [s]
    G.node[s]['curbat'] = 0.3
    G.node[s]['preCS'] = [[80, 20]]
    Q = sorted(G.nodes(data=True), key=lambda x: x[1]['dist'])
    while Q:
        u,data = Q[0]
        Q.remove(Q[0])
        print u, data, "\n\n"
        if data['dist'] == float('inf'):
            print "The graph is not connected"
            break
        for e in G.edges([u], data=True):
            #print data['preCS'], data['myCS']
            #returns time, new list of chargeStations and current battery level
            #print data['preCS']
            dist, pre, curbat = travel_time(copy.deepcopy(data['preCS']), e, data['curbat'])
            #print u, dist, pre, curbat
            if dist == float('inf'):
                print "The path is not possible"
                break
            node = G.node[e[1]]
            #print node['dist'], data['dist'], dist
            #print "pre:  ", pre
            if node['dist'] > data['dist'] + dist:
                #print "updataing"
                #print "updated a chargeStation"
                node['dist'] = dist + data['dist']
                node['path'].extend(data['path'])
                node['curbat'] = curbat
                #print "pre: ", pre
                if pre:
                    # print "in pre"
                    #print pre
                    node['preCS'] = cleanPreCs(pre, node['myCS'], curbat)
                #print node['preCS']
                else:
                    node['preCS'] = [node['myCS']]
                Q.sort(key=lambda x: x[1]['dist'])
# print Q
    print G.node[t]