from time import time
from math import inf

class ia:
	def __init__(self):

	
	def build_input(self, lidar_output, camera_output, ds=10):
		output = []
		for i in range(0, 360, ds):
			for j in range(i, i + ds):
				m = inf
				if time() - lidar_output[(j + 180)%360][2] < 1 and lidar_output[(j + 180)%360][1] < m:
					m = lidar_output[(j + 180)%360][1]
			if m == inf:
				output.append(0)
			else:
				output.append(1 - m/1000)
		for i in camera_output:
			for j in i:
				output.append(j)
		return output

