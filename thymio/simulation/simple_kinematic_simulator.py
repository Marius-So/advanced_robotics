from numpy import sin, cos, pi, sqrt

# A prototype simulation of a differential-drive robot with one sensor
# Constants
###########
R = 0.02  # radius of wheels in meters
L = 0.10  # distance between wheels in meters
weight = 0.27 # (in kg)

w = 0.112 # x of the robot
l = 0.11 # y of the robot
h = 0.053 # z of the robot

simulation_timestep = 0.01  # timestep in kinematics sim (probably don't touch..)

robot_shape = [[-w/2, w/2, -l/2, -l/2], [-w/2, w/2, l/2, l/2], [w/2, w/2, -l/2, l/2], [-w/2, -w/2, l/2, -l/2]]
sensor_shape = [[-0.4, -0.4, l/2, h/2 + 0.16], [-0.2, -0.2, l/2, l/2 + 0.16], [0, 0, l/2, l/2 + 0.16], [0.2, 0.2, l/2, l/2 + 0.16], [0.4, 0.4, l/2, l/2 + 0.16], [-0.3, -0.3, -l/2, -l/2 - 0.16], [0.3, 0.3, -l/2, -l/2 - 0.16]]


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


def collision(walls,x,y,q):
	for s in robot_shape:
		angle = q - 1.57079632679
		ss = [x + s[0] * cos(angle) + s[2] * sin(angle), x + s[1] * cos(angle) + s[3] * sin(angle), y + s[2] * cos(angle) - s[0] * sin(angle), y + s[3] * cos(angle) - s[1] * sin(angle)]
		for w in walls:
			d = how_far_seg2_from_seg1(ss,w)
			if d != (-1, -1):
				return True
	return False

def lidar_sensor(walls,x,y,q): #return (array[0..359]) of lectures of lildar
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
			
#return the output of the 7 InfraRed Sensors in the thymio.
def thymio_sensor(walls, x,y,q):
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

def step(x, y, q, r_w_v, l_w_v):
	global simulation_timestep
	v_x = cos(q)*(R*l_w_v/2 + R*r_w_v/2) 
	v_y = sin(q)*(R*l_w_v/2 + R*r_w_v/2)
	omega = (R*r_w_v - R*l_w_v)/(2*L)    
	x += v_x * simulation_timestep
	y += v_y * simulation_timestep
	q += omega * simulation_timestep
	return [x, y, q]


def save(coo, walls):
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
	
	file = open("walls.dat", "w")
	file.write(to_print_w)
	file.close()
	file = open("trajectory.dat", "w")
	file.write(to_print_c)
	file.close()   

def simulate(x, y, q, r_w_v, l_w_v, sec, walls):
	global simulation_timestep
	coo = []
	for cnt in range(int(sec / simulation_timestep)):
		x, y, q = step(x,y,q,r_w_v, l_w_v)
		coo.append([x,y,q])
		if collision(walls, x,y,q):
			return coo, 
	return coo

if __name__ == "__main__":
	W = 2.0  # width of arena
	H = 2.0  # height of arenai
	walls = [[-W/2, W/2, -H/2, -H/2], [-W/2, W/2, H/2, H/2], [W/2, W/2, -H/2, H/2], [-W/2, -W/2, H/2, -H/2]]
	coo = simulate(0, 0, 0, 10, 10, 5, walls)
	save(coo[0], walls)
