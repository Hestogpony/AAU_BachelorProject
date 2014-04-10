
import networkx as nw

class Road_network(nw.Graph): 
    
    def __init__(self, node, params):
        super(Road_network, self).__init__()
    
    def generate_charge(self):
        pass
    
    def max_velocity(self):
        pass
    
    def fastest_path_optimal(self):
        pass
    
    def fastest_path_naive(self):
        pass
    
    def charge_rate(self, node):
        pass
    

g = Road_network(2, 3)

g.add_node(41)

print(g.nodes())

