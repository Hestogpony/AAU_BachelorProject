"""
Generate bounding boxes of varying sizes - 10km to Denmark
Produce S and T vertice, at the edge of the problem - something like 100 times
Make sure two execusions generate the same results:
	Use the same bounding box and the same nodes as charge stations with the same charge speeds
return runtime
"""
def scale_road_network(road_network, scale_factor):
	print("scaling distancens by: " + str(scale_factor))
	for edge in road_network.edges(data = True):
		new_dist = edge['weight'] * scale_factor
		edge['weight'] = new_dist
