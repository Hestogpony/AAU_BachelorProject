
import importer
import networkx as nx
from fastest_path.vehicle import EV
from fastest_path.roadnetwork import RoadNetwork
from fastest_path.rn_al import fastest_path_greedy
from test_utils import *
import time



def experiment_driving_dist(ev, CS_density, max_distance):
    print 'loading roadnetwork'
    rn = RoadNetwork(nx.read_gpickle('pickle_experiment'))
    set_roadnetwork_complexity(rn, 500000)
    print 'reducing cs density'
    charge_station_density(rn, CS_density)

    f = open('path_time_length(1-500).csv', 'a')
    f.write('dist,time,fail_rate\n')
    for distance in range(250, max_distance, 50):
        for x in xrange(1):
            s,t,dist = s_and_t(rn, distance)
            print s,t,dist
            ################ NAIVE 1
            #naive1_p, naive1_t = naive(rn,s, t, ev)
            ################
            #naive2_p, naive2_t = get_navie_path(rn,s,t, ev)
            ################ GREEDY
            greedy_p,greedy_t = fastest_path_greedy(rn, s, t, 1, ev)
            ################ LP

            ################
            #rn.visualize_path(naive1_p)
            rn.visualize_path(greedy_p)
            #rn.visualize_path(naive2_p)

            print greedy_t#, naive2_t

        # f.write('%s,%s,%s\n' % (distance, sum_time/10.0, fails/10.0))
    f.close()

def experiment_driving_dist2(ev, CS_density,min_dist, max_dist, step_size, iterations, file_name='driving_dist.csv'):
    rn = RoadNetwork(nx.read_gpickle('pickle_experiment'))
    charge_station_density(rn, CS_density)

    with open(file_name, 'a') as f:
        f.write('driving distance,naive-time,naive-fail,hybrid-time, hybrid-fail,greedy-time,greedy-fail\n')

    for distance in range(min_dist, max_dist, step_size):
        print 'driving distance experiment. currently at: ', distance
        naive_t, hybrid_t, greedy_t = 0,0,0
        naive_f, hybrid_f, greedy_f = 0,0,0
        for iteration in xrange(iterations):
            s, t, dist = s_and_t(rn, distance)

            ### NAIVE
            #_, time = naive_path(rn, s, t, ev)
            #naive_t += time if time!=float('inf') else 0
            #naive_f += 0 if time!=float('inf') else 1
            ### LP
            # _, time = fastest_path_greedy(rn, s, t, 2, ev) # 3 for LP
            # hybrid_t += time if time!=float('inf') else 0
            # hybrid_f += 0 if time!=float('inf') else 1

            ### Greedy
            _, time = fastest_path_greedy(rn, s, t, 1, ev) # 1 for slope
            greedy_t += time if time!=float('inf') else 0
            greedy_f += 0 if time!=float('inf') else 1

        with open(file_name, 'a') as f:
            f.write('%s,%s,%s,%s,%s,%s,%s\n' % (
                                              distance,
                                             # naive_t/(iterations-naive_f) if iterations != naive_f else 'inf',
                                             # naive_f,
                                              '.',#   hybrid_t/(iterations-hybrid_f) if iterations != hybrid_f else 'inf',
                                              '.',#   hybrid_f,
                                              greedy_t/(iterations-greedy_f) if iterations != greedy_f else 'inf',
                                              greedy_f,
                                              ))

road_network = RoadNetwork(nx.read_gpickle('pickle_experiment'))
ev = EV(80, 80, lambda x: ((0.04602*x**2+0.6591*x + 173.1174)* 10**(-3)))

#experiment_cs_density(ev, 10, 100)

# experiment_runtime_compexity(ev, 1, 100, 200, 20)

#experiment_ev_consumption(10, 100, 40)

#experiment_charge_rate(road_network, ev, 10, 100, 50)

experiment_driving_dist(ev, 30, 500)

