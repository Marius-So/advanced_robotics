from sokobanSolver import State, SokobanSolver
from random import randint
import time
import matplotlib.pyplot as plt
import numpy as np


# this is the puzzle generator
def generate_all(min, max, ncans, prob):
	x = randint(min,max)
	y = randint(min,max)
	cans = []
	target = []
	robot = (-1, -1)
	while len(cans) < ncans:
		n = (randint(1,y - 2), randint(1,x - 2))
		if n not in cans:
			cans.append(n)
	while len(target) < ncans:
		n = (randint(0,y - 1), randint(0,x - 1))
		if n not in cans and n not in target:
			target.append(n)
	while robot == (-1, -1):
		r = (randint(0,y - 1), randint(0,x - 1))
		if r not in cans:
			robot = r
	board = []
	for i in range(y):
		new_line = []
		for j in range(x):
			if (j,i) not in cans and (j,i) not in target and (j,i) != robot:
				a = randint(0,prob)
				if a == 0:
					new_line.append(1)
				else:
					new_line.append(0)
			else:
				new_line.append(0)
		board.append(new_line)
	return [board, cans, target, robot]

if __name__ == "__main__":
	# this code here runs the solver experiment
	time_1_can = []
	time_2_can = []
	size = []
	for i in range(4, 12):
		time_1_can.append(0)
		size.append(i)
		for j in range(30):
			a = generate_all(i, i + 1, 1, 6)
			init_state = State(a[1],a[3], -1)
			solver = SokobanSolver(a[0], a[2], a[3], a[1])
			print(i)
			a = time.time()
			solver.solve_sokoban(init_state)
			time_1_can[-1] += (time.time() - a) / 30
			del(init_state)
			del(solver)
	for i in range(4, 6):
		time_2_can.append(0)
		for j in range(30):
			a = generate_all(i, i + 1, 2, 6)
			init_state = State(a[1],a[3], -1)
			solver = SokobanSolver(a[0], a[2], a[3], a[1])
			print(i)
			a = time.time()
			solver.solve_sokoban(init_state)
			time_2_can[-1] += (time.time() - a) / 30
			del(init_state)
			del(solver)
	for i in range(6,12):
		time_2_can.append(np.nan)
	print("---------------------")
	plt.plot(size, time_1_can, )
	plt.plot(size, time_2_can)
	plt.show()
