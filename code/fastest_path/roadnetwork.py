import random
import networkx as nw
import json
import webbrowser
import os
import time

class RoadNetwork(nw.Graph): 
    
    def __init__(self):
        super(RoadNetwork, self).__init__()
    
    # Generates random charge rates between min_charge and max_charge
    # on n = num_of_stations random stations 
    def generate_charge(self, min_charge, max_charge, density):
        print("Generating charge rates between: " + str(min_charge) + " and " + str(max_charge) + " for every " + str(density) + " nodes")
        counter = 0
        for node_id in self.nodes():

            if counter % density == 0:
                
                random_charge_rate = random.randint(min_charge, max_charge)
                self.node[node_id]['charge_rate'] = random_charge_rate
            else:
                self.node[node_id]['charge_rate'] = 0
            counter += 1
    
    
    #Scales all roads in a new instance of a road network by scale_factor
    #returns the new instance of the road network: road_network
    def scale_road_network(self, scale_factor):
        road_network = self
        print("scaling distancens by: " + str(scale_factor))
        for edge in road_network.edges(data = True):
            new_dist = edge['weight'] * scale_factor
            edge['weight'] = new_dist
        return road_network
    
    def charge_rate(self, node_id):
        return self.node[node_id]['charge_rate']
        
    def visualize(self):
        json_rn = (json.dumps([{'title': str(node),'lat':self.node[node]['lat'], 'lng':self.node[node]['lon'], 'charge_rate':self.node[node]['charge_rate']} for node in self.nodes()]))
        f = open('path.html','w')
        asdf = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head><title></title></head><body><script type="text/javascript" src="http://maps.googleapis.com/maps/api/js?sensor=false"></script><script type="text/javascript">var markers =%s; window.onload = function () {var mapOptions = {center: new google.maps.LatLng(markers[0].lat, markers[0].lng),zoom: 10,mapTypeId: google.maps.MapTypeId.ROADMAP};var map = new google.maps.Map(document.getElementById("dvMap"), mapOptions);var infoWindow = new google.maps.InfoWindow();var lat_lng = new Array();var latlngbounds = new google.maps.LatLngBounds();for (i = 0; i < markers.length; i++) {var data = markers[i];if (data.charge_rate > 0) {var myLatlng = new google.maps.LatLng(data.lat, data.lng);lat_lng.push(myLatlng);var marker = new google.maps.Marker({position: myLatlng,map: map,title: data.title,visible: true});latlngbounds.extend(marker.position);(function (marker, data) {google.maps.event.addListener(marker, "click", function (e) {infoWindow.setContent(data.description);infoWindow.open(map, marker);});})(marker, data);}}map.setCenter(latlngbounds.getCenter());map.fitBounds(latlngbounds);var path = new google.maps.MVCArray();var service = new google.maps.DirectionsService();var poly = new google.maps.Polyline({ map: map, strokeColor: "#4986E7" });/*for (var i = 0; i < lat_lng.length; i++) {if ((i + 1) < lat_lng.length) {var src = lat_lng[i];var des = lat_lng[i + 1];path.push(src);poly.setPath(path);}}*/}</script><div id="dvMap" style="width: 1000px; height: 600px"></div></body></html>' % (json_rn)
        f.write(asdf)
        f.close()
        webbrowser.open('file://' + os.path.realpath('path.html'))

    def visualize_path(self,p):
        jsonpath = (json.dumps([{'title': str(n),'lat':self.node[n]['lat'], 'lng':self.node[n]['lon']} for n in p]))
        f = open('path.html','w')
        asdf = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head><title></title></head><body><script type="text/javascript" src="http://maps.googleapis.com/maps/api/js?sensor=false"></script><script type="text/javascript">var markers =%s; window.onload = function () {var mapOptions = {center: new google.maps.LatLng(markers[0].lat, markers[0].lng),zoom: 10,mapTypeId: google.maps.MapTypeId.ROADMAP};var map = new google.maps.Map(document.getElementById("dvMap"), mapOptions);var infoWindow = new google.maps.InfoWindow();var lat_lng = new Array();var latlngbounds = new google.maps.LatLngBounds();for (i = 0; i < markers.length; i++) {var data = markers[i];var myLatlng = new google.maps.LatLng(data.lat, data.lng);lat_lng.push(myLatlng);var marker = new google.maps.Marker({position: myLatlng,map: map,title: data.title,visible: false});latlngbounds.extend(marker.position);(function (marker, data) {google.maps.event.addListener(marker, "click", function (e) {infoWindow.setContent(data.description);infoWindow.open(map, marker);});})(marker, data);}map.setCenter(latlngbounds.getCenter());map.fitBounds(latlngbounds);var path = new google.maps.MVCArray();var service = new google.maps.DirectionsService();var poly = new google.maps.Polyline({ map: map, strokeColor: "#4986E7" });for (var i = 0; i < lat_lng.length; i++) {if ((i + 1) < lat_lng.length) {var src = lat_lng[i];var des = lat_lng[i + 1];path.push(src);poly.setPath(path);}}}</script><div id="dvMap" style="width: 1000px; height: 600px"></div></body></html>' % (jsonpath)
        f.write(asdf)
        f.close()
        time.sleep(1)
        webbrowser.open('file://' + os.path.realpath('path.html'))
