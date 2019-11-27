from decimal import Decimal

def simulate(mode, arrival, service, network, fogTimeLimit, fogTimeToCloudTime, time_end):

	def my_round(x, n):	
		temp_1 = Decimal(str(x))
		temp_2 = round(temp_1, n)
		return float(temp_2)

	def display(time, job_number, event, next_arrival_at_fog, fog_next_depart, network_next_depart, \
	cloud_next_depart, fog_jobs, network_jobs, cloud_jobs):
		time = my_round(time, 5)
		next_arrival_at_fog = round(next_arrival_at_fog, 5)
		fog_next_depart = round(fog_next_depart, 5)
		network_next_depart = round(network_next_depart, 5)
		cloud_next_depart = round(cloud_next_depart, 5)
		for job in fog_jobs:
			job[2] = my_round(job[2], 5)
		for job in network_jobs:
			job[2] = my_round(job[2], 5)
		for job in cloud_jobs:
			job[2] = my_round(job[2], 5)
		print('At time t = {:.4f}|| event = \'job {} {}\'|| next_arrival_at_fog = {}, fog_next_depart = {}, \
network_next_depart = {}, cloud_next_depart = {}, fog_jobs = {}, network_jobs = {}, cloud_jobs = {}.'
.format(time, job_number, event, next_arrival_at_fog, fog_next_depart, network_next_depart, \
cloud_next_depart, fog_jobs, network_jobs, cloud_jobs))

	def new_display(time, job_number, event):
		time = my_round(time, 5)
		print("At time t = {:.4f}, event = \'{} {}\'".format(time, job_number, event))

	def update_fog_next_depart(fog_jobs, time):	#update fog_next_depart.
		if fog_jobs:
			fog_next_depart = time + len(fog_jobs) * min([job[2] for job in fog_jobs])
		else:
			fog_next_depart = float('Inf')
		return fog_next_depart

	def update_network_next_depart(network_jobs, time):	#update network_next_depart.
		if network_jobs:
			network_next_depart = time + min([job[2] for job in network_jobs])
		else:
			network_next_depart = float('Inf')
		return network_next_depart

	def update_cloud_next_depart(cloud_jobs, time):	#update cloud_next_depart.
		if cloud_jobs:
			cloud_next_depart = time + len(cloud_jobs) * min([job[2] for job in cloud_jobs])
		else:
			cloud_next_depart = float('Inf')
		return cloud_next_depart


	time = 0 	# starting time
	event = ''
	# 3 lists record the jobs in fog, network and cloud.
	fog_jobs = []
	network_jobs = []
	cloud_jobs = []

	# 4 types times: 1 for arrival event, 3 for departure event.
	if arrival == []:
		next_arrival_at_fog = float('Inf')
	else:
		next_arrival_at_fog = arrival[0]	# starting time
	fog_next_depart = float('Inf')		# set to infinite as fog_jobs is empty in the beginning.
	network_next_depart = float('Inf')
	cloud_next_depart = float('Inf')
	request = list(range(1, len(arrival) + 1)) # [1, 2, 3, 4, 5, 6]

	#**************************************************************************************************
	total_work_time = 0		#used to calculate mean response time
	fog_dep = []
	net_dep = []
	cloud_dep = []

	while (next_arrival_at_fog != float('Inf') or fog_jobs != [] or network_jobs != [] or \
	cloud_jobs != []):
		if time == 0:
			time = next_arrival_at_fog
			event = 'arrivals at fog'

			job_number = arrival.index(time) + 1  # job_number = index + 1.
			fog_actual_service_time = min(service[job_number - 1], fogTimeLimit) # fog 真实服务时间

			fog_jobs.append([job_number, time, fog_actual_service_time]) # new comer job
			next_arrival_at_fog = arrival[1]  # as event is arrival, need to update next_arrival_at_fog
			
			#update fog_next_depart, network_next_depart, cloud_next_depart
			fog_next_depart = update_fog_next_depart(fog_jobs, time)
			network_next_depart = update_network_next_depart(network_jobs, time)
			cloud_next_depart = update_cloud_next_depart(cloud_jobs, time)

	# 		display(time, job_number, event, next_arrival_at_fog, fog_next_depart, network_next_depart, \
	# cloud_next_depart, fog_jobs, network_jobs, cloud_jobs)
			#new_display(time, job_number, event)
		
		last_time = time 	# record last_time stage
		time = min(next_arrival_at_fog, fog_next_depart, network_next_depart, cloud_next_depart)
		if time == next_arrival_at_fog:
			event = 'arrivals at fog'
		if time == fog_next_depart:
			event = 'departs from fog'
		if time == network_next_depart:
			event = 'departs from network to cloud'
		if time == cloud_next_depart:
			event = 'departs from cloud'

		#**************************************************************************************************
		if event == 'arrivals at fog':	
		#update：next_arrival_at_fog, fog_jobs, work left for each job, fog/network/cloud_next_depart
			for job in fog_jobs:	# update work left
				job[2] -= (time - last_time) / len(fog_jobs)
			job_number = arrival.index(time) + 1	# 1, 2, 3, 4, 5, 6
			fog_actual_service_time = min(service[job_number - 1], fogTimeLimit) # fog actual service time
			fog_jobs.append([job_number, time, fog_actual_service_time])	# new comer job

			for job in network_jobs:	# update work left
				job[2] -= (time - last_time)
			for job in cloud_jobs:	# update work left
				job[2] -= (time - last_time) / len(cloud_jobs)

			if arrival.index(next_arrival_at_fog) + 1 < len(arrival):
				next_arrival_at_fog = arrival[arrival.index(next_arrival_at_fog) + 1]
			else:	#确定下一次到fog的arrival时间
				next_arrival_at_fog = float('Inf')

			# update fog_next_depart, network_next_depart, cloud_next_depart.
			fog_next_depart = update_fog_next_depart(fog_jobs, time)
			network_next_depart = update_network_next_depart(network_jobs, time)
			cloud_next_depart = update_cloud_next_depart(cloud_jobs, time)

	# 		display(time, job_number, event, next_arrival_at_fog, fog_next_depart, network_next_depart, \
	# cloud_next_depart, fog_jobs, network_jobs, cloud_jobs)
			#new_display(time, job_number, event)

		#**************************************************************************************************
		if event == 'departs from fog':	
		#update内容：fog_jobs, network_jobs, work left for each job, fog/network/cloud_next_depart
			for job in fog_jobs:	# update work left
				#job[2] -= (time - last_time) / len(fog_jobs)
				job[2] = round(job[2] - (time - last_time) / len(fog_jobs), 5)
			for job in network_jobs:	# update work left
				job[2] -= (time - last_time)
			for job in cloud_jobs:	# update work left
				job[2] -= (time - last_time) / len(cloud_jobs)

			for job in fog_jobs:	# find out which one left fog
				if job[2] == 0:
					job_number = job[0]
					fog_jobs.remove(job)	# update fog_job：delete the left job

			if network[job_number - 1] == 0:
				event = 'departs from fog'
				# the job finishes, update total_work_time.
				total_work_time += (time - arrival[job_number - 1])
			else:
				event = 'departs from fog to network'
				network_jobs.append([job_number, time, network[job_number - 1]])
				# update network_jobs：append the new comer job

			# a job left fog, update fog_dep.
			fog_dep.append([arrival[job_number - 1], time])

			#update fog_jobs, network_jobs, cloud_jobs
			fog_next_depart = update_fog_next_depart(fog_jobs, time)
			network_next_depart = update_network_next_depart(network_jobs, time)
			cloud_next_depart = update_cloud_next_depart(cloud_jobs, time)

	# 		display(time, job_number, event, next_arrival_at_fog, fog_next_depart, network_next_depart, \
	# cloud_next_depart, fog_jobs, network_jobs, cloud_jobs)
			#new_display(time, job_number, event)

		#**************************************************************************************************
		if event == 'departs from network to cloud':
		#update：network_jobs, cloud_jobs, 每个job的剩余工作时间, fog/network/cloud_next_depart
			for job in fog_jobs:	# update fog_jobs 中每个 job 的剩余工作时间
				job[2] -= (time - last_time) / len(fog_jobs)
			for job in network_jobs:	# update network_jobs 中每个 job 的剩余工作时间
				#job[2] -= (time - last_time)
				job[2] = round(job[2] - (time - last_time), 5)
			for job in cloud_jobs:	# update cloud_jobs 中每个 job 的剩余工作时间
				job[2] -= (time - last_time) / len(cloud_jobs)

			for job in network_jobs:	#找出是哪个 job 离开 network 去 cloud 了
				if job[2] == 0:
					job_number = job[0]
					network_jobs.remove(job)	# update network_job：删去离开的 job

			# 有 job 离开 network, update net_dep.
			net_dep.append([arrival[job_number - 1], time])

			cloud_service_time = fogTimeToCloudTime * (service[job_number - 1] - fogTimeLimit)
			cloud_jobs.append([job_number, time, cloud_service_time])

			#update fog_jobs, network_jobs, cloud_jobs 中的 job 的剩余工作时间
			fog_next_depart = update_fog_next_depart(fog_jobs, time)
			network_next_depart = update_network_next_depart(network_jobs, time)
			cloud_next_depart = update_cloud_next_depart(cloud_jobs, time)

	# 		display(time, job_number, event, next_arrival_at_fog, fog_next_depart, network_next_depart, \
	# cloud_next_depart, fog_jobs, network_jobs, cloud_jobs)
			#new_display(time, job_number, event)

		#**************************************************************************************************
		if event == 'departs from cloud':
		#update内容：cloud_jobs, 每个job的剩余工作时间, fog/network/cloud_next_depart
			for job in fog_jobs:	# update fog_jobs 中每个 job 的剩余工作时间
				job[2] -= (time - last_time) / len(fog_jobs)
			for job in network_jobs:	# update network_jobs 中每个 job 的剩余工作时间
				job[2] -= (time - last_time)
			for job in cloud_jobs:	# update cloud_jobs 中每个 job 的剩余工作时间
				job[2] = round(job[2] - (time - last_time) / len(cloud_jobs), 5)
				#job[2] -= (time - last_time) / len(cloud_jobs)

			for job in cloud_jobs:	# find out which job left cloud
				if job[2] == 0:
					job_number = job[0]
					# the job finishes, update total_work_time.
					total_work_time += (time - arrival[job_number - 1])
					cloud_jobs.remove(job)	# update cloud_jobs：删去离开的 job

			# a job left cloud, update cloud_dep.
			cloud_dep.append([arrival[job_number - 1], time])

			#update fog_jobs, network_jobs, cloud_jobs 中的 job 的剩余工作时间
			fog_next_depart = update_fog_next_depart(fog_jobs, time)
			network_next_depart = update_network_next_depart(network_jobs, time)
			cloud_next_depart = update_cloud_next_depart(cloud_jobs, time)

	# 		display(time, job_number, event, next_arrival_at_fog, fog_next_depart, network_next_depart, \
	# cloud_next_depart, fog_jobs, network_jobs, cloud_jobs)
			#new_display(time, job_number, event)
			mean_response_time = total_work_time / len(arrival)
	#print()
	#print("mean response time = {:.4f}".format(mean_response_time))
	mean_response_time = '%4.4f'%mean_response_time		
	for e in fog_dep:
		e[0] = round(e[0], 4)
		e[1] = round(e[1], 4)
	for e in net_dep:
		e[0] = round(e[0], 4)
		e[1] = round(e[1], 4)
	for e in cloud_dep:
		e[0] = round(e[0], 4)
		e[1] = round(e[1], 4)
	fog_dep = sorted(fog_dep, key = lambda x:x[0])	# sort in arrival
	net_dep = sorted(net_dep, key = lambda x:x[0])
	cloud_dep = sorted(cloud_dep, key = lambda x:x[0])

	for e in fog_dep:		
		e[0] = '%.4f'%e[0]	
		e[1] = '%.4f'%e[1]
	for e in net_dep:
		e[0] = '%.4f'%e[0]
		e[1] = '%.4f'%e[1]
	for e in cloud_dep:
		e[0] = '%.4f'%e[0]
		e[1] = '%.4f'%e[1]

	# print('fog_dep = {}'.format(fog_dep))
	# print('net_dep = {}'.format(net_dep))
	# print('cloud_dep = {}'.format(cloud_dep))

	return mean_response_time, fog_dep, net_dep, cloud_dep