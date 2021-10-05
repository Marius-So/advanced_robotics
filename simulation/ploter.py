import matplotlib.pyplot as plt
from math import cos, sin
from time import sleep

file1 = open("trajectory.dat", "r")
lines = file1.readlines()
cornersx = [-1.1, -1.1, 1.1, 1.1]
cornersy = [-1.1, 1.1, -1.1, 1.1]

i = 0

for line in lines:
	if i % 5 == 0:
		a, b, angle = line.split(",")
		plt.cla()
		plt.arrow(float(a),float(b), 0.4 * cos(float(angle)), 0.4 * sin(float(angle)), width=0.01)
		plt.scatter(cornersx,cornersy, 0)
		plt.pause(0.01)
		
	i += 1

plt.show()

