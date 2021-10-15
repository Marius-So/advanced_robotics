import csv
from copy import copy, deepcopy
import numpy as np
import cv2
import math
from numpy.lib.function_base import diff
from kinematic_simulator import kinetic_simulator
from random import randint

def getPointValues(i, j, ks):
    angle = 0
    return ks.lidar_sensor(i, j, angle)


def generateSampleTest(size):
    sample = [randint(0, 5)/10 for i in range(size)]
    print("sample: " + str(sample))
    current = [randint(0, 9) for i in range(size)]
    print("current: " + str(current))
    return current, sample


def getFitability(current, simulated):
    differences = [0 for i in range(len(current))]
    fitability = 0
    for i in range(len(differences)):
        diff = current[i] - simulated[i]
        differences[i] = diff
        fitability = fitability + math.sqrt(math.pow(diff, 2))
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

def getSamplePoints(prev, depth, H, W):
    samplePoints = []
    p1 = (prev[0] + H/(2**depth), prev[1] - W/(2**depth))
    p2 = (prev[0] + H/(2**depth), prev[1] + W/(2**depth))
    p3 = (prev[0] - H/(2**depth), prev[1] + W/(2**depth))
    p4 = (prev[0] - H/(2**depth), prev[1] - W/(2**depth))
    samplePoints.append(p1)
    samplePoints.append(p2)
    samplePoints.append(p3)
    samplePoints.append(p4)
    return samplePoints


def recursion(realValues, prev, depth, H, W,ks):
    #print("--------------depth: " + str(depth))
    depth = depth + 1
    # cutoffFunction
    if(depth >= 20):
        return prev

    sample = getSamplePoints(prev, depth, H, W)
    #print(sample)

    bestPoint = (0, 0)
    minFitability = 999999

    for point in sample:
        simulatedValues = getPointValues(point[0], point[1], ks)
        fitability = getFitability(realValues, simulatedValues)

        if(minFitability > fitability):
            minFitability = fitability
            bestPoint = point
    print("bestPoint: " + str(bestPoint))
    #print("Fitability: " + str(fitability))
    recursion(realValues, bestPoint, depth, H, W, ks)


if __name__ == "__main__":
    W = 4.0  # width of arena
    H = 4.0  # height of arena
    walls = [[-W/2, W/2, -H/2, -H/2], [-W/2, W/2, H/2, H/2],
            [W/2, W/2, -H/2, H/2], [-W/2, -W/2, H/2, -H/2]]
    #ks = kinetic_simulator(walls)

    #testPoint = (1.9,1.9)
    #current = getPointValues(testPoint[0],testPoint[1],ks)
    #recursion(current, (0, 0), 0, H, W, ks)

    ks2 = kinetic_simulator(walls)
    testPoint = (-0.23,1.11)
    current = getPointValues(testPoint[0],testPoint[1],ks2)
    recursion(current, (0, 0), 1, H, W, ks2)
