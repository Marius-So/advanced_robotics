import csv
from copy import copy, deepcopy
import numpy as np
import cv2
import math
from simple_kinematic_simulator import kinetic_simulator
from random import randint, randrange, sample

def getPointValues(i, j, angle, W, H, resolution, walls):
    angle = 0
    ks = kinetic_simulator(walls)
    # I have the feeling that this convertion to x,y is wrong
    x, y = j * resolution - (W - resolution) / 2, - \
        i * resolution + (H - resolution) / 2
    return ks.lidar_sensor(x, y, angle)


def generateSampleTest(size):
    sample = [[[randint(0, 9) for i in range(size)]
               for j in range(size)] for z in range(size)]
    print("sample: " + str(sample))
    current = [randint(0, 9) for i in range(size)]
    print("current: " + str(current))
    return current, sample


def getSimulatedValues(W, H, resolution, walls):
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
    differences = [[[0 for i in range(len(current))] for j in range(
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
    toPrint(summatory)

    # in percentage:
    tot = 0
    for i in range(len(summatory)):
        for j in range(len(summatory[i])):
            tot = tot + summatory[i][j]
    percent = [[0] * len(differences)] * len(differences[0])
    for i in range(len(summatory)):
        for j in range(len(summatory[i])):
            percent[i][j] = summatory[i][j]/tot
    print(percent)

    # to get the position of the min:
    minPosition = (0, 0)
    min = 99999
    for i in range(len(summatory)):
        for j in range(len(summatory[i])):
            if(summatory[i][j] < min):
                min = summatory[i][j]
                minPosition = (i, j)
    print(minPosition)


def toPrint(list):  # two three-dimensional list
    print("toPrint")
    tp = []
    
    for i in range(len(list)):
        aux = []
        for j in range(len(list)):
            aux.append(list[i][j])
            print(aux)
        tp.append(aux)
        aux.clear
    print(tp)

    print("end")

    for i in range(len(list)):
        line = []
        for j in range(len(list[i])):
            line.append(i)
            line.append(j)
            line.append(list[i][j])
            print(line)
            tp.append(line)
    print("tp:" + str(tp))


def write_csv(list, filename: str):
    with open(filename, 'w') as f:
        writer = csv. writer(f)
        for n in range(len(list)):
            writer.writerow([ns[i]] + res[i, :]. tolist())


if __name__ == "__main__":

    resolution = 0.5  # meter
    W = 1.0  # width of arena
    H = 1.0  # height of arena
    walls = [[-W/2, W/2, -H/2, -H/2], [-W/2, W/2, H/2, H/2],
             [W/2, W/2, -H/2, H/2], [-W/2, -W/2, H/2, -H/2]]

    print(getPointValues(0,0,0,W,H,resolution,walls))
    #current, sample = generateSampleTest(2)
    #compare(current, sample)
