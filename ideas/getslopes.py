lowestSpeed = 64.0
highestSpeed = 80.0
edgeDist = [70.0]
slopes = []
for x in range(0, len(edgeDist)):
	a = ((edgeDist[x]/highestSpeed) - (edgeDist[x]/lowestSpeed))/(highestSpeed-lowestSpeed)
	b = a*lowestSpeed+(edgeDist[x]/lowestSpeed)
	print x+1, a, b


def f(v):
    return (0.0286 * v**2 + 0.4096 * v + 107.57) * 10**(-3)


x = 86.4
x2 = 90

#75.6    79.2    82.8    86.4    90

y = f(x)
y2 = f(x2)
slope = (y2-y)/(x2-x)

konstant = y-slope*x
print konstant, slope