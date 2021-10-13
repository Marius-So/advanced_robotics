from copy import copy, deepcopy
import numpy as np
import cv2
import math
from simple_kinematic_simulator import kinetic_simulator
from random import randint, randrange, sample


def getPointValues(i, j, angle, W, H, resolution, walls):
    angle = 0
    ks = kinetic_simulator(walls)
    x, y = j * resolution - (W - resolution)/ 2, -i * resolution + (H - resolution) / 2
    return ks.lidar_sensor(x, y, angle)


def generateSampleTest(size):
    sample = [[[randint(0, 9) for i in range(size)]
               for j in range(size)] for z in range(size)]
    print("sample: " + str(sample))
    current = [randint(0, 9) for i in range(size)]
    print("current: " + str(current))
    return current, sample


def method(W, H, resolution, walls):
    map = [[0 for i in range(int(W/resolution))]
           for j in range((int)(H/resolution))]
    simuRes = deepcopy(map)
    ks = kinetic_simulator(walls)
    for i in range(len(map)):
        for j in range(len(map[i])):
            x, y = j * resolution - \
                (W - resolution) / 2, -i * \
                resolution + (H - resolution) / 2
            simuRes[i][j] = ks.lidar_sensor(x, y, 0)
    print("simulation values:" + str(simuRes))


def compare(current, simulated):
    differences = sample = [[[0 for i in range(len(current))] for j in range(
        len(current))] for k in range(len(current))]
    for i in range(len(simulated)):
        #print("i = " + str(i))
        for j in range(len(simulated[i])):
            #print("j = " + str(j))
            rest = []
            for k in range(len(simulated[i][j])):
                rest = (current[k] - simulated[i][j][k])
                differences[i][j][k] = rest
    print("differences: " + str(differences))

    summatory = [[0] * len(differences)] * len(differences[0])
    #print("summatory: " + str(summatory))
    for i in range(len(differences)):
        for j in range(len(differences[i])):
            sum = 0
            for k in (differences[i][j]):
                sum = sum + math.sqrt(math.pow(k, 2))
            summatory[i][j] = sum
            print("sum: " + str(sum))
            sum = 0
    print("summatory: " + str(summatory))

    # in percentage:
    percent = [[0] * len(summatory)] * len(summatory[0])
    totalSum = 0
    for s in sum:
        totalSum = totalSum + s
    for s in sum:
        aux = s/totalSum
        percent.append(aux)
    # print(percent)

    return min(sum)


if __name__ == "__main__":

    resolution = 0.5  # meter
    W = 1.0  # width of arena
    H = 1.0  # height of arena
    walls = [[-W/2, W/2, -H/2, -H/2], [-W/2, W/2, H/2, H/2],
             [W/2, W/2, -H/2, H/2], [-W/2, -W/2, H/2, -H/2]]

    # method(W,H,resolution,walls)
    #compare(current, simulated)
    current, sample = generateSampleTest(2)
    compare(current, sample)
