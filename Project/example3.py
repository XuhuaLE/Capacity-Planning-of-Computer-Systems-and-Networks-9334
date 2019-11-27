from decimal import Decimal

def my_round(x, n):	# 对 x 四舍五入保留 n 位小数
	temp_1 = Decimal(str(x))
	temp_2 = round(temp_1, n)
	return float(temp_2)

def display(time, job_number, event, next_arrival_at_fog, fog_next_depart, network_next_depart, \
cloud_next_depart, fog_jobs, network_jobs, cloud_jobs):
	time = my_round(time, 5)	# 四舍五入保留5位小数
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

def update_fog_next_depart(fog_jobs, time):	#更新 fog_next_depart.
	if fog_jobs:
		fog_next_depart = time + len(fog_jobs) * min([job[2] for job in fog_jobs])
	else:
		fog_next_depart = float('Inf')
	return fog_next_depart

def update_network_next_depart(network_jobs, time):	#更新 network_next_depart.
	if network_jobs:
		network_next_depart = time + min([job[2] for job in network_jobs])
	else:
		network_next_depart = float('Inf')
	return network_next_depart

def update_cloud_next_depart(cloud_jobs, time):	#更新 cloud_next_depart.
	if cloud_jobs:
		cloud_next_depart = time + len(cloud_jobs) * min([job[2] for job in cloud_jobs])
	else:
		cloud_next_depart = float('Inf')
	return cloud_next_depart


#fogTimeLimit = 2	# fog service time limit for a job.
#fogTimeToCloudTime = 0.6 	# fog -> cloud service time ratio.

fogTimeLimit = 2.5	# fog service time limit for a job.
fogTimeToCloudTime = 0.7 	# fog -> cloud service time ratio.

time = 0 	# starting time
event = ''
# 3 lists record the jobs in fog, network and cloud.
fog_jobs = []
network_jobs = []
cloud_jobs = []

#arrival_time_at_fog = [1.1, 6.2, 7.4, 8.3, 9.1, 10.1]
#service_time_at_fog = [4.1, 5.2, 1.3, 2.0, 3.2, 4.1]
#network_latency = [1.5, 1.3, 0, 0, 1.6, 1.8]

arrival_time_at_fog = [1, 2, 4, 5, 6]
service_time_at_fog = [3.7, 5.1, 1.3, 2.4, 4.5]
network_latency = [1.5, 1.4, 0, 0, 1.6]

# 4 types times: 1 for arrival event, 3 for departure event.
if arrival_time_at_fog == []:
	next_arrival_at_fog = float('Inf')
else:
	next_arrival_at_fog = arrival_time_at_fog[0]	# starting time
fog_next_depart = float('Inf')		# set to infinite as fog_jobs is empty in the beginning.
network_next_depart = float('Inf')
cloud_next_depart = float('Inf')
request = list(range(1, len(arrival_time_at_fog) + 1)) # [1, 2, 3, 4, 5, 6]

