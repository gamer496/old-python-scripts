import os
import time

class ExecutionTime:
	def __init__(self):
		self.start_time=time.time()

	def duration(self):
		return time.time()-self.start_time

pa=raw_input("Enter the path of script to be monitored:\n")
timer=ExecutionTime()
os.system("python "+pa)
print timer.duration()