# -*- coding: utf-8 -*-
import psycopg2
import re
import networkx as nx
from operator import itemgetter
from haversine import distance

class OSMLoader():
    def __init__(self,xmin,ymin,xmax,ymax):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.conn = self.connect()
        self.cur = self.conn.cursor()
        self.intersection = []

    def connect(self):
        return psycopg2.connect(database="osm",port='5432', host='127.0.0.1', user="mikkel", password="syrlinger")

    def intersections(self):
        #self.cur.execute('select line1.name, line2.name, st_xmin(line1.way), st_ymin(line1.way) from planet_osm_line as line1 join planet_osm_line as line2 on st_xmin(line1.way)=st_xmin(line2.way) and st_ymin(line1.way)=st_ymin(line2.way) where line1.way && St_makeenvelope(%s,%s,%s,%s) and line1.name!=line2.name order by line1.name, line1.ref ;' % (self.xmin, self.ymin, self.xmax, self.ymax))
        self.out = []
        self.cur.execute('select a.name, b.name, st_astext(st_intersection(a.way, b.way)), a.osm_id from planet_osm_line as a, planet_osm_line as b where a.way && St_makeenvelope({0},{1},{2},{3}) and b.way && St_makeenvelope({0},{1},{2},{3}) and st_intersects(a.way, b.way)=\'t\' and a.name != b.name;'.format(self.xmin, self.ymin, self.xmax, self.ymax))

        print 'done'
        nextintersection = self.cur.fetchone()
        while nextintersection != None:
            if ('MULTI' not in nextintersection[2]):
                dct = {'wayID':nextintersection[3], 'from': nextintersection[0], 'to': nextintersection[1]}
                point = re.sub("[^0-9,. ]", "", nextintersection[2])
                dct['x'] = point.split(" ")[0]
                dct['y'] = point.split(" ")[1]
                self.out.append(dct)
            nextintersection = self.cur.fetchone()
        return sorted(self.out, key=itemgetter('wayID', 'x', 'y'))

    def ways(self):
        self.cur('select name, st_ymin(way), st_xmin(way) from planet_osm_line where planet_osm_line.way && St_makeenvelope(%s%s%s%s);' % (self.xmin, self.ymin, self.xmax, self.ymax))

    def toGraph(self):
        self.graph = nx.Graph()
        e = self.intersections()
        print len(e)
        for i in range(0, len(e)-2):
            wayID = e[i]['wayID']
            #print e[i]
            while e[i+1]['wayID'] == wayID:
                self.graph.add_edge(e[i]['x']+e[i]['y'], e[i+1]['x']+e[i+1]['y'], weight=distance((float(e[i]['x']), float(e[i]['y'])),(float(e[i+1]['x']), float(e[i+1]['y']))))
                #self.graph.add_edge(e[i]['from']+e[i]['to'], e[i]['to']+e[i]['from'], weight=0)
                #G.add_edge('s','1',weight=200, speed_limit=20)
                i = i+1
                if i == len(e)-1:
                    break
        



#print i-1, entries[i-1]['wayID'], entries[i-1]['from'], entries[i-1]['to'], entries[i-1]['x'] 
#print i, entries[i]['wayID'], entries[i]['from'], entries[i]['to'], entries[i]['x'] 
#self.graph.add_edge(entry[0]['from'], entry['to']+entry['wayID'])
osmloader = OSMLoader(9.931589,57.014727,10.013458,57.049189)

printer = osmloader.toGraph()

path = nx.shortest_path(osmloader.graph, '9.96841657.0381227', '9.932740157.0251882', weight='weight')
print path

dist = 0
for x in xrange(0,len(path)-2):
    dist += 1
    #dist += osmloader.graph[path[x]][path[x+1]]['weight']
print dist
print osmloader.graph


def all_paths(graph, start, end, path=[] ):
    path = path + [start]
    if start == end:
        return [path]
    if not start in graph:
        return []
    paths = []
    
    for node in graph[start]:
        newpaths = []        
        if node not in path:
            newpaths = all_paths(graph, node, end, path)
        for newpath in newpaths:
            paths.append(newpath)
    return paths

print all_paths(osmloader.graph, '9.96841657.0381227', '9.932740157.0251882')
#print all_paths(osmloader.graph, '9.96841657.0381227', '9.932740157.0251882')

#print list(nx.all_simple_paths(osmloader.graph, source='9.96841657.0381227', target='9.932740157.0251882', cutoff=2*dist))



# path = nx.shortest_path(osmloader.graph, '9.96841657.0381227', '9.932740157.0251882')




