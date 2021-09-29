from copy import deepcopy
import time

class SokobanSolver:
	def __init__(self, board, targets, robot, can) -> None:
		self.board = board
		self.targets = targets
		self.robot = robot
		self.can = can
		self.x = len(self.board[0]) - 1
		self.y = len(self.board) - 1

	def generate_new_states(self, state, prev):
		ret = []
		if state._robot[0] > 0: #are we at border
			if self.board[state._robot[0] - 1][state._robot[1]] == 0: #is there a wall
				if (state._robot[0] - 1, state._robot[1]) in state._cans:  #is there a can
					if state._robot[0] > 1 and self.board[state._robot[0] - 2][state._robot[1]] == 0 and (state._robot[0] - 2, state._robot[1]) not 	in state._cans: #is the can is at the border, or is there a wall or a can in front of her
						new_cans = []
						for i in state._cans:
							if i != (state._robot[0] - 1, state._robot[1]):
								new_cans.append(i)
						new_cans.append((state._robot[0] - 2, state._robot[1]))
						ret.append(State(new_cans, (state._robot[0] - 1, state._robot[1]),prev))
				else:
					ret.append(State(state._cans, (state._robot[0] - 1, state._robot[1]),prev))
		if state._robot[0] < self.y:
			if self.board[state._robot[0] + 1][state._robot[1]] == 0:
				if (state._robot[0] + 1, state._robot[1]) in state._cans:
					if state._robot[0] < self.y - 1 and self.board[state._robot[0] + 2][state._robot[1]] == 0 and (state._robot[0] + 2, state._robot[1]) 	not in state._cans:
						new_cans = []
						for i in state._cans:
							if i != (state._robot[0] + 1, state._robot[1]):
								new_cans.append(i)
						new_cans.append((state._robot[0] + 2, state._robot[1]))
						ret.append(State(new_cans, (state._robot[0] + 1, state._robot[1]),prev))
				else:
					ret.append(State(state._cans, (state._robot[0] + 1, state._robot[1]),prev))
		if state._robot[1] < self.x:
			if self.board[state._robot[0]][state._robot[1] + 1] == 0:
				if (state._robot[0], state._robot[1] + 1) in state._cans:
					if state._robot[1] < self.x - 1 and self.board[state._robot[0]][state._robot[1] + 2] == 0 and (state._robot[0], state._robot[1] + 2) 	not in state._cans:
						new_cans = []
						for i in state._cans:
							if i != (state._robot[0], state._robot[1] + 1):
								new_cans.append(i)
						new_cans.append((state._robot[0], state._robot[1] + 2))
						ret.append(State(new_cans, (state._robot[0], state._robot[1] + 1), prev))
				else:
					ret.append(State(state._cans, (state._robot[0], state._robot[1] + 1), prev))
		if state._robot[1] > 0:
			if self.board[state._robot[0]][state._robot[1] - 1] == 0:
				if (state._robot[0], state._robot[1] - 1) in state._cans:
					if state._robot[1] > 1 and self.board[state._robot[0]][state._robot[1] - 2] == 0 and (state._robot[0], state._robot[1] - 2) not 	in state._cans:
						new_cans = []
						for i in state._cans:
							if i != (state._robot[0], state._robot[1] - 1):
								new_cans.append(i)
						new_cans.append((state._robot[0], state._robot[1] - 2))
						ret.append(State(new_cans, (state._robot[0], state._robot[1] - 1), prev))
				else:
					ret.append(State(state._cans, (state._robot[0], state._robot[1] - 1), prev))
		return ret


	def check_stuck(self, cans):
		for can in cans:
			if can not in self.targets:
				if not (can[0] == 0 or can[0] == self.y or can[1] == 0 or can[1] == self.x):
					if self.board[can[0]][can[1] + 1] == 1 and self.board[can[0] + 1][can[1]] == 1:
						return True
					if self.board[can[0] + 1][can[1]] == 1 and self.board[can[0]][can[1] - 1] == 1:
						return True
					if self.board[can[0]][can[1] - 1] == 1 and self.board[can[0] - 1][can[1]] == 1:
						return True
					if self.board[can[0]][can[1] + 1] == 1 and self.board[can[0] - 1][can[1]] == 1:
						return True
				if can[0] == 0 and can[1] == 0 or can[0] == self.y and can[1] == 0 or can[0] == 0 and can[1] == self.x and can[0] == self.y and can[1] == self.x:
					return True
		return False

	def solve_sokoban(self, begining):
		self.targets.sort()
		states_list = [begining]
		begining = 0
		end = 1
		a = 0
		while (True):
			a = 0
			for i in range(begining, end):
				new = self.generate_new_states(states_list[i], i)
				for j in new:
					if j not in states_list and self.check_stuck(j._cans) == False:
						states_list.append(j)
						j._cans.sort()
						a += 1
						if self.targets == j._cans:
							return states_list
			begining = end
			end += a
			if a == 0:
				return states_list

	def recursive_print_traject(self, l, i, after):
		if l[i]._prev != -1:
			ret = self.recursive_print_traject(l, l[i]._prev, i)
		else:
			ret = []
		self.printStateFancy(l[i])
		print('---------------')
		if l[after]._robot[0] > l[i]._robot[0]:
			ret.append("down")
		elif l[after]._robot[0] < l[i]._robot[0]:
			ret.append("up")
		elif l[after]._robot[1] > l[i]._robot[1]:
			ret.append("right")
		else:
			ret.append("left")
		if l[after]._cans != l[i]._cans:
			ret.append("can")
		return ret


	def printStateFancy(self, state):
		for i in range(len(self.board)):
			line = ""
			for j in range(len(self.board[i])):
				e = self.board[i][j]
				if(e == 0): e = " "	  #Empty
				if(e == 1): e = "⊠"  #Walls
				for t in self.targets:
					if(t == (i,j)): e = "✛" #Target
				for c in state._cans:
					if(c == (i,j)): e = "⬤" #Can
				if ((state._robot[0] , state._robot[1]) == (i,j)): e = "△" #Can
				line = line + str(e) + " "
			print(line)
	
	def complexity_both(self, begining):
		self.targets.sort()
		states_list = [begining]
		begining = 0
		end = 1
		a = 0
		b = 0
		while (True):
			a = 0
			for i in range(begining, end):
				b = b + 1
				new = self.generate_new_states(states_list[i], i)
				for j in new:
					if j not in states_list and self.check_stuck(j._cans) == False:
						states_list.append(j)
						j._cans.sort()
						a += 1
						if self.targets == j._cans:
							return len(states_list) / b
			begining = end
			end += a
			if a == 0:
				print("no")
				return len(states_list)/ b

	def complexity_stuck(self, begining):
		self.targets.sort()
		states_list = [begining]
		begining = 0
		end = 1
		a = 0
		b = 0
		while (True):
			a = 0
			for i in range(begining, end):
				b = b + 1
				new = self.generate_new_states(states_list[i], i)
				for j in new:
					if self.check_stuck(j._cans) == False:
						states_list.append(j)
						j._cans.sort()
						a += 1
						if self.targets == j._cans:
							return len(states_list) / b
			begining = end
			end += a
			if a == 0:
				return len(states_list)/ b
	
	def complexity_not(self, begining):
		self.targets.sort()
		states_list = [begining]
		begining = 0
		end = 1
		a = 0
		b = 0
		while (True):
			a = 0
			for i in range(begining, end):
				b = b + 1
				new = self.generate_new_states(states_list[i], i)
				for j in new:
					if j not in states_list:
						states_list.append(j)
						j._cans.sort()
						a += 1
						if self.targets == j._cans:
							return len(states_list) / b
			begining = end
			end += a
			if a == 0:
				return len(states_list)/ b
	
	def complexity_bf(self, begining):
		self.targets.sort()
		states_list = [begining]
		begining = 0
		end = 1
		a = 0
		b = 0
		while (True):
			a = 0
			for i in range(begining, end):
				b = b + 1
				new = self.generate_new_states(states_list[i], i)
				for j in new:
					states_list.append(j)
					j._cans.sort()
					a += 1
					if self.targets == j._cans:
						return len(states_list) / b
			begining = end
			end += a
			if a == 0:
				return len(states_list)/ b

