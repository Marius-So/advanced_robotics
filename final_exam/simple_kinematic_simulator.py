from numpy import sin, cos, pi, sqrt

# A prototype simulation of a differential-drive robot with one sensor

# Constants
###########
R = 0.02  # radius of wheels in meters
L = 0.10  # distance between wheels in meters
weight = 0.27 # (in kg)

W = 2.0  # width of arena
H = 2.0  # height of arena
w = 0.112 # x of the robot
l = 0.11 # y of the robot
h = 0.053 # z of the robot

simulation_timestep = 0.01  # timestep in kinematics sim (probably don't touch..)

walls = [[-W/2, W/2, -H/2, -H/2], [-W/2, W/2, H/2, H/2], [W/2, W/2, -H/2, H/2], [-W/2, -W/2, H/2, -H/2]]
robot_shape = [[-w/2, w/2, -l/2, -l/2], [-w/2, w/2, l/2, l/2], [w/2, w/2, -l/2, l/2], [-w/2, -w/2, l/2, -l/2]]
sensor_shape = [[-0.4, -0.4, l/2, h/2 + 0.16], [-0.2, -0.2, l/2, l/2 + 0.16], [0, 0, l/2, l/2 + 0.16], [0.2, 0.2, l/2, l/2 + 0.16], [0.4, 0.4, l/2, l/2 + 0.16], [-0.3, -0.3, -l/2, -l/2 - 0.16], [0.3, 0.3, -l/2, -l/2 - 0.16]]

# Variables 
###########

coo = []
speed = [0,0]
x = 0.0   # robot position in meters - x direction - positive to the right 
y = 0.0   # robot position in meters - y direction - positive up
q = 1.57079632679   # robot heading with respect to x-axis in radians 

left_wheel_velocity =  10  # robot left wheel velocity in radians/s
right_wheel_velocity = 10  # robot right wheel velocity in radians/s

# Kinematic model
#################
# updates robot position and heading based on velocity of wheels and the elapsed time
# the equations are a forward kinematic model of a two-wheeled robot - don't worry just use it

#use this function to calculate intersection point with seg1 and seg2
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
				return x, x * coef2 + offset2
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
				return seg2[0], y
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
				return seg1[0], y
	return -1, -1

def frictions():
	global x,y,q, h, w, speed
	#air_volumic_mass = 1.229
	#drag coefficient = 0.5
	surface = w*h
	ret = [[[x,y], [speed[0]**2,speed[1]**2]]]
	if speed[0] > 0:
		ret[0][1][0] *= -w*h*1.229*0.5
	else:
		ret[0][1][0] *= w*h*1.229*0.5
	if speed[1] > 0:
		ret[0][1][1] *= -w*h*1.229*0.5
	else:
		ret[0][1][1] *= w*h*1.229*0.5
	return ret


def wheels():
	global x,y,L,q
	angle = q - 1.57079632679
	if y == 0:
		return [[[x + L/2 * cos(angle),y + L/2 * sin(angle)], [0,5]], [[x - L/2 * cos(angle),y - L/2 * sin(angle)], [0,5]]]
	return []

def collision():
	global x, y, q, coo
	for s in robot_shape:
		angle = q - 1.57079632679
		ss = [x + s[0] * cos(angle) + s[2] * sin(angle), x + s[1] * cos(angle) + s[3] * sin(angle), y + s[2] * cos(angle) - s[0] * sin(angle), y + s[3] * cos(angle) - s[1] * sin(angle)]
		for w in walls:
			d = how_far_seg2_from_seg1(ss,w)
			#if d != (-1, -1):
			#	print(d[0], d[1])
			#	print(x - coo[-2][0], y - coo[-2][1])				
	return []

def lidar_sensor():
	global x,y,q
	ret = []
	for i in range(0,360):
		angle = q + i / 57.2957795131 - 1.57079632679
		ss = [x, y, x + 10 * cos(angle), y + 10 * sin(angle)]
		minv = 999999999
		for w in walls:
			v = how_far_seg2_from_seg1(ss,w)
			d = ((ss[0] - v[0]) ** 2 + (ss[2] - v[1]) ** 2) ** 0.5
			if d < minv:
				minv = d
		ret.append(minv)
	return ret
			

def thymio_sensor():
	global x, y, q
	ret = []
	for s in sensor_shape:
		angle = q - 1.57079632679
		ss = [x + s[0] * cos(angle) + s[2] * sin(angle), x + s[1] * cos(angle) + s[3] * sin(angle), y + s[2] * cos(angle) - s[0] * sin(angle), y + s[3] * cos(angle) - s[1] * sin(angle)]
		minv = 99999999
		for w in walls:
			v = how_far_seg2_from_seg1(ss,w)
			if v != (-1,-1):
				d = ((ss[0] - v[0]) ** 2 + (ss[2] - v[1]) ** 2) ** 0.5
				if d < minv:
					minv = d
		if minv > 16:
			ret.append(0)
		else:
			#ret.append(0.00007*minv**4 + 0.025*minv**3 - 2.9084*minv**2 + 103.76*minv + 3567.7) the equation suck
			ret.append(minv)
	return ret

def pfd(forces):
	global x, y, q, speed
	
	result = [0,0]
	for i in forces:
		result[0] += i[1][0]
		result[1] += i[1][1]
	result[0] /= weight
	result[1] /= weight
	speed[0] += result[0] * simulation_timestep
	speed[1] += result[1] * simulation_timestep
	x += speed[0] * simulation_timestep
	y += speed[1] * simulation_timestep
	
	for i in forces:
		if i[1][0] != 0 or i[1][1] != 0:
			print(i)
			if i[1][0] == 0:
				normalized_orthogonal = [1, 0]
			elif i[1][1] == 0:
				normalized_orthogonal = [0, 1]
			else:
				normalized_orthogonal = [1/(1 + i[1][0] ** 2/ i[1][1] ** 2), -i[1][0]/(i[1][1] + i[1][0] ** 2/i[1][1])]
		#i[0] + distance * normalized_orthogonal + b * i[1] = [x,y]
		# we want find the distance
		# 
	
# Simulation loop
#################
for cnt in range(500):
    #step simulation
	forces = []
	forces.extend(wheels())
	forces.extend(frictions())
	forces.extend(collision())
	pfd(forces)
    #check collision with arena walls 
	coo.append([x, y, q])

to_print_w = ""
for w in walls:
    for j in range(3):
        to_print_w += str(w[j]) + ','
    to_print_w += str(w[3]) + '\n'
to_print_w += "--\n"
for w in robot_shape:
    for j in range(3):
        to_print_w += str(w[j]) + ','
    to_print_w += str(w[3]) + '\n'

to_print_c = ""
for i in coo:
	for j in range(2):
		to_print_c += str(i[j]) + ','
	to_print_c += str(i[2]) + '\n'

file = open("walls.date", "w")
file.write(to_print_w)
file.close()
file = open("trajectory.dat", "w")
file.write(to_print_c)
file.close()   
