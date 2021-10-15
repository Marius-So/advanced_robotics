import csv
from copy import copy, deepcopy
import numpy as np
import cv2
import math
from numpy.lib.function_base import diff
from kinematic_simulator import kinetic_simulator
from random import randint

def getPointValues(i, j, angle, W, H, resolution, walls):
    angle = 0
    ks = kinetic_simulator(walls)
    x, y = j * resolution - (W - resolution) / 2, - \
        i * resolution + (H - resolution) / 2
    return ks.lidar_sensor(x, y, angle)

def generateSampleTest(size):
    sample = [randint(0, 9) for i in range(size)]
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


def getFitability(current, simulated):
    differences = [0 for i in range(len(current))]
    fitability = 0
    for i in range(len(differences)):
        diff = current[i] - simulated[i]
        differences[i] = diff
        fitability = fitability + math.sqrt(math.pow(diff,2))
    #print("differences: " + str(differences))
    #print("fitability: " + str(fitability))
    return fitability

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
            #writer.writerow([ns[i]] + res[i, :]. tolist())
            print("bu")

if __name__ == "__main__":

    resolution = 0.5  # meter
    W = 1.0  # width of arena
    H = 1.0  # height of arena
    walls = [[-W/2, W/2, -H/2, -H/2], [-W/2, W/2, H/2, H/2],
             [W/2, W/2, -H/2, H/2], [-W/2, -W/2, H/2, -H/2]]

    #print(getPointValues(0,0,0,W,H,resolution,walls))
    current, sample = generateSampleTest(4)
    getFitability(current, sample)
