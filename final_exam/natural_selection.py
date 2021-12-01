from NN import NN
import numpy as np
from kinematic_simulator import kinematic_simulator
from random import randint, random

class learn:
	def __init__(self):
		self.s_genes = 792
		self.s_input = 76
		self.seeker_genes = np.random.random(self.s_genes)
		self.avoider_genes = np.random.random(self.s_genes)
		self.best_seeker_genes = [self.seeker_genes, 0]
		self.best_avoider_genes = [self.avoider_genes, 0]

	def learn(self):
		for simulation in range(1, 1001):
			print(simulation)
			evolve_seeker = (self.best_avoider_genes[1] > self.best_seeker_genes[1])
			if evolve_seeker == True:
				self.seeker_genes = np.copy(self.best_seeker_genes[0])
				for i in range(2000//simulation):
					self.seeker_genes[randint(0, self.s_genes - 1)] = random()
				self.seeker_nn = NN(self.seeker_genes, 76, 10, 2)
				self.avoider_nn = NN(self.best_avoider_genes[0], 76,10,2)
			else:
				self.avoider_genes = np.copy(self.best_avoider_genes[0])
				for i in range(2000//simulation):
					self.avoider_genes[randint(0, self.s_genes - 1)] = random()
				self.seeker_nn = NN(self.best_seeker_genes[0], 76, 10, 2)
				self.avoider_nn = NN(self.avoider_genes, 76, 10, 2)
			self.simulator = kinematic_simulator([], [[[0,0,1.5]], [[0.5,0.5,5]], [[-0.5, 0.5, 4]]], ["red", "blue", "blue"])
			for i in range(180):
				a = self.simulator.lidar_sensor(0)
				b = [self.simulator.camera(0, "red", 8), self.simulator.camera(0, "yelow", 8), self.simulator.camera(0, "blue", 8), self.simulator.camera(0, "green", 8), self.simulator.camera(0, "purple", 8)]
				d = build_input(a,b)
				speed1 = self.seeker_nn.forward_propagation(d)
				a = self.simulator.lidar_sensor(1)
				b = [self.simulator.camera(1, "red", 8), self.simulator.camera(1, "yelow", 8), self.simulator.camera(1, "blue", 8), self.simulator.camera(1, "green", 8), self.simulator.camera(1, "purple", 8)]
				d = build_input(a,b)
				speed2 = self.avoider_nn.forward_propagation(d)
				a = self.simulator.lidar_sensor(2)
				b = [self.simulator.camera(2, "red", 8), self.simulator.camera(2, "yelow", 8), self.simulator.camera(2, "blue", 8), self.simulator.camera(2, "green", 8), self.simulator.camera(2, "purple", 8)]
				d = build_input(a,b)
				speed3 = self.avoider_nn.forward_propagation(d)
				self.simulator.simulate([speed1, speed2, speed3], 1)
			del self.seeker_nn
			del self.avoider_nn
			if evolve_seeker == True:
				if self.simulator.fitness[0] > self.best_seeker_genes[1]:
					self.best_seeker_genes = [np.copy(self.seeker_genes), self.simulator.fitness[0]]
					self.best_avoider_genes[1] = 0.5*self.simulator.fitness[1] + 0.5*self.simulator.fitness[2]
					print(self.best_seeker_genes)
			else:
				if self.simulator.fitness[1] + self.simulator.fitness[2] > 2*self.best_avoider_genes[1]:
					self.best_avoider_genes = [np.copy(self.avoider_genes), 0.5*self.simulator.fitness[1] + 0.5*self.simulator.fitness[2]]
					self.best_seeker_genes[1] = self.simulator.fitness[0]
					print(self.best_avoider_genes)
			print(self.simulator.fitness)
			self.simulator.save()
			del self.simulator

def build_input(lidar_output, camera_output, ds=10):
	output = []
	for i in range(0, 360, ds):
		for j in range(i, i + ds):
			m = float('inf')
			if lidar_output[(j + 180)%360] != 999999999:
				m = lidar_output[(j + 180)%360]
		if m == float('inf'):
			output.append(0)
		else:
			output.append(1 - m/1000)
	for i in camera_output:
		for j in i:
			output.append(j)
	return output

if __name__ == "__main__":
	a = learn()
	a.learn()	
