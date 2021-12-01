import matplotlib.pyplot as plt
from math import cos, sin
from time import sleep

file = open("trajectory.dat", "r")
lines = file.readlines()
file.close()
file = open("walls.dat", "r")
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

s = len(lines)
i = 0
while i < s:
	plt.cla()
	plt.scatter([-1, -1, 1,1], [-1,1,1,-1])
	for w in walls:
		plt.plot([w[0], w[1]], [w[2], w[3]], 'g')
	while (lines[i] != '---\n'):
		a, b, c = lines[i].split(",")
		x = float(a)
		y = float(b)
		angle = float(c)
		for r in robot:
			if y > - 100:
				plt.plot([r[0] * cos(-angle) + x + r[2] * sin(-angle), r[1] * cos(-angle) + x + r[3] * sin(-angle)], [r[2] * cos(-angle) + y - r[0] * sin(-angle) , r[3] * cos(-angle) + y - r[1] * sin(-angle)], 'b')
		i += 1
	i += 101
	plt.pause(0.01)
