lowestSpeed = 70
highestSpeed = 98
edgeDist = [50.0, 4.0, 41.0, 100.0, 5.2, 4.0, 209.0, 20.0, 30.0, 7.0]
slopes = []
for x in range(0, len(edgeDist)):
	a = ((edgeDist[x]/highestSpeed) - (edgeDist[x]/lowestSpeed))/(highestSpeed-lowestSpeed)
	b = a*lowestSpeed+(edgeDist[x]/lowestSpeed)
	print x+1, a, b
