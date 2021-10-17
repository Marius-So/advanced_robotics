from kinematic_simulator import kinematic_simulator
from pathfinding import pathfinder
from random import randint

def generate_world():
	h = 1
	w = 1
	walls = [[-w/2, -w/2, -h/2, h/2], [w/2, w/2, -h/2,h/2],[-w/2,w/2,h/2,h/2],[-w/2,w/2,-h/2,-h/2]]
	q = 0
	x = 0
	y = 0
	simulator = kinematic_simulator(walls)
	return simulator, x,y,q

if __name__ == "__main__":
	simulator, x ,y ,q = generate_world()
	coo = [[x, y ,q]]
	while(len(coo) < 10000):
		distance = simulator.thymio_sensor(coo[-1][0],coo[-1][1],coo[-1][2])
		if distance[0] < 0.14 or distance[1] < 0.14 or distance[2] < 0.14 or distance[3] < 0.14 or distance[4] < 0.14:
			if distance[0] + distance[1] != distance[3] + distance[4]:
				coo.extend(simulator.simulate(coo[-1][0],coo[-1][1],coo[-1][2],2,-1,6))
			else:
				coo.extend(simulator.simulate(coo[-1][0],coo[-1][1],coo[-1][2],2, -1,3))
		else:
			coo.extend(simulator.simulate(coo[-1][0],coo[-1][1],coo[-1][2],1,1,1))
	simulator.save(coo)
