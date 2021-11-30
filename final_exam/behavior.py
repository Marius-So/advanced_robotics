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
				speed = [10, -10] 
			else:
				speed = [-10, 10]
		else:
			speed=[10,10]
		simulator.simulate([speed, [randrange(40)-20, randrange(40)-20], [randrange(40)-20,randrange(40)-20]], 0.1)
	simulator.save()


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
