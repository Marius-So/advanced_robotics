import numpy as np
import cv2
import math
from simple_kinematic_simulator import lidar_sensor

current = [1, 2, 3, 4, 5, 6]
p1 = [0, 2, 3, 4, 5, 6]
p2 = [0, 0, 3, 4, 5, 6]
p3 = [0, 0, 0, 4, 5, 6]

simulated = [p1, p2, p3]


def compare(current, simulated):
    differences = []
    for view in simulated:
        aux = []
        for i in range(view):
            aux.append(current[i] - simulated[i])
        differences.append(aux)
    sum = []
    small = 0
    for dif in differences:
        for i in range(dif):
            sum[i] = sum[i] + dif[i]
        print(sum)

    current = []
    center, widthheight, angle = cv2.minAreaRect(
        np.asarray(res).astype(np.int))

# lidar_sensor(walls,x,y,q)


def method():
    spaceResolution = 0.1 #meter
    W = 2.0  # width of arena
    H = 2.0  # height of arenai
    walls = [[-W/2, W/2, -H/2, -H/2], [-W/2, W/2, H/2, H/2],
             [W/2, W/2, -H/2, H/2], [-W/2, -W/2, H/2, -H/2]]
    map = [[0 for i in range (W/spaceResolution)] for j in range(H/spaceResolution)] 
    print(map)

if __name__ == "__main__":
    method()
    #rest = 0
    #compare(current, simulated)
