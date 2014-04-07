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


def produceData(speedLimits, presion):
	for speedLimit in speedLimits:
		data = getLines(f, (speedLimit-10, speedLimit), presion)
		points =  data[1]
		for point in points:
			print point[0]
		print 
	print "Split"
	for speedLimit in speedLimits:
		data = getLines(f, (speedLimit-10, speedLimit), presion)
		points =  data[1]
                for point in points:
                        #print point[1]
			pass
                
		print data[2]
		
speedLimits = [50, 40, 70, 30, 90, 50, 55,  12]
produceData(speedLimits, 2)

#print getLines(f, (70*0.7, 70), 5)
