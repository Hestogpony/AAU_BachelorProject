import xml.sax as sax
import psycopg2


class OSMIntersections (sax.ContentHandler):
    def __init__ (self):
        self.intersections = {}
        self.nodes = {}
        self.ways = 0

    def startElement (self, name, attrs):
        if name == 'way':
            self.ways += 1
        elif name == 'nd':
            ref = attrs['ref']
            if ref in self.nodes:
                self.intersections[ref] = 0
            else:
                self.nodes[ref] = 0

class OSMGraph (sax.ContentHandler):
    def __init__ (self, intersections):
        self.intersections = intersections
        self.conn = self.connect()
        self.cur = self.conn.cursor()
        self.way_id = ''
        self.way= []
        self.context = ''
        self.roadcontext = False
        self.roadtype = ''
        self.name = ''
    
    def connect(self):
        return psycopg2.connect(database="osmgraph",port='5432', host='172.31.253.80', user="d609f14", password="cocio")

    def startElement (self, name, attrs):
        if name == 'node' and attrs['id'] in self.intersections:
            self.cur.execute('INSERT INTO nodes VALUES ({0}, {1}, {2})'.format(attrs['id'],attrs['lat'], attrs['lon']))
        elif name == 'way':
            self.context = 'way'
            self.roadcontext = False
            self.way_id = attrs['id']
        elif name == 'nd' and attrs['ref'] in self.intersections:
            self.way.append(attrs['ref'])
        elif name == 'tag' and self.context == 'way':
            if 'name' == attrs['k']:
                self.name = attrs['v']
            else:
                self.name = 'unnamed'
            if 'highway' == attrs['k']:
                self.roadcontext = True
                self.roadtype = attrs['v']



    def endElement(self, name):
        if name == 'way' and self.roadcontext and self.name != 'unnamed':
            for x in xrange(len(self.way)-2):
                node1 = self.way[x]
                node2 = self.way[x+1]
                self.cur.execute(u'INSERT INTO edges VALUES ({0}, {1}, \'{2}\', {3}, \'{4}\')'.format(node1,node2, unicode(self.name.replace("'", "''")), self.way_id, self.roadtype))
            self.way = []

copenhagen = open("copenhagen.osm","r")
osmintersections = OSMIntersections()
parser = sax.make_parser()  
parser.setContentHandler(osmintersections)
parser.parse(copenhagen)
copenhagen.seek(0)
print 'go'
osmgraph = OSMGraph(osmintersections.intersections)
parser.setContentHandler(osmgraph)
parser.parse(copenhagen)
osmgraph.conn.commit()



