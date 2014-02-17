graph = { 'A' : {'B':2,'C':4},
	'B':{'C':3,'D':2},
	'C' : {'E':4},
	'D' : {'C':1},
	'E' : {'F':2},
	'F' : {'C':1}}


def sum(path):
	length = 0
	i = 0
	while i < len(path)-1 :
		length += graph[path[i]][path[i+1]]
		i = i +1
	return length
		

def find_path(graph, start, end, path=[]):
	path = path + [start]
	if start == end: 
		return path
	if not graph.has_key(start):
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


print shortest_paths(graph, 'A', 'F')
