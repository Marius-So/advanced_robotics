import numpy as np
import random
from kinematic_simulator import kinematic_simulator
import matplotlib.pyplot as plt


# https://towardsdatascience.com/simple-reinforcement-learning-q-learning-fcddc4b6fe56

actions = ['left', 'right', 'straight', 'back']  # constant speed
states = ['sLeft', 'sRight', 'sNothing', 'sStraight']  # state of the sensors
rewards = [[0, 2, 0, 0], #sleft 
           [2, 0, 0, 0], #sright
           [0, 0, 2, 0],
           [1, 1, 0, 0.4]]

Q = np.random.randn(len(states), len(actions))*0.0
Q_save = []
for i in Q:
    s = []
    for j in i:
        s.append([j])
    Q_save.append(s)


#Q[0] = [0,   1,   0.5, 0] #sleft
#Q[1] = [1,   0,   0.5, 0] #sRight
#Q[2] = [0.2, 0.2, 1,   0] #sNothing
#Q[3] = [1, 0.2, 0,   0.2] #sStraight


speed = 2
time = 0.1
redu = 0.2
iterations = 10000
h = 1.5
w = 1.5
walls = [[-w/2, -w/2, -h/2, h/2], [w/2, w/2, -h/2, h/2], [-w/2, w/2, h/2, h/2], [-w/2, w/2, -h/2, -h/2], [-0.2, 0, 0.4, 0.4], [0.2,0, 0.4,0.3], [-0.2, 0, -0.4, -0.3], [0.2,0, -0.4,-0.3]]
simulator = kinematic_simulator(walls)
coo = [[0, 0, 3.14/2]]


def activate(a):
    if a == 0:
        coo.extend(simulator.simulate(
            coo[-1][0], coo[-1][1], coo[-1][2], speed, -speed, time))
    if a == 1:
        coo.extend(simulator.simulate(
            coo[-1][0], coo[-1][1], coo[-1][2], -speed, speed, time))
    if a == 2:
        coo.extend(simulator.simulate(
            coo[-1][0], coo[-1][1], coo[-1][2], speed, speed, time))
    if a == 3:
        coo.extend(simulator.simulate(
            coo[-1][0], coo[-1][1], coo[-1][2], -speed, -speed, time))


def getState():
    lecture = simulator.thymio_sensor(coo[-1][0], coo[-1][1], coo[-1][2])
    for i in range(0, 7):
        if lecture[i] == 99999999:
            lecture[i] = 0
    if lecture[0] < lecture[2] and lecture[2] < lecture[4]:
        return 0
    if lecture[0] > lecture[2] and lecture[2] > lecture[4]:
        return 1
    if lecture[0] == lecture[2] and lecture[2] == lecture[4] and lecture[4] == 0:
        return 2
    else:
        return 3

def getBestAction(state):
    #print(Q)
    best = 0
    bestindex = 0
    for i in range(len(Q[state])):
        if Q[state][i]>best:
            best = Q[state][i]
            bestindex = i
    return bestindex

def QLearning():
    # Initialize q-table values to 0
    # Set the percent you want to explore
    epsilon = 0.99
    reducer = 0.95
    min_eps = 0.1
    lr = 0.5
    gamma = 0.85
    a = 2
    for i in range(iterations):
        s = getState()
        if random.uniform(0, 1) < max(min_eps, epsilon):
            a = random.randint(0, len(actions) - 1)
            epsilon *= reducer
        else:
            # Exploit: select the action with max value (future reward)
            a = getBestAction(s)
        activate(a)
        new_s = getState()
        Q[s, a] = Q[s, a] + lr * (rewards[s][a] + gamma * getBestAction(new_s) - Q[s, a])
        for i in range(4):
            for j in range(4):
                Q_save[i][j].append(Q[i,j])
    simulator.save(coo[int(iterations/2):])
    print(Q)
    for i in Q_save:
        for j in i:
            plt.plot(j)
    plt.show()


if __name__ == "__main__":
    QLearning()
