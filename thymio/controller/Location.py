import csv
from copy import copy, deepcopy
import numpy as np
import cv2
import math
from numpy.lib.function_base import append, diff
from kinematic_simulator import kinematic_simulator
from random import randint, sample


class Location:
    def __init__(self, H, W) -> None:
        self.data = [[]]
        self.H = H
        self.W = W
        walls = [[-W/2, W/2, -H/2, -H/2], [-W/2, W/2, H/2, H/2],
                 [W/2, W/2, -H/2, H/2], [-W/2, -W/2, H/2, -H/2]]
        self.ks = kinematic_simulator(walls)
        self.H = H
        self.W = W

    def getPointValues(self, i, j, angle):
        return self.ks.lidar_sensor(i, j, angle)

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
        p1 = (prev[0] + self.W/(2**(depth+2)), prev[1] - self.H/(2**(depth+2)))
        p2 = (prev[0] + self.W/(2**(depth+2)), prev[1] + self.H/(2**(depth+2)))
        p3 = (prev[0] - self.W/(2**(depth+2)), prev[1] + self.H/(2**(depth+2)))
        p4 = (prev[0] - self.W/(2**(depth+2)), prev[1] - self.H/(2**(depth+2)))
        samplePoints.append(p1)
        samplePoints.append(p2)
        samplePoints.append(p3)
        samplePoints.append(p4)
        # print(samplePoints)
        return samplePoints

    def findLocationBySimulation(self, realValues, angle, prev, depth):
        dataDepth = []
        #print("angle: " + str(angle))
        # cutoffFunction
        if(depth >= 20):
            return prev

        dataDepth.append(depth)
        dataDepth.append(prev[0])
        dataDepth.append(prev[1])
        #dataDepth.append(self.getDistance(self.testPoint, prev))
        self.data.append(dataDepth)

        sample = self.getSamplePoints(prev, depth)
        bestPoint = (0, 0)
        minFitability = 999999
        # print(sample)
        for point in sample:
            simulatedValues = self.getPointValues(point[0], point[1], angle)
            fitability = self.getFitability(realValues, simulatedValues)

            if(minFitability > fitability):
                minFitability = fitability
                bestPoint = point
        print("bestPoint: " + str(bestPoint))
        #print("Fitability: " + str(fitability))
        self.findLocationBySimulation(realValues, angle, bestPoint, depth + 1)

    def write_csv(self, filename: str):
        header = ["depth", "x", "y", "distance"]
        with open(filename, 'w', encoding='UTF8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(self.data)

    def findLocationByDistance(self, realValues, angle):
        front = realValues[0]/1000
        back = realValues[180]/1000
        right = realValues[270]/1000
        left = realValues[90]/1000
        #print("front, back, right, left")
        #print(front, back, right, left)
        long = 0
        short = 0

        if((front + back) >= (right + left)):
            # im looking at 0 or 180 in W direction
            long = front + back
            short = right + left
        else:
            # im looking at 90 or 270 in H direction
            long = right + left
            short = front + back

        print("long: " + str(long))
        print("short: " + str(short))

        #print(front, back, right, left)
        if(angle == math.radians(0)):
            x = self.W/2 - front
            y = self.H/2 - left
        if(angle == math.radians(90)):
            x = self.W/2 - right
            y = self.H/2 - front
        if(angle == math.radians(180)):
            x = -self.W/2 + front
            y = -self.H/2 + left
        if(angle == math.radians(270)):
            x = -self.W/2 + right
            y = -self.H/2 + front
        print("(x,y): " + "(" + str(x) + " , " + str(y) + ")")
        
        print("LONG IS >=W, I GUESS WE DIDNT MEASURE THE MAP PROPERLY OR THE LIDAR HAS AN INSANE ERROR")
        print(math.degrees(math.cos(W/long)))


if __name__ == "__main__":
    # loc.write_csv("thymio\\data\\DataLocationExperiments.csv")
    W = 2.0  # width of arena
    H = 1.0  # height of arena

    realValues = [357.5, 358.75, 360.25, 363.0, 363.25, 364.25, 365.0, 366.5, 367.0, 368.25, 370.0, 370.25, 371.75, 374.25, 376.5, 377.75, 381.0, 382.0, 386.75, 389.25, 389.75, 395.0, 397.25, 402.25, 405.0, 406.75, 413.25, 416.0, 420.75, 423.0, 429.75, 436.0, 440.75, 442.75, 451.25, 458.25, 467.25, 472.0, 477.0, 486.5, 496.25, 503.75, 507.5, 520.0, 532.5, 541.25, 544.5, 559.5, 575.5, 591.75, 593.5, 610.0, 630.75, 651.75, 665.75, 674.25, 699.0, 726.0, 746.5, 755.75, 786.25, 827.0, 852.0, 867.5, 913.25, 964.5, 1022.25, 1069.25, 1096.5, 1144.25, 1298.25, 1205.5, 1199.25, 1194.75, 1192.25, 1182.5, 1179.5, 1176.75, 1170.75, 1168.75, 1165.75, 1163.75, 1159.0, 1159.0, 1155.75, 1153.0, 1151.0, 1148.5, 1148.5, 1150.0, 1155.5, 1155.75, 1154.75, 1160.0, 1160.25, 1161.25, 1164.0, 1170.75, 1171.25, 1177.0, 1180.0, 1189.0, 1188.0, 1196.0, 1201.75, 1208.5, 1209.5, 1220.25, 1231.5, 1234.5, 1247.25, 1254.75, 1269.25, 1272.25, 1287.75, 1299.5, 1317.75, 1319.25, 1335.0, 1353.25, 1352.0, 1373.0, 1368.25, 1322.0, 1309.25, 1274.75, 1238.5, 1214.0, 1198.75, 1164.5, 1130.75, 1128.25, 1105.5, 1077.0, 1063.75, 1050.25, 1032.25, 1008.0, 1002.25, 978.5, 966.75, 955.0, 948.75, 931.75, 915.0, 913.0, 901.25, 887.75, 878.0, 874.75, 862.25, 852.0, 850.5, 842.25, 832.75, 826.0, 825.5, 815.5, 808.25, 805.75, 801.75, 796.25, 797.75, 792.0, 785.25, 783.5, 782.75, 780.25, 775.25, 771.75, 770.5, 769.0, 766.75, 764.75, 764.75,
                  762.0, 760.25, 760.0, 758.0, 760.25, 762.5, 761.75, 764.5, 766.0, 766.5, 769.25, 772.25, 772.75, 775.25, 778.0, 783.25, 784.5, 785.0, 792.0, 796.75, 796.5, 803.0, 810.0, 818.5, 817.0, 821.25, 830.25, 842.5, 843.25, 852.25, 862.25, 868.75, 875.0, 887.25, 901.75, 909.75, 917.25, 931.25, 946.5, 947.0, 964.75, 983.25, 993.5, 1004.5, 1024.75, 1050.0, 1058.75, 1070.5, 1186.25, 1066.25, 1052.5, 1039.5, 1020.5, 1010.5, 998.0, 978.75, 960.5, 952.5, 941.5, 928.25, 920.75, 912.75, 897.5, 885.75, 885.25, 874.5, 861.25, 859.5, 851.75, 842.25, 834.75, 832.25, 824.25, 818.25, 815.5, 815.25, 805.75, 798.75, 799.75, 795.0, 790.75, 787.75, 785.25, 782.0, 778.25, 778.0, 776.75, 773.5, 773.75, 771.75, 770.0, 765.75, 765.5, 764.0, 765.25, 768.75, 767.5, 772.75, 773.25, 776.75, 775.25, 778.25, 781.25, 784.5, 785.0, 789.25, 791.75, 793.0, 798.0, 803.75, 811.25, 813.0, 818.0, 825.5, 830.5, 833.5, 839.75, 847.75, 847.25, 809.0, 782.5, 752.5, 745.25, 713.5, 692.25, 685.5, 658.25, 640.0, 634.5, 611.75, 596.75, 592.0, 573.25, 560.5, 556.0, 540.0, 530.25, 526.0, 512.0, 499.25, 497.5, 488.25, 477.25, 470.0, 471.5, 456.75, 451.5, 449.25, 441.5, 436.0, 429.25, 428.0, 419.5, 414.75, 412.5, 407.75, 404.5, 401.75, 397.25, 393.5, 390.75, 389.5, 386.0, 383.75, 381.75, 379.0, 377.5, 376.5, 373.25, 371.5, 370.25, 369.0, 366.75, 365.75, 365.5, 364.5, 363.0, 362.75, 361.75, 361.75, 360.0, 360.0, 359.75, 359.5, 358.75]
    angle = math.pi/2
    loc = Location(H, W)
    #loc.findLocationBySimulation(realValues, angle, (0, 0), 0)
    # print(math.degrees(angle))
    # loc.findLocationByDistance(realValues)

    # comparing methods:
    walls = [[-W/2, W/2, -H/2, -H/2], [-W/2, W/2, H/2, H/2],
             [W/2, W/2, -H/2, H/2], [-W/2, -W/2, H/2, -H/2]]
    ks = kinematic_simulator(walls)

    angle = math.radians(0)
    # CAREFULL WITH THE . and , the mutherfucker doesnt show an error
    testPoint = (0.1, 0)
    #current = ks.lidar_sensor(testPoint[0], testPoint[1], angle)
    print("Real angle: " + str(angle) +
          "[rads] " + str(math.degrees(angle)) + "[degrees]")
    #loc.findLocationBySimulation(realValues, 0, (0, 0), 0)
    loc.findLocationByDistance(realValues, angle)
