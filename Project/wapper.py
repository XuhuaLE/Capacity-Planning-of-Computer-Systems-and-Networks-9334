from simulation import simulate
from decimal import Decimal
import random
import numpy
from math import log

test_folder = './sample_files/'
#my_output_files = './my_output_files'
def run_simulation(test_number, ramdom_seed):
	with open(test_folder + 'mode_' + str(test_number) + '.txt') as file:
		mode = file.readline().strip()

	with open(test_folder + 'para_' + str(test_number) + '.txt') as file:
		n = 0	# used to count the line number
		time_end = None
		for line in file:
			line = line.strip('\n')	# get rid of '\n'
			n += 1
			if n == 1:
				fogTimeLimit = float(line)
			if n == 2:
				fogTimeToCloudTime = float(line)
			if n == 3:
				if mode == 'random':
					time_end = float(line)

	with open(test_folder + 'arrival_' + str(test_number) + '.txt') as file:
		if mode == 'trace':
			arrival = []
			for line in file:
				line = line.strip('\n')	# get rid of '\n'
				arrival.append(float(line))
		if mode == 'random':
			for line in file:
				line = line.strip('\n')	# get rid of '\n'
				if line:
					arrival = line

	with open(test_folder + 'service_' + str(test_number) + '.txt') as file:
		service = []
		for line in file:
			line = line.strip('\n')	# get rid of '\n'
			service.append(float(line))

	with open(test_folder + 'network_' + str(test_number) + '.txt') as file:
		network = []
		for line in file:
			line = line.strip('\n')	# get rid of '\n'
			network.append(float(line))


	if mode == 'trace':
		mrt, fog_dep, net_dep, cloud_dep = simulate(mode, arrival, service, network, \
fogTimeLimit, fogTimeToCloudTime, time_end)
	if mode == 'random':

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
		    while next_arrival_time < time_end:
		        arrival.append(next_arrival_time)
		        service.append(next_service_time)
		        next_arrival_time = next_arrival_time + (-log(1 - random.random()) / float(lambd))
		        next_service_time = get_service_time(alpha_1, alpha_2, beta)

		    length = len(arrival)
		    network = numpy.random.uniform(mu_1, mu_2, length).tolist()

		    return arrival, service, network

		arrival, service, network = get_information(arrival, service[0], service[1], service[2], \
													network[0], network[1], 0)

		mrt, fog_dep, net_dep, cloud_dep = simulate(mode, arrival, service, network, \
fogTimeLimit, fogTimeToCloudTime, time_end)


	# write out the output files to current directory
	#mrt
	with open("mrt_" + str(test_number) + ".txt", "w") as file:
	    file.write(mrt)
	# fog_dep
	with open("fog_dep_" + str(test_number) + ".txt", "w") as file:
	    for departure_time in fog_dep:
	        file.write(str(departure_time[0]) + "\t" + str(departure_time[1]) + "\n")
	# net_dep
	with open("net_dep_" + str(test_number) + ".txt", "w") as file:
	    for departure_time in net_dep:
	        file.write(str(departure_time[0]) + "\t" + str(departure_time[1]) + "\n")
	# cloud_dep
	with open("cloud_dep_" + str(test_number) + ".txt", "w") as file:
	    for departure_time in cloud_dep:
	        file.write(str(departure_time[0]) + "\t" + str(departure_time[1]) + "\n")


with open(test_folder + "num_tests.txt") as file:
    num_tests = int(file.readline())

for test_number in range(1, num_tests + 1):
	run_simulation(test_number, 0)


#run_simulation(4, 0)
