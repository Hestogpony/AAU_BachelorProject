speeds = [10.0,20.0,30.0,40.0,50.0,60.0,70.0,80.0,90.0]
dist = 50.0
chargingSpeed = 1000*12000.0
smallest = 1000
s = 0
for speed in range(10, 90):
	if dist/speed+((speed*speed+speed)*dist)/chargingSpeed < smallest:
		smallest = dist/speed+((speed*speed+speed)*dist)/chargingSpeed
		s = speed
	print speed, dist/speed+((speed*speed+speed)*dist)/chargingSpeed
	
print 
print s, smallest
