import subprocess

def getSlope(lowerX, higherX, lowerY, higherY):
    return (higherY-lowerY)/(higherX-lowerX)

def LPprinter(ChargeConstants, edgeDists, edgeSpeeds, Precision, ev):
    n = "param n := {0};\n".format(len(edgeDists))
    m = "param m := {0}; \n".format(Precision)
    initialBat = "param initialBat := {0};\n".format(ev.curbat)
    batCap = "param batCap := {0}; \n".format(ev.battery_capacity)
    points = "param points: \n"
    points2 = "param points2: \n"
    linesA = "param linesA: \n"
    linesB = "param linesB: \n"
    speedDists = "param speedDistanceRelation: \n 1 2 := \n"
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
        points2 += higherXes + "\n"
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
    proc = subprocess.Popen("glpsol --model fastestPathLinearization.mod --data LPData.dat", stdout=subprocess.PIPE, shell=True)

    pathTime = float('inf')
    pathCurbat = 0
    for line in iter(proc.stdout.readline, ''):
        #print line
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

def linearProgramming(G, nodes, ev, curbat):
    ChargeConstants = []
    edgeDists = []
    edgeSpeeds = []
    numOfcs = 0
    cs = []
    for i in range(0,len(nodes)-1):
        if G.node[nodes[i]]['charge_rate'] > 0:
            numOfcs += 1
            cs.append(G.node[nodes[i]]['charge_rate'])
        ChargeConstants.append(G.node[nodes[i]]['charge_rate'])
        edge = G.edge[nodes[i]][nodes[i+1]]
        edgeSpeeds.append(edge['speed_limit'])
        edgeDists.append(edge['weight'])
    print "Total cs", numOfcs, cs
    #print ChargeConstants, edgeDists
    #print edge
    #ChargeConstants.append(G.node[nodes[-1]]['charge_rate'])
    #print ChargeConstants, len(ChargeConstants)
    #print edgeSpeeds, len(edgeSpeeds)
    #print edgeDists, len(edgeDists)
    time, newcurbat = LPprinter(ChargeConstants, edgeDists, edgeSpeeds, 20, ev)
    return time, newcurbat
    # print G.node[preNode]['charge_rate'], G.node[curNode]['charge_rate']