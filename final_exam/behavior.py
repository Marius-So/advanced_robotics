#simple one
import time
import matplotlib.pyplot as plt
import numpy as np
from random import randrange


def simulation_behaviour():
	from kinematic_simulator import kinematic_simulator
	simulator = kinematic_simulator([], [[[0,0,1.5]], [[0.5,0.5,5]], [[-0.5, 0.5, 4]]], ["red", "blue", "blue"])
	speed = [0,0]
	for i in range(600):
		if simulator.camera(0, "blue", 9)[4] == 0:
			l = simulator.lidar_sensor(0)
			a = l.index(min(l))
			if a > 180:
				speed1 = [10, -10] 
			else:
				speed1 = [-10, 10]
		else:
			speed1=[10,10]
		speed2 = [15,10]
		if simulator.robots[1][-1][0] > 1 or simulator.robots[1][-1][0] < -1 or simulator.robots[1][-1][1] > 1 or simulator.robots[1][-1][1] < -1:
			speed2 = [10,15]
		speed3 = [10,15]
		if simulator.robots[2][-1][0] > 1 or simulator.robots[2][-1][0] < -1 or simulator.robots[2][-1][1] > 1 or simulator.robots[2][-1][1] < -1:
			speed3 = [15,10]
		simulator.simulate([speed1, speed3, speed2], 0.1)
	simulator.save()
	print(simulator.fitness)


def real_behaviour():
	from hardware import input_output	
	from camera_analysis import analyse_for_colours, get_bin_detection
	io = input_output()
	pic = io.take_picture()
	masks = analyse_for_colours(pic)
	print(get_bin_detection(mask[3], 12))
	plt.imshow(pic)
	plt.show()

if __name__ == '__main__':
	simulation_behaviour()
