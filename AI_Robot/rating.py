import numpy as np
import random
from kinematic_simulator import kinematic_simulator

class rate:
	def __init__(self, Q, s=1, time=0.1, iteration=200):
		self.Q = Q
		self.time = time
		self.iteration = iteration
		walls = [[-s/2, -s/2, -s/2, s/2], [s/2, s/2, -s/2, s/2], [-s/2, s/2, s/2, s/2], [-s/2, s/2, -s/2, -s/2]]
		self.simulator = kinematic_simulator(walls, [[0,0,0]])

	
	def activate(self, a):
		if a == 0:
			self.coo.extend(self.simulator.simulate(self.coo[-1][0], self.coo[-1][1], self.coo[-1][2], speed, -speed, time))
		if a == 1:
			self.coo.extend(self.simulator.simulate(self.coo[-1][0], self.coo[-1][1], self.coo[-1][2], -speed, speed, time))
		if a == 2:
			self.coo.extend(self.simulator.simulate(self.coo[-1][0], self.coo[-1][1], self.coo[-1][2], speed, speed, time))
		if a == 3:
			self.coo.extend(self.simulator.simulate(self.coo[-1][0], self.coo[-1][1], self.coo[-1][2], -speed, -speed, time))


	def getState(self):
		lecture = self.simulator.thymio_sensor(self.coo[-1][0], self.coo[-1][1], self.coo[-1][2])
		for i in range(0, 7):
			if lecture[i] == 99999999:
				lecture[i] = 0
		if lecture[0] < lecture[2] and lecture[2] < lecture[4]:
			return 0
		if lecture[0] > lecture[2] and lecture[2] > lecture[4]:
			return 1
		if lecture[0] == lecture[2] and lecture[2] == lecture[4] and lecture[4] == 0:
			return 2
		else:
			return 3

	def getBestAction(self, state):
    	#print(Q)
		best = 0
		bestindex = 0
		for i in range(len(self.Q[state])):
			if self.Q[state][i]>best:
				best = self.Q[state][i]
				bestindex = i
		return bestindex

	def Q_rate(self):
		score = 0
		for i in range(iterations):
			s = getState()
			a = getBestAction(s)
			if a == 2:
				score += 1
			elif a == 2:
				score -= 1
			activate(a)
		return score - self.simulator.n_collision * 20
	
