import matplotlib.pyplot as plt
from math import cos, sin
from time import sleep

file = open("trajectory.dat", "r")
lines = file.readlines()
file.close()
file = open("walls.date", "r")
world = file.readlines()
file.close()

walls = []
robot = []
cond = 0
for line in world:
	if cond == 0:
		if line == '--\n':
			cond = 1
		else:
			walls.append(line[:-1].split(','))
			for i in range(len(walls[-1])):
				walls[-1][i] = float(walls[-1][i])
	else:
		robot.append(line[:-1].split(','))
		for i in range(len(robot[-1])):
			robot[-1][i] = float(robot[-1][i])
print(robot)
i = 0

for line in lines:
	if i % 1 == 0:
		a, b, c = line.split(",")
		x = float(a)
		y = float(b)
		angle = float(c)
		plt.cla()
		plt.arrow(x,y, 0.2 * cos(angle), 0.2 * sin(angle), width=0.01)
		for w in walls:
			plt.plot([w[0], w[1]], [w[2], w[3]], 'g')
		for r in robot:
			plt.plot([r[0] * cos(-angle + 1.57079632679) + x + r[2] * sin(-angle + 1.57079632679), r[1] * cos(-angle + 1.57079632679) + x + r[3] * sin(-angle + 1.57079632679)], [r[2] * cos(-angle + 1.57079632679) + y - r[0] * sin(-angle + 1.57079632679) , r[3] * cos(-angle + 1.57079632679) + y - r[1] * sin(-angle + 1.57079632679)], 'b')
		plt.pause(0.01)
		
	i += 1
plt.show()
