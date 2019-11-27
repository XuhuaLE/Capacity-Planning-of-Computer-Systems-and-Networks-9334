import sys

def display(time, event, next_arrival_time, next_departure_time, job_list):
	time = round(time, 1)	# 四舍五入保留一位小数
	next_arrival_time = round(next_arrival_time, 1)
	next_departure_time = round(next_departure_time, 1)
	for job in job_list:
		job[1] = round(job[1], 1)
	transfer_job_list = [tuple(job) for job in job_list]
	print('At time t = {}, event = \'{}\', next arrival time = {}, \
next departure time = {}, job list = {}.'
.format(time, event, next_arrival_time, next_departure_time, transfer_job_list))

arrival_time = [1, 2, 3, 5, 15] # arrival_time_at_fog
service_time = [2.1, 3.3, 1.1, 0.5, 1.7] # service_time_at_fog

time = 0 # master_clock
job_list = []
event = '' # event_type
next_arrival_time = 0
next_departure_time = float('Inf')
current_index = 0
request = list(range(1, len(arrival_time) + 1)) # running jobs: job 1, job 2...
# [1, 2, 3, 4, 5]
#cycle = 0	# 防止无限循环
while request: # and cycle <= 30:
	#cycle += 1
	if time == 0 and arrival_time[0] != 0:	# the start stage
		next_arrival_time = arrival_time[0]
		display(time, event, next_arrival_time, next_departure_time, job_list)
	last_time = time # record last time stage
	time = min(next_arrival_time, next_departure_time)
	if next_arrival_time <= next_departure_time:
		event = 'arrival'
	if next_arrival_time >= next_departure_time:
		event = 'departure'
	#if next_arrival_time == next_departure_time: # 一个 job 离开，一个 job 到达
	#	pass
	if event == 'arrival':
		current_index = request[0] - 1
		for job in job_list:	# 每个在 job_list 的 job 的 time left 都减去这段时间的完成工作量
			job[1] -= (time - last_time) / len(job_list)
		#job_list.append([time, 这里是这个 job 的 service time]) # new comer
		job_list.append([time, service_time[current_index + len(job_list)]]) # new comer
		next_departure_time = time + len(job_list) * min([e[1] for e in job_list]) 
		if current_index + len(job_list) < len(arrival_time):	# normal case
			next_arrival_time = arrival_time[current_index + len(job_list)]	# 下一个 arrival 时间
		else:	# special case: no more arrivals, which means that the next arrival time is inifite
			next_arrival_time = float('Inf')
		display(time, event, next_arrival_time, next_departure_time, job_list)

	if event == 'departure':
		for job in job_list:
			job[1] -= (time - last_time) / len(job_list)
		for job in job_list:
			if job[1] == min(e[1] for e in job_list):
				departure_job = job_list.index(job)
		request.remove(arrival_time.index(job_list[departure_job][0]) + 1)
		job_list.pop(departure_job)
		if job_list:
			next_departure_time = time + len(job_list) * min([e[1] for e in job_list])
		else:
			next_departure_time = float('Inf') 
		display(time, event, next_arrival_time, next_departure_time, job_list)