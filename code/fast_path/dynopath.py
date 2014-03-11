""" Script for finding a dynamic programming solution to the optimal solution to a path """


def g(min, speed):
	return min*(4*speed+49)/1000

def f(energy, min, chargingSpeed):
	if (energy/80) < 0.8:
		return min*chargingSpeed
	else: 
		return min*(0.4*chargingSpeed)




nodes = [10, 22, 10, 11, 8, 10]
edges = [16, 40, 8, 4, 43, 9]
maxspeed = [50, 50, 100, 50, 50, 30]

def findOptimal(x, i, j, k, z):
	if i == len(nodes)-1:
		return 0
	if j == len(nodes)-1 and z > g(edges[j],maxspeed[j]):
		return 0
	if z < 0:
		return 10000
	if 120 < z:
		return 10000
	if  x > maxspeed[j]:
		return 10000
	else:
		test =  min(k + findOptimal(maxspeed[j], i, j, k+5, z+f(z,k,nodes[i])), edges[j] + findOptimal(maxspeed[j+1], i+1, j+1, 0, g(edges[j], x)))   
		return test

print findOptimal(maxspeed[0], 0, 0, 0, 20)
