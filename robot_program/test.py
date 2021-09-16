from copy import deepcopy

class State:
	def __init__(self, cans, robot):
		self._cans = cans
		self._robot = robot

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

def finalState(list1, list2):
	for i in list1:
		if i in list2:
			list1.remove(i)
			list2.remove(i)
		else:
			return False
	return True

def generate_new_states(state):
	#up
	ret = []
	if state._robot[0] > 0:
		if board[state._robot[0] - 1][state._robot[1]] == 0:
			if (state._robot[0] - 1, state._robot[1]) in state._cans: 
				if board[state._robot[0] - 2][state._robot[1]] == 0 and (state._robot[0] - 2, state._robot[1]) not in state._cans and state._robot[0] > 1:
					new_cans = []
					for i in state._cans:
						if i != (state._robot[0] - 1, state._robot[1]):
							new_cans.append(i)
					new_cans.append((state._robot[0] - 2, state._robot[1]))
					ret.append(State(new_cans, (state._robot[0] - 1, state._robot[1])))
			else:
				ret.append(State(state._cans, (state._robot[0] - 1, state._robot[1])))
	if state._robot[0] < y:
		if board[state._robot[0] + 1][state._robot[1]] == 0:
			if (state._robot[0] + 1, state._robot[1]) in state._cans:
				if board[state._robot[0] + 2][state._robot[1]] == 0 and (state._robot[0] + 2, state._robot[1]) not in state._cans and state._robot[0] < y - 1:
					new_cans = []
					for i in state._cans:
						if i != (state._robot[0] + 1, state._robot[1]):
							new_cans.append(i)
						new_cans.append((state._robot[0] + 2, state._robot[1]))
					ret.append(State(new_cans, (state._robot[0] + 1, state._robot[1])))
			else:
				ret.append(State(state._cans, (state._robot[0] + 1, state._robot[1])))
	if state._robot[1] < x:
		if board[state._robot[0]][state._robot[1] + 1] == 0:
			if (state._robot[0], state._robot[1] + 1) in state._cans:
				if board[state._robot[0]][state._robot[1] + 2] == 0 and (state._robot[0], state._robot[1] + 2) not in state._cans and state._robot[1] < x - 1:
					new_cans = []
					for i in state._cans:
						if i != (state._robot[0], state._robot[1] + 1):
							new_cans.append(i)
						new_cans.append((state._robot[0], state._robot[1] + 2))
					ret.append(State(new_cans, (state._robot[0], state._robot[1] + 1)))
			else:
				ret.append(State(state._cans, (state._robot[0], state._robot[1] + 1)))
	if state._robot[1] > 0:
		if board[state._robot[0]][state._robot[1] - 1] == 0:
			if (state._robot[0], state._robot[1] - 1) in state._cans:
				if board[state._robot[0]][state._robot[1] - 2] == 0 and (state._robot[0], state._robot[1] - 2) not in state._cans and state._robot[1] > 1:
					new_cans = []
					for i in state._cans:
						if i != (state._robot[0], state._robot[1] - 1):
							new_cans.append(i)
						new_cans.append((state._robot[0], state._robot[1] - 2)) 
					ret.append(State(new_cans, (state._robot[0], state._robot[1] - 1)))
			else:
				ret.append(State(state._cans, (state._robot[0], state._robot[1] - 1)))
	return ret

def check_board():
	# check for target ion wall
	for t in target:
		if board[t[0]][t[1]] == "1":
			print("there is a mistake here")

def printState(state):
	b = deepcopy(board)
	for t in target:
		b[t[0]][t[1]]="T"
	for c in state._cans:
		b[c[0]][c[1]]="C"
	b[state._robot[0]][state._robot[1]]="R"			
	for i in range(len(board)):
		line = ""
		for j in range(len(board[i])):
			line = line + str(b[i][j]) + " "
		print(line)

def printStateFancy(state):
	for i in range(len(board)):
		line = ""
		for j in range(len(board[i])):
			e = board[i][j]
			if(e == 0): e = " "	  #Empty
			if(e == 1): e = "⊠"  #Walls
			for t in target:
				if(t == (i,j)): e = "✛" #Target
			for c in cans:
				if(c == (i,j)): e = "⬤" #Can
			if ((state._robot[0] , state._robot[1]) == (i,j)): e = "△" #Can
			line = line + str(e) + " "
		print(line)

def recursive(state):
	print(finalState(cans,target))
	if(finalState(cans,target)):
		return state 	
	newStates = generate_new_states(state)
	for ns in newStates:
		printStateFancy(ns)
		#recursive(ns)

def available():
	print()


board = [	[1,1,1,1,1,1,1,1,1],
			[1,0,0,0,0,0,0,0,1],
			[1,0,0,0,0,0,0,0,1],
			[1,0,0,1,1,1,0,0,1],
			[1,0,0,0,0,0,0,0,1],
			[1,0,0,0,0,0,0,0,1],
			[1,1,1,1,1,1,1,1,1]]

board2 = [	[1,1,1,1,1,1,1,1,1],
			[1,0,0,0,0,0,0,0,1],
			[1,0,1,0,1,0,0,0,1],
			[1,0,0,0,0,0,0,0,1],
			[1,0,1,0,1,0,1,0,1],
			[1,0,0,0,0,0,0,0,1],
			[1,1,1,1,1,1,1,1,1]]


x = len(board[0])
y = len(board)

robot = (2,3)
target = [(2,5)]
cans = [(2,4)]

a = State(cans, robot)
printStateFancy(a)
print(recursive(a))

