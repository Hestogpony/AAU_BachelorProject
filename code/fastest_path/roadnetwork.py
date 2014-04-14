import random
import networkx as nw

class RoadNetwork(nw.Graph): 
    
    def __init__(self, params):
        super(RoadNetwork, self).__init__()
    
    def generate_charge(self, min_charge, max_charge, num_of_stations):
        print("Generating" + num_of_stations + "charge stations with rates between:" + min_charge + "and" + max_charge)
        
        for i in range(0, num_of_stations):
            random_station = random.randint(0, len(self.nodes(False)))
            random_charge = random.randint(min_charge, max_charge)
            print(self.nodes(False)[random_station] + "gets:")
            self.nodes(False)[random_station]
            
        
    

    def charge_rate(self, node):
        pass
    
    def prune(self):
        pass
        
    
    

