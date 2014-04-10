def getLines(function, range, presion): 
	xmin = range[0]
	xmax = range[1]
	points = []
	slopes = []
	konstants = []
	x = xmin
	x2 = 0
	while x+presion < xmax:
		y = function(x)
		x2 = x + presion	
		y2 = function(x2)
		points.append([x,x2])
		slope = (y2-y)/(x2-x)
		slopes.append(slope)
		konstant = y-slope*x
		konstants.append(konstant)
		x = x2
	return slopes, points, konstants

def f(x):
	return 0.0286*x*x + 0.4096*x + 107.57

points = []
points1 = []
linea = []
lineb = []
def produceData(speedLimits, presion):

	for speedLimit in speedLimits:
		data = getLines(f, (speedLimit-30,speedLimit), presion)
		#print data
		ps = []
		ps1 = []
		aa = []
		bs = []
		for a in data[0]:
			aa.append(a)
		
		for b in data[2]:
			bs.append(b)

		for p in data[1]:
			ps.append(p[0])
			ps1.append(p[1])

		points.append(ps)
		points1.append(ps1)
		linea.append(aa)
		lineb.append(bs)			
	
file = open("data.dat", "w")
def printOutput(ps):
	
	i = 1
	printpoints = ""
	for point in ps:
		printpoints += str(i) + "\t"
		for p in point:
			printpoints += str(round(p, 2)) + "\t"
		printpoints += "\n"
		i += 1	
	print printpoints
	file.write(printpoints)
		
speedLimits = []
for i in range(0, 152):
	speedLimits.append(100)
produceData(speedLimits, 2)
printOutput(points)
printOutput(points1)
printOutput(linea)
printOutput(lineb)
file.close()
