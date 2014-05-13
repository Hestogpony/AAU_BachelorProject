import copy
from sympy import *
from operator import itemgetter

x = Symbol('x')
dist = 80
chargeRate = 50
ev = 0


def consumption_rate(v):
    return ((0.0286 * v**2 + 0.4096 * v + 107.57) * 10**(-3))

try:
    v_dont = solve( dist*((0.0286 * x**2 + 0.4096 * x + 107.57) * 10**(-3)) - ev)
    t_dont = dist/v_dont[0]
except: 
    pass
y = dist/x + ((((0.0286 * x**2 + 0.4096 * x + 107.57) * 10**(-3))*dist)/chargeRate)
yprime = y.diff()
v_do = solve(yprime)
print v_do
v_do = v_do[0]
v_do = 60
print dist*consumption_rate(v_do)
t_do = dist/v_do + ((consumption_rate(v_do)*dist)/chargeRate)

print "hvis vi ikke lader er v: ", v_dont[0]
print "Hvis vi lader er v: ", v_do

print "hvis vi ikke lader er time: ", t_dont
print "hvis vi lader er time: ", t_do