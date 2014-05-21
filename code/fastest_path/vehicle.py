"""
Gammel forbrug: y= ((0.04602*x**2 +  0.6591*x + 173.1174) * 10**(-3))
Nyt forbrug: y= (0.019*x**2 - 0.770*x + 184.4 * 10**(-3))
"""	

class EV():
    def __init__(self, battery_capacity, curbat, consumption_rate):
        self.battery_capacity = battery_capacity # capacity in kWh
        self.curbat = curbat
        self.consumption_rate = consumption_rate # kwh/km

    # consumption rate in kWh/mile
    # def consumption_rate(self, speed):
    #     return (0.0286 * math.pow(speed, 2) + 0.4096 * speed + 107.57) * 10**(-3)