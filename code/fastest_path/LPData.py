batteryCap = 50
Precision = 5
ChargeConstants = [10, 0 , 0, 0, 0 , 15, 12, 0, 15, 0, 0, 0, 0, 0, 0, 0, 0,20 ,0 ,0,0 ,0 ,0]
edgeDists = [10, 80 , 5, 2, 4 , 15, 12, 5, 15, 3, 4, 6, 2, 7, 10, 1, 2,20 ,9 ,4,5 ,2 ,3]
edgeSpeeds = [90, 80,101, 116 , 115, 112, 114 , 110, 120, 50, 100, 73, 84, 80, 50, 70, 100, 100, 102,120 ,90 ,40,50]

def consumption_rate(v):
	return ((0.0286 * v**2 + 0.4096 * v + 107.57) * 10**(-3))

def getSlope(lowerX, higherX, lowerY, higherY):
	return (higherY-lowerY)/(higherX-lowerX)

points = "param points: \n"
points2 = "param points2: \n"
linesA = "param linesA: \n"
linesB = "param linesB: \n"
speedDists = "param speedDistanceRelation: \n 1		2 := \n"
edgeDist = "param edgeDist := "
chargeConstants = "param chargeConstants := "
rangeList = ""
for i in range(0, len(edgeDists)):
	edgeDist += "%s %s, " % ((i+1), edgeDists[i])
	chargeConstants += "%s %s, " % ((i+1), ChargeConstants[i])
	rangeList += "%s " % (i+1)
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
		slope = getSlope(lowerX, higherX, consumption_rate(lowerX), consumption_rate(higherX))
		lineA += "%s " % slope
		lineB += "%s " % (consumption_rate(higherX)-slope*higherX)
		minSpeed += stepSize

	points += lowerXes + "\n"
	points2 +=  higherXes + "\n"
	speedDists += speedDist + "\n"
	linesA += lineA + "\n"
	linesB += lineB + "\n"

print points + ";"
print points2 + ";"
print speedDists + ";"
print linesA + ";"
print linesB + ";"
print edgeDist + ";"
print chargeConstants + ";"
