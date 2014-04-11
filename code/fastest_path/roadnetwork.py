
import networkx as nw

class RoadNetwork(nw.Graph): 
    
    def __init__(self, params):
        super(RoadNetwork, self).__init__()
    
    def generate_charge(self):
        pass
    
    
    def charge_rate(self, node):
        pass
    
    def prune(self):
        pass
    
    
    
    
g = RoadNetwork(2, 3)

g.add_node(41)


