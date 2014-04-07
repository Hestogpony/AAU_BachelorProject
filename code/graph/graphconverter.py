import networkx as nx

G=nx.read_gpickle("aalborgost.gpickle")

#paths = nx.all_simple_paths(G, source='9.96841657.0381227', target='9.932740157.0251882')
edges =  sorted(G.edges(data=True))
nodes = sorted(G.nodes())

#print edges
graph = {}
i = 0
for node in nodes:
	dct = {}
	edge = edges[i][0]
	while node == edge and i < len(edges)-1:
		if edges[i][1] != edge:
			dct[edges[i][1]] = [edges[i][2]['weight']]
		i = i + 1
		edge = edges[i][0]
	if dct:	
		if node in graph:
			graph[node].update(dct)
		else:
			graph[node] = dct

#print (graph)

def all_paths(graph, start, end, path=[]):
        path = path + [start]
        if start == end:
                return [path]
        if not start in graph:
                return []
        paths = []
	newpaths = []
        for node in graph[start]:
                if node not in path:
                        newpaths = all_paths(graph, node, end, path)
                for newpath in newpaths:
                        paths.append(newpath)
        return paths

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



path = []
for node in nodes:
	try:
		pathone = nx.shortest_path(G, '9.96841657.0381227', node)
		pathtwo = nx.shortest_path(G, node, '9.932740157.0251882')
		path.append(set(pathone + pathtwo))
	except:
		pass

print (nx.topological_sort(G))

#for edge in edges:
#	print edge[0], edge[1] 
#print list(paths)

#print sorted(G.nodes())