#**************************************************************************************************
cycle = 0	# 防止无限循环
while (next_arrival_at_fog != float('Inf') or fog_jobs != [] or network_jobs != [] or \
cloud_jobs != []) and cycle <= 30:
	cycle += 1
	if time == 0:
		time = next_arrival_at_fog
		event = 'arrivals at fog'

		job_number = arrival_time_at_fog.index(time) + 1  # 看是哪个 job 到达了，注意 job_number = index + 1.
		fog_actual_service_time = min(service_time_at_fog[job_number - 1], fogTimeLimit) # fog 真实服务时间

		fog_jobs.append([job_number, time, fog_actual_service_time]) # 新来的 job
		next_arrival_at_fog = arrival_time_at_fog[1]  # 由于 event 是 arrival, 需要更新 next_arrival_at_fog
		
		#更新 fog_next_depart, network_next_depart, cloud_next_depart
		fog_next_depart = update_fog_next_depart(fog_jobs, time)
		network_next_depart = update_network_next_depart(network_jobs, time)
		cloud_next_depart = update_cloud_next_depart(cloud_jobs, time)

		display(time, job_number, event, next_arrival_at_fog, fog_next_depart, network_next_depart, \
cloud_next_depart, fog_jobs, network_jobs, cloud_jobs)
	
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
	# 还有其他情况：某一时刻发生多个动作：一个request到达fog，另一个request离开network，等等。

	#**************************************************************************************************
	if event == 'arrivals at fog':	
	#更新内容：next_arrival_at_fog, fog_jobs, 每个jobs的剩余工作时间, fog/network/cloud_next_depart
		for job in fog_jobs:	# 每个job需要更新剩余所需工作时间
			job[2] -= (time - last_time) / len(fog_jobs)
		job_number = arrival_time_at_fog.index(time) + 1	# 1, 2, 3, 4, 5, 6
		fog_actual_service_time = min(service_time_at_fog[job_number - 1], fogTimeLimit) # fog 真实服务时间
		fog_jobs.append([job_number, time, fog_actual_service_time])	# 这是新来的job

		for job in network_jobs:	# 每个job需要更新剩余所需工作时间
			job[2] -= (time - last_time)
		for job in cloud_jobs:	# 每个job需要更新剩余所需工作时间
			job[2] -= (time - last_time) / len(cloud_jobs)

		if arrival_time_at_fog.index(next_arrival_at_fog) + 1 < len(arrival_time_at_fog):
			next_arrival_at_fog = arrival_time_at_fog[arrival_time_at_fog.index(next_arrival_at_fog) + 1]
		else:	#确定下一次到fog的arrival时间
			next_arrival_at_fog = float('Inf')

		# 更新 fog_next_depart, network_next_depart, cloud_next_depart.
		fog_next_depart = update_fog_next_depart(fog_jobs, time)
		network_next_depart = update_network_next_depart(network_jobs, time)
		cloud_next_depart = update_cloud_next_depart(cloud_jobs, time)

		display(time, job_number, event, next_arrival_at_fog, fog_next_depart, network_next_depart, \
cloud_next_depart, fog_jobs, network_jobs, cloud_jobs)

	#**************************************************************************************************
	if event == 'departs from fog':	
	#更新内容：fog_jobs, network_jobs（可能会变动）, 每个job的剩余工作时间, fog/network/cloud_next_depart
		for job in fog_jobs:	# 更新 fog_jobs 中每个 job 的剩余工作时间
			#job[2] -= (time - last_time) / len(fog_jobs)
			job[2] = round(job[2] - (time - last_time) / len(fog_jobs), 5)
		for job in network_jobs:	# 更新 network_jobs 中每个 job 的剩余工作时间
			job[2] -= (time - last_time)
		for job in cloud_jobs:	# 更新 cloud_jobs 中每个 job 的剩余工作时间
			job[2] -= (time - last_time) / len(cloud_jobs)

		for job in fog_jobs:	#找出是哪个 job 离开了fog
			if job[2] == 0:
				job_number = job[0]
				fog_jobs.remove(job)	# 更新 fog_job：删去离开的 job

		if network_latency[job_number - 1] == 0:
			event = 'departs from fog'
		else:
			event = 'departs from fog to network'
			network_jobs.append([job_number, time, network_latency[job_number - 1]])
			# 更新 network_jobs：添加新来的 job

		#更新 fog_jobs, network_jobs, cloud_jobs 中的 job 的剩余工作时间
		fog_next_depart = update_fog_next_depart(fog_jobs, time)
		network_next_depart = update_network_next_depart(network_jobs, time)
		cloud_next_depart = update_cloud_next_depart(cloud_jobs, time)

		display(time, job_number, event, next_arrival_at_fog, fog_next_depart, network_next_depart, \
cloud_next_depart, fog_jobs, network_jobs, cloud_jobs)


	#**************************************************************************************************
	if event == 'departs from network to cloud':
	#更新内容：network_jobs, cloud_jobs, 每个job的剩余工作时间, fog/network/cloud_next_depart
		for job in fog_jobs:	# 更新 fog_jobs 中每个 job 的剩余工作时间
			job[2] -= (time - last_time) / len(fog_jobs)
		for job in network_jobs:	# 更新 network_jobs 中每个 job 的剩余工作时间
			#job[2] -= (time - last_time)
			job[2] = round(job[2] - (time - last_time), 5)
		for job in cloud_jobs:	# 更新 cloud_jobs 中每个 job 的剩余工作时间
			job[2] -= (time - last_time) / len(cloud_jobs)

		for job in network_jobs:	#找出是哪个 job 离开 network 去 cloud 了
			if job[2] == 0:
				job_number = job[0]
				network_jobs.remove(job)	# 更新 network_job：删去离开的 job
		cloud_service_time = fogTimeToCloudTime * (service_time_at_fog[job_number - 1] - fogTimeLimit)
		cloud_jobs.append([job_number, time, cloud_service_time])

		#更新 fog_jobs, network_jobs, cloud_jobs 中的 job 的剩余工作时间
		fog_next_depart = update_fog_next_depart(fog_jobs, time)
		network_next_depart = update_network_next_depart(network_jobs, time)
		cloud_next_depart = update_cloud_next_depart(cloud_jobs, time)

		display(time, job_number, event, next_arrival_at_fog, fog_next_depart, network_next_depart, \
cloud_next_depart, fog_jobs, network_jobs, cloud_jobs)

	#**************************************************************************************************
	if event == 'departs from cloud':
	#更新内容：cloud_jobs, 每个job的剩余工作时间, fog/network/cloud_next_depart
		for job in fog_jobs:	# 更新 fog_jobs 中每个 job 的剩余工作时间
			job[2] -= (time - last_time) / len(fog_jobs)
		for job in network_jobs:	# 更新 network_jobs 中每个 job 的剩余工作时间
			job[2] -= (time - last_time)
		for job in cloud_jobs:	# 更新 cloud_jobs 中每个 job 的剩余工作时间
			job[2] = round(job[2] - (time - last_time) / len(cloud_jobs), 5)
			#job[2] -= (time - last_time) / len(cloud_jobs)

		for job in cloud_jobs:	# 找出是哪个 job 离开 cloud 了
			if job[2] == 0:
				job_number = job[0]
				cloud_jobs.remove(job)	# 更新 cloud_jobs：删去离开的 job

		#更新 fog_jobs, network_jobs, cloud_jobs 中的 job 的剩余工作时间
		fog_next_depart = update_fog_next_depart(fog_jobs, time)
		network_next_depart = update_network_next_depart(network_jobs, time)
		cloud_next_depart = update_cloud_next_depart(cloud_jobs, time)

		display(time, job_number, event, next_arrival_at_fog, fog_next_depart, network_next_depart, \
cloud_next_depart, fog_jobs, network_jobs, cloud_jobs)
