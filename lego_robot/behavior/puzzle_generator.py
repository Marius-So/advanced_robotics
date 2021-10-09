from sokobanSolver import State, SokobanSolver
from random import randint
import time
import matplotlib.pyplot as plt
import numpy as np
import statistics
import csv 

size = 5 #samples
maxSizeBoard = 20
infil = 0

# this is the puzzle generator
def generate_all(x, y, ncans, prob):
	cans = []
	target = []
	robot = (0, 1)
	walls = []
	while len(cans) < ncans:
		n = (1, x - 2)
		if n not in cans and n != robot:
			cans.append(n)
	while len(target) < ncans:
		n = (y-1, x - 1)
		if n not in cans and n not in target and n != robot:
			target.append(n)
	board = []
	for i in range(y):
		new_line = []
		for j in range(x):
			new_line.append(0)
		board.append(new_line)
	while len(walls) < prob * x * y:
		n = (randint(0, y-1), randint(0,x - 1))
		if n not in cans and n not in target and n != robot and n not in walls:
			walls.append(n)
			board[n[0]][n[1]] = 1
	return [board, cans, target, robot]

if __name__ == "__main__":
	# this code here runs the solver experiment
	time_1_can = []
	time_2_can = []
	real_time_1_can = []
	real_time_2_can = []
	for i in range(4, maxSizeBoard):
		print('Size: ' + str(i))
		time_1_can.append([])
		real_time_1_can.append([])
		for j in range(size):
			print("Iteration: " + str(j))
			a = generate_all(i, i, 1, infil)
			init_state = State(a[1],a[3], -1)
			solver = SokobanSolver(a[0], a[2], a[3], a[1])
			solver.printStateFancy(init_state)
			a = time.time()
			time_1_can[-1].append(len(solver.solve_sokoban(init_state)))
			real_time_1_can[-1].append(time.time() - a)
			del(init_state)
			del(solver)
	for i in range(4, 4):
		print('Size: ' + str(i))
		time_2_can.append([])
		real_time_2_can.append([])
		for j in range(size):
			print("Iteration: " + str(j))
			a = generate_all(i, i, 2, infil)
			init_state = State(a[1],a[3], -1)
			solver = SokobanSolver(a[0], a[2], a[3], a[1])
			solver.printStateFancy(init_state)
			solver.solve_sokoban(init_state)
			a = time.time()
			time_2_can[-1].append(len(solver.solve_sokoban(init_state)))
			real_time_2_can[-1].append(time.time() - a)
			del(init_state)
			del(solver)

average_1_can = []
for i in time_1_can:
	average_1_can.append(0)
	for j in i:
		average_1_can[-1] += j / size

average_time_1_can = []
for i in real_time_1_can:
	average_time_1_can.append(0)
	for j in i:
		average_time_1_can[-1] += j / size

average_time_2_can = []
for i in real_time_2_can:
	average_time_2_can.append(0)
	for j in i:
		average_time_2_can[-1] += j / size

average_2_can = []
for i in time_2_can:
	average_2_can.append(0)
	for j in i:
		average_2_can[-1] += j / size

ecart_type_1 = []
for i in range(len(average_1_can)):
	ecart_type_1.append(0)
	for j in time_1_can[i]:
		ecart_type_1[-1] += (average_1_can[i] - j) ** 2
	ecart_type_1[-1] = (ecart_type_1[-1] / size) ** 0.5

ecart_type_2 = []
for i in range(len(average_2_can)):
    ecart_type_2.append(0)
    for j in time_2_can[i]:
        ecart_type_2[-1] += (average_2_can[i] - j) ** 2
    ecart_type_2[-1] = (ecart_type_2[-1] / size) ** 0.5

ecart_type_real_1 = []
for i in range(len(average_time_1_can)):
	ecart_type_real_1.append(0)
	for j in real_time_1_can[i]:
		ecart_type_real_1[-1] += (average_time_1_can[i] - j) ** 2
	ecart_type_real_1[-1] = (ecart_type_real_1[-1] / size) ** 0.5

ecart_type_real_2 = []
for i in range(len(average_time_2_can)):
	ecart_type_real_2.append(0)
	for j in real_time_2_can[i]:
		ecart_type_real_2[-1] += (average_time_2_can[i] - j) ** 2
	ecart_type_real_2[-1] = (ecart_type_real_2[-1] / size) ** 0.5

with open("data1can.csv", 'w') as myfile:
	wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
	for i in range(len(average_1_can)):
		wr.writerow([i+4, average_1_can[i], ecart_type_1[i], average_time_1_can[i], ecart_type_real_1[i]])

with open("data2can.csv", 'w') as myfile:
	wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
	for i in range(len(average_2_can)):
		wr.writerow([i+4, average_2_can[i], ecart_type_2[i], average_time_2_can[i], ecart_type_real_2[i]])

print(real_time_1_can)

plt.show()
