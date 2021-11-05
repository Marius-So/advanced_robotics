from matplotlib.pyplot import get
import numpy as np
import random
from kinematic_simulator import kinematic_simulator

# https://towardsdatascience.com/simple-reinforcement-learning-q-learning-fcddc4b6fe56

actions = ['left', 'right', 'straight', 'stop']  # constant speed
states = ['sLeft', 'sRight', 'sStraight, sNothins']  # state of the sensors
rewards = [[0, 1, 0.6, 0.3],
           [1, 0, 0.6, 0.3],
           [0.6, 0.6, 0, 0.3],
           [0.3, 0.3, 1, 0]]

Q = np.zeros((len(states), len(actions)))

speed = 2
time = 1
redu = 0.5
iterations = 100
h = 1
w = 1
walls = [[-w/2, -w/2, -h/2, h/2], [w/2, w/2, -h/2, h/2],
         [-w/2, w/2, h/2, h/2], [-w/2, w/2, -h/2, -h/2]]
simulator = kinematic_simulator(walls)
coo = [[0, 0, 0]]


def activate(a):
    if a == 0:
        coo.extend(simulator.simulate(
            coo[-1][0], coo[-1][1], coo[-1][2], speed*redu, speed, time))
    if a == 1:
        coo.extend(simulator.simulate(
            coo[-1][0], coo[-1][1], coo[-1][2], speed, speed*redu, time))
    if a == 2:
        coo.extend(simulator.simulate(
            coo[-1][0], coo[-1][1], coo[-1][2], speed, speed, time))
    if a == 3:
        coo.extend(simulator.simulate(
            coo[-1][0], coo[-1][1], coo[-1][2], 0, 0, time))


def getState():
    # states = ['sLeft', 'sRight', 'sStraight, sNothins'
    lecture = simulator.thymio_sensor(coo[-1][0], coo[-1][1], coo[-1][2])
    for i in range(0, 7):
        if lecture[i] == 99999999:
            lecture[i] = 0

    if lecture[0] > lecture[2] and lecture[2] > lecture[4]:
        return 0
    if lecture[0] < lecture[2] and lecture[2] < lecture[4]:
        return 1
    if lecture[0] == lecture[2] and lecture[2] == lecture[4] and lecture[4] == 0:
        return 2
    else:
        return 3

def getBestAction(state):
    print(state)
    print(Q)
    best = 0
    bestindex = 0
    for i in range(len(Q[state])):
        if Q[state][i]>best:
            best = Q[state][i]
            bestindex = i
    return i

def QLearning():
    # Initialize q-table values to 0
    # Set the percent you want to explore
    epsilon = 0.2
    lr = 0.5
    gamma = 0.85
    a = 2
    s = 3
    for i in range(iterations):
        if random.uniform(0, 1) < epsilon:
            # Explore: select a random action
            a = random.randint(0, len(actions))
        else:
            # Exploit: select the action with max value (future reward)
            a = getBestAction(s)

        s = getState()
        activate(a)
        new_s = getState()
        Q[s, a] = Q[s, a] + lr * (rewards[s][a] + gamma * getBestAction(new_s) - Q[s, a])
    simulator.save(coo)


if __name__ == "__main__":
    QLearning()
