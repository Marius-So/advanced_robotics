from kinematic_simulator import kinematic_simulator
from pathfinding import pathfinder
from random import randint
import matplotlib.pyplot as plt


def detect_local_min(l):
	ret = []
	s = len(l) + 1
	ss = s - 2
	for i in range(0, s):
		if l[(i - 1) % ss] > l[i % ss] and l[i % ss] < l[(i + 1) % ss]:
			ret.append(i % ss)
	return ret
	
def generate_world():
	h = 1
	w = 2
	walls = [[-w/2, -w/2, -h/2, h/2], [w/2, w/2, -h/2,h/2],[-w/2,w/2,h/2,h/2],[-w/2,w/2,-h/2,-h/2]]
	q = randint(0,360) / 360
	x = randint(-9,9) / 20
	y = randint(-4,4) / 10
	simulator = kinematic_simulator(walls)
	return simulator, x,y,q

if __name__ == "__main__":
	simulator, x ,y ,q = generate_world()
	coo = [[x, y ,q]]
	while(detect_local_min(simulator.lidar_sensor(coo[-1][0], coo[-1][1], coo[-1][2]))[0] != 1):
		coo.extend(simulator.simulate(coo[-1][0],coo[-1][1],coo[-1][2],2,-1,0.1))
	while(simulator.lidar_sensor(coo[-1][0], coo[-1][1], coo[-1][2])[0] > 0.1):
		coo.extend(simulator.simulate(coo[-1][0],coo[-1][1],coo[-1][2],2,2,0.1))
	coo.extend(simulator.simulate(coo[-1][0],coo[-1][1],coo[-1][2],-1,2,0.3))
	while(detect_local_min(simulator.lidar_sensor(coo[-1][0], coo[-1][1], coo[-1][2]))[0] > 4):
		coo.extend(simulator.simulate(coo[-1][0],coo[-1][1],coo[-1][2],-1,2,0.1))
	while(simulator.lidar_sensor(coo[-1][0], coo[-1][1], coo[-1][2])[0] > 0.1):
		coo.extend(simulator.simulate(coo[-1][0],coo[-1][1],coo[-1][2],2,2,0.1))
	coo.extend(simulator.simulate(coo[-1][0],coo[-1][1],coo[-1][2],-1,2,0.3))
	while(detect_local_min(simulator.lidar_sensor(coo[-1][0], coo[-1][1], coo[-1][2]))[0] > 4):
		coo.extend(simulator.simulate(coo[-1][0],coo[-1][1],coo[-1][2],-1,2,0.1))
	coo.extend(simulator.simulate(coo[-1][0],coo[-1][1],coo[-1][2],-1,2,0.3))
	while(detect_local_min(simulator.lidar_sensor(coo[-1][0], coo[-1][1], coo[-1][2]))[0] > 4):
		coo.extend(simulator.simulate(coo[-1][0],coo[-1][1],coo[-1][2],-1,2,0.1))

	simulator.save(coo)
