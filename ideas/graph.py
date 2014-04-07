graph = { 'A' : {'B':[2, 3],'C':[4, 5]},
	'B':{'C':[3, 4],'D':[2,3]},
	'C' : {'E':[4,6]},
	'D' : {'C':[1,2]},
	'E' : {'F':[2,1]},
	'F' : {'C':[1,2]}}


def sum(path):
	length = 0
	i = 0
	while i < len(path)-1 :
		length +=  graph[path[i]][path[i+1]][0] 
		i = i +1
	return length
		

def find_path(graph, start, end, path=[]):
	path = path + [start]
	if start == end: 
		return path
	if not start in graph:
		return None
	shortest = None
	for node in graph[start]:
		if node not in path:
			newpath = find_path(graph, node, end, path)
			if newpath:
				if not shortest or sum(newpath) < sum(shortest):
					 shortest = newpath
	return shortest

def find_path_through(graph, start, through, end):
	startToThrough = find_path(graph, start, through)
	ThroughToEnd = find_path(graph, through, end)
	if startToThrough and ThroughToEnd:
		return list(set(startToThrough + ThroughToEnd)) 
	return None


def shortest_paths(graph,start, end):
	paths = dict()
	for node in graph:
		paths[node] = find_path_through(graph, start, node, end)
	return paths


def all_paths(graph, start, end, path=[]):
        path = path + [start]
        if start == end:
                return [path]
        if not start in graph:
                return []
        paths = []
        for node in graph[start]:
                if node not in path:
                        newpaths = all_paths(graph, node, end, path)
                for newpath in newpaths:
                        paths.append(newpath)
        return paths

class battery:
	def __init__(self, batteryLevel, batteryCap):
		self.batteryLevel = batteryLevel
		self.batteryCap = batteryCap

	def chargeCar(self, amoundCharged):
		self.batteryLevel += amoundCharged		
	
def optipath(path=[], initialbattery=0, batterycap=85):
	chargeStations = { 'A' : 10,
			   'B' : 12,
			   'C' : 10,
			   'D' : 13,
			   'E' : 9, 
			   'F' : 0} 
	bat = battery(initialbattery, batterycap)
	range = 0

def inrange(bat=battery(0,85), path=[]):
	inrange = []
	#while battery.batteryLevel > 

	
def getlengths(path=[], graph=[]):
	vertecis = graph
	tuples = dict()
	for p in path:	
		print (p)
		print(vertecis[p])
		vertecis = graph[p]
		#print(p, vertecis)

getlengths(all_paths(graph, 'A', 'F')[1], graph)
print (shortest_paths(graph, 'A', 'F'))
#print (optipath())

#print (all_paths(graph, 'A', 'F'))
