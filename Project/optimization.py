from simulation import simulate
from decimal import Decimal
import random
import numpy
from math import log
import matplotlib.pyplot as plt

def get_service_time(alpha_1, alpha_2, beta):
    power = 1 / (1 - beta)
    base = random.random() * (alpha_2 ** (1 - beta) - alpha_1 ** (1 - beta)) + alpha_1 ** (1 - beta)
    return base ** power

def get_information(lambd, alpha_1, alpha_2, beta, mu_1, mu_2, random_seed):
    arrival = []
    network = []
    service = []
    random.seed(random_seed)	
    next_arrival_time = -log(1 - random.random()) / float(lambd)
    next_service_time = get_service_time(alpha_1, alpha_2, beta)
    while next_arrival_time < 1000:
        arrival.append(next_arrival_time)
        service.append(next_service_time)
        next_arrival_time = next_arrival_time + (-log(1 - random.random()) / float(lambd))
        next_service_time = get_service_time(alpha_1, alpha_2, beta)

    length = len(arrival)
    network = numpy.random.uniform(mu_1, mu_2, length).tolist()

    return arrival, service, network


fogTimeLimit = 0
flag = 1
my_seed = 1
fog_time_limit_list = []
mrt_list = []
count = 1
while fogTimeLimit < 0.20:
    flag += 1
    fogTimeLimit += 0.01
    if flag % 10 == 0:
        my_seed += 1
    arrival, service, network = get_information(lambd=9.72, alpha_1=0.01, alpha_2=0.4, beta=0.86, 
    	mu_1=1.200, mu_2=1.470, random_seed=my_seed)
    mrt = simulate("random", arrival, service, network, fogTimeLimit, fogTimeToCloudTime=0.6, time_end =1000)[0]
    fog_time_limit_list.append(fogTimeLimit)
    mrt_list.append(float(mrt))
    count += 1
    print("count: ",count)

plt.plot(fog_time_limit_list, mrt_list)
plt.show()

