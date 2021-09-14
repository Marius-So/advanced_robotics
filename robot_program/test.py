class state:
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
				target.append(i * len(board[i]) + j)
			elif board[i][j] == '*':
				new_line.append(0)
				target.append(i * len(board[i]) + j)
				cans.append(i * len(board[i]) + j)
			elif board[i][j] == '$':
				new_line.append(0)
				can.append(i * len(board[i]) + j)
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

def generate_new_states(state):
	#up
	ret = []
	if state._robot > x:
		if board[state._robot - x] == 0:
			if state._robot - x in state._cans:
				if board[state._robot - 2 * x] == 0 and state._robot - 2 * x not in state._cans and state._robot > 2 * x:
					new_cans = []
					for i in state._cans:
						if i != state._robot - x:
							new_cans.append(i)
					new_cans.append(state._robot - 2 * x)
					ret.append(state(new_cans, state._robot - x))
			else:
				ret.append(state(state._cans, state._robot - x))
	if state._robot < y - x:
		if board[state._robot + x] == 0:
			if state._robot + x in state._cans:
				if board[state._robot + 2 * x] == 0 and state._robot + 2 * x not in state._cans and state._robot < y - 2 * x:
					new_cans = []
					for i in state._cans:
						if i != state._robot + x:
							new_cans.append(i)
							new_cans.append(state._robot + 2 * x)
					ret.append(state(new_cans, state._robot + x))
			else:
				ret.append(state(state._cans, state._robot + x))
	if state._robot > 1:
		if board[state._robot - 1] == 0:
			if state._robot - 1 in state._cans:
				if board[state._robot - 2] == 0 and state._robot - 2 not in state._cans and state._robot > 2:
					new_cans = []
					for i in states._cans:
						if i != state._robot - 1:
							new_cans.append(i)
						new_cans.append(state._robot - 2)
					ret.append(state(new_cans, state._robot - 1))
				else:
					ret.append(state(state._cans, state._robot - 1))
	if state._robot < x - 1:
		if board[state._robot + 1] == 0:
			if state._robot + 1 in state._cans:
				if board[state._robot + 2] == 0 and state._robot + 2 not in state._cans and state._robot < x - 2:
					new_cans = []
					for i in states._cans:
						if i != state._robot + 1:
							new_cans.append(i)
						new_cans.append(state._robot + 2)
					ret.append(state(new_cans, state._robot + 1))
			else:
				ret.append(state(state._cans, state._robot + 1))
	return ret

target = [19,32,46]
board = [	[1,1,1,1,1,1,1,1,1],
			[1,0,0,0,0,0,0,0,1],
			[1,0,1,0,1,0,0,0,1],
			[1,0,0,0,0,0,0,0,1],
			[1,0,1,0,1,0,1,0,1],
			[1,0,0,0,0,0,0,0,1],
			[1,1,1,1,1,1,1,1,1]]
x = len(board[0])
y = len(board)

robot = 10
cans = [21, 39, 46]

a = state(cans, robot)
print(generate_new_states(a))

