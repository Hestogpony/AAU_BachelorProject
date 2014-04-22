import copy
from sympy import *


def fastest_path_optimal():
    pass

def fastest_path_naive():
    pass

def f(x):
    return (0.0286 * math.pow(x, 2) + 0.4096 * x + 107.57) * 10**(-3)

def function():
    pass

def travel_time(charge_rates, e, v, curbat):
    print charge_rates
    dist = e[2]['weight'] 
    x = Symbol('x')
    print dist
    y = dist/x + ((((0.0286 * x**2 + 0.4096 * x + 107.57) * 10**(-3))*dist)/charge_rates[0][1])
    print y
    yprime = y.diff()
    test = solve(yprime)
    print yprime
    print test
    dist = e[2]['weight'] 
    #print dist/v + (0.0286*2 * x + 0.4096) * 10**(-3)*dist

def fastest_path_greedy(G,s, ev):
    G = copy.copy(G)

    for id,data in G.nodes(data=True):
        data['dist'] = float('inf')
        data['path'] = []
        data['bestCS'] = [(0, data['charge_rate'])]
    G.node[s]['dist'] = 0
    G.node[s]['path'] = [s]
    Q = sorted(G.nodes(data=True), key=lambda x: x[1]['dist'])
    while Q:
        u,data = Q[0]
        Q.remove(Q[0])
        if data['dist'] == float('inf'):
            break
        for e in G.edges([u], data=True):
            alt = travel_time(data['bestCS'], e, G.node[e[1]], ev)



        