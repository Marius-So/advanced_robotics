import csv
from copy import copy, deepcopy
import numpy as np
import cv2
import math
from numpy.lib.function_base import append, diff
from kinematic_simulator import kinematic_simulator
from random import randint, sample


class Location:
    def __init__(self, H,W,testPoint) -> None:
        self.data = [[]]
        walls = [[-W/2, W/2, -H/2, -H/2], [-W/2, W/2, H/2, H/2],
             [W/2, W/2, -H/2, H/2], [-W/2, -W/2, H/2, -H/2]]
        self.ks = kinematic_simulator(walls)
        self.testPoint = testPoint
        self.H = H
        self.W = W

    def getPointValues(self, i, j, angle = 0):
        return self.ks.lidar_sensor(i, j, angle)

    def generateSampleTest(self, size):
        sample = [randint(0, 5)/10 for i in range(size)]
        #print("sample: " + str(sample))
        current = [randint(0, 9) for i in range(size)]
        #print("current: " + str(current))
        return current, sample

    def getFitability(self, current, simulated):
        differences = [0 for i in range(len(current))]
        fitability = 0
        for i in range(len(differences)):
            diff = current[i] - simulated[i]
            differences[i] = diff
            fitability = fitability + math.sqrt(math.pow(diff, 2))
        # print("differences: " + str(differences))
        # print("fitability: " + str(fitability))
        return fitability

    def getDistance(self, a, b):
        return math.sqrt(math.pow((a[0]-b[0]), 2)+math.pow((a[1]-b[1]), 2))

    def getSamplePoints(self, prev, depth):
        #print("getSample depth: " + str(depth))
        samplePoints = []
        p1 = (prev[0] + self.H/(2**(depth+2)), prev[1] - self.W/(2**(depth+2)))
        p2 = (prev[0] + self.H/(2**(depth+2)), prev[1] + self.W/(2**(depth+2)))
        p3 = (prev[0] - self.H/(2**(depth+2)), prev[1] + self.W/(2**(depth+2)))
        p4 = (prev[0] - self.H/(2**(depth+2)), prev[1] - self.W/(2**(depth+2)))
        samplePoints.append(p1)
        samplePoints.append(p2)
        samplePoints.append(p3)
        samplePoints.append(p4)
        #print(samplePoints)
        return samplePoints

    def recursion(self, realValues, prev, depth, angle):
        dataDepth = []
        # depth = depth + 1
        # cutoffFunction
        if(depth >= 20):
            return prev

        dataDepth.append(depth)
        dataDepth.append(prev[0])
        dataDepth.append(prev[1])
        dataDepth.append(self.getDistance(self.testPoint, prev))
        self.data.append(dataDepth)

        sample = self.getSamplePoints(prev, depth)
        bestPoint = (0, 0)
        minFitability = 999999
        #print(sample)
        for point in sample:
            simulatedValues = self.getPointValues(point[0], point[1], angle)
            fitability = self.getFitability(realValues, simulatedValues)

            if(minFitability > fitability):
                minFitability = fitability
                bestPoint = point
        print("bestPoint: " + str(bestPoint))
        #print("Fitability: " + str(fitability))
        self.recursion(realValues, bestPoint, depth + 1, angle)

    def write_csv(self, filename: str):
        header = ["depth", "x", "y", "distance"]
        with open(filename, 'w', encoding='UTF8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(self.data)


if __name__ == "__main__":
    W = 4.0  # width of arena
    H = 4.0  # height of arena
    testPoint = (-1.38, -0.958)
    loc = Location(H,W,testPoint)
    current = loc.getPointValues(testPoint[0], testPoint[1])
    loc.recursion(current, (0, 0), 0)
    # print(data)
    loc.write_csv("thymio\\data\\DataLocationExperiments.csv")