#	def check(list1, list2):
#	for i in list1:
#		if i in list2:
#			list1.remove(i)
#			list2.remove(i)
#		else:
#			return False
#	return True

class State:
	def __init__(self, cans, robot, prev: int):
		self._cans = cans
		self._robot = robot
		self._prev = prev

	def __eq__(self, x):
		if self._cans == x._cans and self._robot == x._robot:
			return True
		return False

	def __str__(self):
		a = ""
		a += str(self._robot)
		for i in self._cans:
			a +=str(i)
		return a

#def board_translation(board):
#	robot = -1
#	cans = []
#	target = []
#	new_board = []
#	for i in range(len(board)):
#		new_line = []
#		for j in range(len(board[i])):
#			if board[i][j] == 'X':
#				new_line.append(1)
#			elif board[i][j] == '@':
#				new_line.append(0)
#				robot = i * len(board[i]) + j
#			elif board[i][j] == '.':
#				new_line.append(0)
#				target.append((i,j))
#			elif board[i][j] == '*':
#				new_line.append(0)
#				target.append((i,j))
#				cans.append((i,j))
#			elif board[i][j] == '$':
#				new_line.append(0)
#				cans.append((i,j))
#			elif board[i][j] == ' ':
#				new_line.append(0)
#			else:
#				print ("ERRORRRRRRRRRR")
#	print(new_board)
#	return robot, cans, target, new_board
#
if '__main__' == __name__:
	cans = [(1,1),(2,1), (3,1)]
	robot = (0,0)
	target = [(0,3),(2,0),(3,3)]
	board = [[0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0]]

	init_state = State(cans,robot, -1)
	solver = SokobanSolver(board, target, robot, cans)
	solver.printStateFancy(init_state)
	solution = solver.solve_sokoban(init_state)
	plan = solver.recursive_print_traject(solution, len(solution) - 1, -1)[:-1]
	print(plan)






