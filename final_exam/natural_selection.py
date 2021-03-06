from NN import NN
import numpy as np
from kinematic_simulator import kinematic_simulator
from random import randint, random
import os
from datetime import datetime
from behaviour_avoider import get_simu_behaviour

nbin = 5
h = 2.5
w = 2.5
#walls = [[-w/2, -w/2, -h/2, h/2], [w/2, w/2, -h/2,h/2],[-w/2,w/2,h/2,h/2],[-w/2,w/2,-h/2,-h/2]]
walls=[]

class learn:
	def __init__(self):
		self.s_genes = 510
		self.s_input = 39
		if os.path.isfile("seeker.txt"):
			self.seeker_genes = np.loadtxt("seeker.txt", delimiter=", ")
		else:
			self.seeker_genes = np.random.random(self.s_genes)
		if os.path.isfile("avoider.txt"):
			self.avoider_genes = np.loadtxt("avoider.txt", delimiter=", ")
		else:
			self.avoider_genes = np.random.random(self.s_genes)
		self.best_seeker_genes = [self.seeker_genes, -99999]
		self.best_avoider_genes = [self.avoider_genes, -99999]

	def learn(self, how_much_time):
		for simulation in range(1, 999999):
			print(simulation)
			if True:
				self.seeker_genes = np.copy(self.best_seeker_genes[0])
				if simulation > 1:
					print("evolve seeker")
					for i in range(len(self.seeker_genes)):
						if random() < 0.2:
							self.seeker_genes[i] += randint(-100, 100)/500
				self.seeker_nn = NN(self.seeker_genes, self.s_input, 10, 10)
				self.avoider_nn = NN(self.best_avoider_genes[0], self.s_input,10,10)
			else:
				self.avoider_genes = np.copy(self.best_avoider_genes[0])
				if simulation > 1:
					for i in range(len(self.avoider_genes)):
						if random() < 0.2:
							self.avoider_genes[i] += randint(-100, 100)/500
				self.seeker_nn = NN(self.best_seeker_genes[0], self.s_input, 10, 10)
				self.avoider_nn = NN(self.avoider_genes, self.s_input, 10, 10)
			score = [0] * 3
			for start in range(4):
				if start == 3:
					self.simulator = kinematic_simulator(walls, [[[0,0,1.5]], [[0.6,0.6,5]], [[0.6, -0.6, 4]]], ["red", "blue", "blue"])
				elif start == 1:
					self.simulator = kinematic_simulator(walls, [[[0,0,1.5]], [[-0.6,0.6,5]], [[-0.6, -0.6, 4]]], ["red", "blue", "blue"])
				elif start == 2:
					self.simulator = kinematic_simulator(walls, [[[0,0,1.5]], [[-0.6, 0.6, 5]], [[0.6, 0.6, 4]]], ["red", "blue", "blue"])
				else:
					self.simulator = kinematic_simulator(walls, [[[0,0,1.5]], [[-0.6, -0.6, 5]], [[0.6, -0.6, 4]]], ["red", "blue", "blue"])
				for i in range(how_much_time):
					a = self.simulator.lidar_sensor(0)
					b = [self.simulator.camera(0, "red", nbin), self.simulator.camera(0, "yelow", nbin), self.simulator.camera(0, "blue", nbin), self.simulator.camera(0, "green", nbin), self.simulator.camera(0, "purple", nbin)]
					c = self.simulator.ground_sensor(0)
					d = build_input(a,b,c, 30)
					speed1 = self.seeker_nn.forward_propagation(d)
					a = self.simulator.lidar_sensor(1)
					b = [self.simulator.camera(1, "red", nbin), self.simulator.camera(1, "yelow", nbin), self.simulator.camera(1, "blue", nbin), self.simulator.camera(1, "green", nbin), self.simulator.camera(1, "purple", nbin)]
					c = self.simulator.ground_sensor(1)
					d = build_input(a,b,c, 20)
					speed2 = get_simu_behaviour(d)
					a = self.simulator.lidar_sensor(2)
					b = [self.simulator.camera(2, "red", nbin), self.simulator.camera(2, "yelow", nbin), self.simulator.camera(2, "blue", nbin), self.simulator.camera(2, "green", nbin), self.simulator.camera(2, "purple", nbin)]
					c = self.simulator.ground_sensor(2)
					d = build_input(a,b,c, 20)
					speed3 = get_simu_behaviour(d)
					self.simulator.simulate([speed1, speed2, speed3], 0.5)
				for i in range(len(self.simulator.fitness)):
					score[i] += self.simulator.fitness[i]
			if True:
				if score[0] >= self.best_seeker_genes[1]:
					print("save seeker")
					self.best_seeker_genes = [np.copy(self.seeker_genes), score[0]]
					self.best_avoider_genes[1] = 0.5*score[1] + 0.5*score[2]
					np.savetxt("seeker.txt", [self.best_seeker_genes[0]], delimiter=", ")
					name = "genes_archives/seeker" + datetime.today().strftime('%y-%m-%d-%H-%M-%s') + ".txt"
					np.savetxt(name, [self.best_seeker_genes[0]], delimiter=", ")
					self.simulator.save()
			else:
				if score[1] + score[2] >= 2*self.best_avoider_genes[1]:
					print("save avoider")
					self.best_avoider_genes = [np.copy(self.avoider_genes), 0.5*score[1] + 0.5*score[2]]
					self.best_seeker_genes[1] = score[0]
					np.savetxt("avoider.txt", [self.best_avoider_genes[0]], delimiter=", ")
					name = "genes_archives/avoider" + datetime.today().strftime('%y-%m-%d-%H-%M-%s') + ".txt"
					np.savetxt(name, [self.best_avoider_genes[0]], delimiter=", ")
					self.simulator.save()
			print(score)

def build_input(lidar_output, camera_output, ground, ds=10):
	output = []
	for i in range(0, 360, ds):
		for j in range(i, i + ds):
			m = float('inf')
			if lidar_output[j] != 999999999:
				m = lidar_output[j] * 1000
		if m == float('inf') or m > 1999:
			output.append(0)
		else:
			output.append(1 - m/2000)
	for i in camera_output:
		for j in i:
			output.append(j)
	output.append(ground[0])
	output.append(ground[1])
	return output

if __name__ == "__main__":
	a = learn()
	a.learn(60)
