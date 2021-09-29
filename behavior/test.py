from sokobanSolver import State, SokobanSolver
from random import randint

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
	for i in range(10):	
		a = generate_all(4, 5, 3, 5)
		init_state = State(a[1],a[3], -1)
		solver = SokobanSolver(a[0], a[2], a[3], a[1])
		#solution = solver.solve_sokoban(init_state)
		#plan = solver.recursive_print_traject(solution, len(solution) - 1, -1)[:-1]
		print("both", solver.complexity_both(init_state))
		print("stuck", solver.complexity_stuck(init_state))
		print("not", solver.complexity_not(init_state))
		print("brute force", solver.complexity_bf(init_state))
		del(init_state)
		del(solver)
