from copy import deepcopy


class State:
    def __init__(self, cans, robot):
        self.cans = cans
        self.robot = robot


def finalState(state):
    for t in target:
        if(t not in state.cans):
            return False
    print("GAME OVER. YOU WIN")
    return True


def check_board():
    # check for target ion wall
    for t in target:
        if board[t[0]][t[1]] == "1":
            print("there is a mistake here")


def printStateFancy(state):
    for i in range(len(board)):
        line = ""
        for j in range(len(board[i])):
            e = board[i][j]
            if(e == 0):
                e = " "  # Empty
            if(e == 1):
                e = "⊠"  # Walls
            for t in target:
                if(t == (i, j)):
                    e = "✛"  # Target
            for c in state.cans:
                if(c == (i, j)):
                    e = "◯"  # Can
            if ((state.robot[0], state.robot[1]) == (i, j)):
                e = "△"  # Robot
            for t in target:
                for c in state.cans:
                    if(((i, j) == c) & (c == t)):
                        e = "⬤"
            line = line + str(e) + " "
        print(line)

# Return a list of valid moves from a state.


def validMoves(state):
    vm = []
    up = (state.robot[0] - 1, state.robot[1])
    dw = (state.robot[0] + 1, state.robot[1])
    rt = (state.robot[0], state.robot[1] + 1)
    lt = (state.robot[0], state.robot[1] - 1)
    options = [up, dw, rt, lt]

    for o in options:
        if(isWall(o) == False & isCan(o) == False):
            vm.append(o)
        else:
            if(isWall(o) == False & isCan(o)):
                vectorDirection = (
                    state.robot[0] - o[0], state.robot[1] - o[0])
                canNewPos = (o[0] + vectorDirection[0],
                             o[1] + vectorDirection[1])
                if(isWall(canNewPos) == False & isCan(canNewPos) == False):
                    vm.append(o)
    # print(vm)
    return vm
# Helper function of validMoves


def isWall(tuple):
    if(board[tuple[0]][tuple[1]] == 1):
        return True
    else:
        return False
# Helper function of validMoves


def isCan(tuple):
    for c in cans:
        if(c == tuple):
            return True
    else:
        return False


def newState(current, move):
    if(isCan(move) == False):
        return State(current.cans, move)
    else:
        cans = []
        vectorDirection = (
            current.robot[0] - move[0], current.robot[1] - move[0])
        canNewPos = (move[0] + vectorDirection[0],
                     move[1] + vectorDirection[1])
        # print(str(canNewPos))
        cans.append(canNewPos)
        for c in (current.cans):
            if(c != move):
                cans.append(c)
                # print(str(cans))
        return State(cans, move)


def recursive(state, depth):
    print("Depth: " + str(depth))
    printStateFancy(state)
    if(finalState(state) == True):
        return
    if(depth > limitDepth):
        return
    depth = depth + 1
    vm = validMoves(state)
    for m in vm:
        ns = newState(state, m)
        if (isExplored(ns) == False):
            explored.append(state)
            recursive(ns, depth)

previousDepth = 0
tr = []
def handler(state, depth):
    if (previousDepth < depth):
        tr.append(state)

#-------------------------------------------------------------------------- im here, I need to track the winner branches


def isExplored(state):
    for ex in explored:
        if((ex.robot == state.robot) & (ex.cans == state.cans)):
            return True
    return False


board = [	[1, 1, 1, 1, 1, 1, 1, 1, 1],
          [1, 0, 0, 0, 0, 0, 0, 0, 1],
          [1, 0, 0, 0, 0, 0, 0, 0, 1],
          [1, 0, 0, 1, 1, 1, 0, 0, 1],
          [1, 0, 0, 0, 0, 0, 0, 0, 1],
          [1, 0, 0, 0, 0, 0, 0, 0, 1],
          [1, 1, 1, 1, 1, 1, 1, 1, 1]]

robot = (1, 2)
target = [(2, 5)]
cans = [(2, 4)]

explored = []
trajectories = [[]]


a = State(cans, robot)
tr.append(a)
# explored.append(a)
#printStateFancy(a)
limitDepth = 10
depth = 0
recursive(a, depth)
