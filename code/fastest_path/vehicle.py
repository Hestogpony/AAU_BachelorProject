

class ElectricalVehicle(object):
    def __init__(self, battery_capacity):
        self.battery_capacity = battery_capacity # capacity in kWh
        
    # consumption rate in kWh/mile
    def consumption_rate(self, speed): 
        return (0.0286 * math.pow(speed, 2) + 0.4096 * speed + 107.57) * 10**(-3)
        