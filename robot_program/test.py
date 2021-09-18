from copy import deepcopy

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

def board_translation(board):
	robot = -1
	cans = []
	target = []
	new_board = []
	for i in range(len(board)):
		new_line = []
		for j in range(len(board[i])):
			if board[i][j] == 'X':
				new_line.append(1)
			elif board[i][j] == '@':
				new_line.append(0)
				robot = i * len(board[i]) + j
			elif board[i][j] == '.':
				new_line.append(0)
				target.append((i,j))
			elif board[i][j] == '*':
				new_line.append(0)
				target.append((i,j))
				cans.append((i,j))
			elif board[i][j] == '$':
				new_line.append(0)
				can.append((i,j))
			elif board[i][j] == ' ':
				new_line.append(0)
			else:
				print ("ERRORRRRRRRRRR")
	return robot, can, target, new_board	
	

def check(list1, list2):
	for i in list1:
		if i in list2:
			list1.remove(i)
			list2.remove(i)
		else:
			return False
	return True

def generate_new_states(state, prev):
	ret = []
	if state._robot[0] > 0: #are we at border
		if board[state._robot[0] - 1][state._robot[1]] == 0: #is there a wall
			if (state._robot[0] - 1, state._robot[1]) in state._cans:  #is there a can
				if state._robot[0] > 1 and board[state._robot[0] - 2][state._robot[1]] == 0 and (state._robot[0] - 2, state._robot[1]) not in state._cans: #is the can is at the border, or is there a wall or a can in front of her 
					new_cans = []
					for i in state._cans:
						if i != (state._robot[0] - 1, state._robot[1]):
							new_cans.append(i)
					new_cans.append((state._robot[0] - 2, state._robot[1]))
					ret.append(State(new_cans, (state._robot[0] - 1, state._robot[1]),prev))
			else:
				ret.append(State(state._cans, (state._robot[0] - 1, state._robot[1]),prev))
	if state._robot[0] < y:
		if board[state._robot[0] + 1][state._robot[1]] == 0:
			if (state._robot[0] + 1, state._robot[1]) in state._cans:
				if state._robot[0] < y - 1 and board[state._robot[0] + 2][state._robot[1]] == 0 and (state._robot[0] + 2, state._robot[1]) not in state._cans:
					new_cans = []
					for i in state._cans:
						if i != (state._robot[0] + 1, state._robot[1]):
							new_cans.append(i)
					new_cans.append((state._robot[0] + 2, state._robot[1]))
					ret.append(State(new_cans, (state._robot[0] + 1, state._robot[1]),prev))
			else:
				ret.append(State(state._cans, (state._robot[0] + 1, state._robot[1]),prev))
	if state._robot[1] < x:
		if board[state._robot[0]][state._robot[1] + 1] == 0:
			if (state._robot[0], state._robot[1] + 1) in state._cans:
				if state._robot[1] < x - 1 and board[state._robot[0]][state._robot[1] + 2] == 0 and (state._robot[0], state._robot[1] + 2) not in state._cans:
					new_cans = []
					for i in state._cans:
						if i != (state._robot[0], state._robot[1] + 1):
							new_cans.append(i)
					new_cans.append((state._robot[0], state._robot[1] + 2))
					ret.append(State(new_cans, (state._robot[0], state._robot[1] + 1), prev))
			else:
				ret.append(State(state._cans, (state._robot[0], state._robot[1] + 1), prev))
	if state._robot[1] > 0:
		if board[state._robot[0]][state._robot[1] - 1] == 0:
			if (state._robot[0], state._robot[1] - 1) in state._cans:
				if state._robot[1] > 1 and board[state._robot[0]][state._robot[1] - 2] == 0 and (state._robot[0], state._robot[1] - 2) not in state._cans:
					new_cans = []
					for i in state._cans:
						if i != (state._robot[0], state._robot[1] - 1):
							new_cans.append(i)
					new_cans.append((state._robot[0], state._robot[1] - 2)) 
					ret.append(State(new_cans, (state._robot[0], state._robot[1] - 1), prev))
			else:
				ret.append(State(state._cans, (state._robot[0], state._robot[1] - 1), prev))
	return ret
	

def check_stuck(cans):
	for can in cans:
		if can not in target:
			if board[can[0]][can[1] + 1] == 1 and board[can[0] + 1][can[1]] == 1:
				return True
			if board[can[0] + 1][can[1]] == 1 and board[can[0]][can[1] - 1] == 1:
				return True
			if board[can[0]][can[1] - 1] == 1 and board[can[0] - 1][can[1]] == 1:
				return True
			if board[can[0]][can[1] + 1] == 1 and board[can[0] - 1][can[1]] == 1:
				return True
	return False
		

def solve_sokoban(begining):
    target.sort()
    states_list = [begining]
    begining = 0
    end = 1
    while (True):
        a = 0
        for i in range(begining, end):
            new = generate_new_states(states_list[i], i)
            for j in new:
                if j not in states_list and check_stuck(j._cans) == False:
                    #printStateFancy(j)
                    states_list.append(j)
                    j._cans.sort()
                    a += 1
                    if target == j._cans:
                        return states_list
        begining = end
        end += a
        if a == 0:
            return states_list

def check_board():
	# check for target ion wall
	for t in target:
		if board[t[0]][t[1]] == "1":
			print("there is a mistake here")

def recursive_print_traject(l, i, after):
	if l[i]._prev != -1:
		ret = recursive_print_traject(l, l[i]._prev, i)
	else:
		ret = []
	#printStateFancy(l[i])
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


def printStateFancy(state):
	for i in range(len(board)):
		line = ""
		for j in range(len(board[i])):
			e = board[i][j]
			if(e == 0): e = " "	  #Empty
			if(e == 1): e = "⊠"  #Walls
			for t in target:
				if(t == (i,j)): e = "✛" #Target
			for c in state._cans:
				if(c == (i,j)): e = "⬤" #Can
			if ((state._robot[0] , state._robot[1]) == (i,j)): e = "△" #Can
			line = line + str(e) + " "
		print(line)

board = [	[1,1,1,1,1,1,0,0],
			[1,0,0,0,0,1,0,0],
			[1,0,1,0,0,1,0,0],
			[1,0,0,0,0,1,1,1],
			[1,0,0,0,0,0,0,1],
			[1,0,0,1,0,0,0,1],
			[1,1,1,1,1,1,1,1]]


x = len(board[0]) - 1
y = len(board) - 1

robot = (5,5)
target = [(1,3), (2,3), (3,3)]
cans = [(4,2),(4,3), (4,4)]

begining = State(cans,robot, -1)
a = solve_sokoban(begining)
print(recursive_print_traject(a, len(a) - 1, -1))

