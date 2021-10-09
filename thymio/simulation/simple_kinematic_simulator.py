import shapely
from shapely.geometry import LinearRing, LineString, Point
from numpy import sin, cos, pi, sqrt
from random import random

# A prototype simulation of a differential-drive robot with one sensor

# Constants
###########
R = 0.02  # radius of wheels in meters
L = 0.10  # distance between wheels in meters

W = 2.0  # width of arena
H = 2.0  # height of arena
w = 0.112 # width of the robot
h = 0.11 # height of the robot

simulation_timestep = 0.01  # timestep in kinematics sim (probably don't touch..)

# the world is a rectangular arena with width W and height H
walls = [[-W/2, W/2, -H/2, -H/2], [-W/2, W/2, H/2, H/2], [W/2, W/2, -H/2, H/2], [-W/2, -W/2, H/2, -H/2]]
robot_shape = [[-w/2, w/2, -h/2, -h/2], [-w/2, w/2, h/2, h/2], [w/2, w/2, -h/2, h/2], [-w/2, -w/2, h/2, -h/2]]

# Variables 
###########

x = 0.0   # robot position in meters - x direction - positive to the right 
y = 0.0   # robot position in meters - y direction - positive up
q = 1.57079632679   # robot heading with respect to x-axis in radians 

left_wheel_velocity =  10  # robot left wheel velocity in radians/s
right_wheel_velocity = 10  # robot right wheel velocity in radians/s

# Kinematic model
#################
# updates robot position and heading based on velocity of wheels and the elapsed time
# the equations are a forward kinematic model of a two-wheeled robot - don't worry just use it

def how_far_seg2_from_seg1(seg1, seg2):
	dx1 = seg1[0] - seg1[1]
	dx2 = seg2[0] - seg2[1]
	dy1 = seg1[2] - seg1[3]
	dy2 = seg2[2] - seg2[3]
	if dx1 != 0 and dx2 != 0:
		coef1 = dy1 / dx1
		offset1 = seg1[2] - coef1 * seg1[0]
		coef2 = dy2 / dx2
		offset2 = seg2[2] - coef2 * seg2[0]
		if coef1 != coef2:
			x = (offset2 - offset1) / (coef1 - coef2)
			minx1 = min(seg1[0], seg1[1])
			maxx1 = max(seg1[0], seg1[1])
			minx2 = min(seg2[0], seg2[1])
			maxx2 = max(seg2[0], seg2[1])
			if x >= minx1 and x >= minx2 and x <= maxx1 and x <= maxx2:
				return ((x - seg1[0]) ** 2 + (x * coef2 + offset2 - seg1[2]) ** 2) ** 0.5
	elif dx1 != 0:
		coef1 = dy1 / dx1
		offset1 = seg1[2] - coef1 * seg1[0]
		minx1 = min(seg1[0], seg1[1])
		maxx1 = max(seg1[0], seg1[1])
		if seg2[0] >= minx1 and seg2[0] <= maxx1:
			y = coef1 * seg2[0] + offset1
			miny2 = min(seg2[2], seg2[3])
			maxy2 = max(seg2[2], seg2[3])
			if y > miny2 and y < maxy2:
				return ((seg1[0] - seg2[0]) ** 2 + (seg1[2] - y) ** 2) ** 0.5
	elif dx2 != 0:
		coef2 = dy2 / dx2
		offset2 = seg2[2] - coef2 * seg2[0]
		minx2 = min(seg2[0], seg2[1])
		maxx2 = max(seg2[0], seg2[1])
		if seg1[0] > minx2 and seg1[0] < maxx2:
			y = coef2 * seg1[0] + offset2
			miny1 = min(seg1[2], seg1[3])
			maxy1 = max(seg1[2], seg1[3])
			if y > miny1 and y < maxy1:
				return abs(seg1[2] - y)
	return -1

def collision():
	global x, y, q
	for s in robot_shape:
		angle = q + 1.57079632679
		ss = [x + s[0] * cos(angle) + s[2] * sin(angle), x + s[1] * cos(angle) + s[3] * sin(angle), y + s[2] * cos(angle) - s[0] * sin(angle), y + s[3] * cos(angle) - s[1] * sin(angle)]
		for w in walls:
			if how_far_seg2_from_seg1(ss,w) != -1:
				return True
	return False
	

def simulationstep():
	global x, y, q
	v_x = cos(q)*(R*left_wheel_velocity/2 + R*right_wheel_velocity/2) 
	v_y = sin(q)*(R*left_wheel_velocity/2 + R*right_wheel_velocity/2)
	omega = (R*right_wheel_velocity - R*left_wheel_velocity)/(2*L)    
	x += v_x * simulation_timestep
	y += v_y * simulation_timestep
	q += omega * simulation_timestep

# Simulation loop
#################
file = open("walls.dat", "w")
to_print = ""
for w in walls:
	for j in range(3):
		to_print += str(w[j]) + ','
	to_print += str(w[3]) + '\n'
to_print += "--\n"
for w in robot_shape:
	for j in range(3):
		to_print += str(w[j]) + ','
	to_print += str(w[3]) + '\n'
file.write(to_print)
file.close()
	
file = open("trajectory.dat", "w")

for cnt in range(500):
    #step simulation
	simulationstep()
	if collision():
		file.write( str(x) + "," + str(y) + "," + str(q) + "\n")
		break
    #check collision with arena walls 
        
	file.write( str(x) + "," + str(y) + "," + str(q) + "\n")

file.close()
    
