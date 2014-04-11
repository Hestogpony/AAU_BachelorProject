# -*- coding: utf-8 -*-
from haversine import distance

import psycopg2
import networkx as nx
import json
import webbrowser
import os

class Loader():
    def __init__(self):
        self.conn = psycopg2.connect(database="osmgraph",port='5432', host='127.0.0.1', user="mikkel", password="syrlinger")
        self.cur = self.conn.cursor()

    def create_graph(self,lonmin,latmin,lonmax,latmax):
        self.lonmin = lonmin
        self.lonmax = lonmax
        self.latmin = latmin
        self.latmax = latmax
        self.graph = nx.Graph()

    def load_graph(self):
        self.cur.execute('select n1.id, n1.lat, n1.lon, n2.id, n2.lat, n2.lon, name  from nodes as n1, nodes as n2, edges where n1.id=node1 and n2.id=node2 and n1.lon between {0} and {1} and n2.lon between {0} and {1} and n1.lat between {2} and {3} and n2.lat between {2} and {3};'.format(self.lonmin, self.lonmax, self.latmin, self.latmax))
        nexttuple = self.cur.fetchone()
        while nexttuple is not None:
            dist = distance((float(nexttuple[1]),float(nexttuple[2])),(float(nexttuple[4]),float(nexttuple[5])))
            self.graph.add_edge(nexttuple[0],nexttuple[3],weight=dist, name=nexttuple[6])
            self.graph.node[nexttuple[0]]['lon'] = str(nexttuple[2])
            self.graph.node[nexttuple[0]]['lat'] = str(nexttuple[1])
            self.graph.node[nexttuple[3]]['lon']= str(nexttuple[5])
            self.graph.node[nexttuple[3]]['lat'] = str(nexttuple[4])
            nexttuple = self.cur.fetchone()


    def street_node(self,street):
        self.cur.execute('select id from nodes, edges where (node1=id or node2=id) and name=\'{0}\''.format(street))
        return self.cur.fetchone()[0]

    def node_street(self,node):
        self.cur.execute('select name from edges where node1={0}'.format(node))
        return self.cur.fetchone()[0]

    def visualize_path(self,p):
        jsonpath = (json.dumps([{'title': str(n),'lat':self.graph.node[n]['lat'], 'lng':self.graph.node[n]['lon']} for n in p]))
        f = open('path.html','w')
        asdf = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head><title></title></head><body><script type="text/javascript" src="http://maps.googleapis.com/maps/api/js?sensor=false"></script><script type="text/javascript">var markers =%s; window.onload = function () {var mapOptions = {center: new google.maps.LatLng(markers[0].lat, markers[0].lng),zoom: 10,mapTypeId: google.maps.MapTypeId.ROADMAP};var map = new google.maps.Map(document.getElementById("dvMap"), mapOptions);var infoWindow = new google.maps.InfoWindow();var lat_lng = new Array();var latlngbounds = new google.maps.LatLngBounds();for (i = 0; i < markers.length; i++) {var data = markers[i];var myLatlng = new google.maps.LatLng(data.lat, data.lng);lat_lng.push(myLatlng);var marker = new google.maps.Marker({position: myLatlng,map: map,title: data.title,visible: false});latlngbounds.extend(marker.position);(function (marker, data) {google.maps.event.addListener(marker, "click", function (e) {infoWindow.setContent(data.description);infoWindow.open(map, marker);});})(marker, data);}map.setCenter(latlngbounds.getCenter());map.fitBounds(latlngbounds);var path = new google.maps.MVCArray();var service = new google.maps.DirectionsService();var poly = new google.maps.Polyline({ map: map, strokeColor: "#4986E7" });for (var i = 0; i < lat_lng.length; i++) {if ((i + 1) < lat_lng.length) {var src = lat_lng[i];var des = lat_lng[i + 1];path.push(src);poly.setPath(path);}}}</script><div id="dvMap" style="width: 1000px; height: 600px"></div></body></html>' % (jsonpath)
        f.write(asdf)
        f.close()
        webbrowser.open('file://' + os.path.realpath('path.html'))

    def node_street_path(self, p):
        return [self.node_street(n) for n in p]






