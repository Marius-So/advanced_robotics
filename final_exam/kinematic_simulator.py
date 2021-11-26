from numpy import sin, cos, pi, sqrt, nan

class kinematic_simulator:
	def __init__(self, walls, robots, simulation_timestep = 0.01) -> None:

		# A prototype simulation of a differential-drive robot with one sensor
		# Constants
		###########

		self.R = 0.02  # radius of wheels in meters
		self.L = 0.10  # distance between wheels in meters
		self.weight = 0.27 # (in kg)

		self.w = 0.112 # x of the robot
		self.l = 0.11 # y of the robot
		self.h = 0.053 # z of the robot
		self.robots = robots
		

		self.simulation_timestep = simulation_timestep  # timestep in kinematics sim (probably don't touch..)

		self.robot_shape = [[-self.l/2, self.l/2, -self.w/2, -self.w/2], [-self.l/2, self.l/2, self.w/2, self.w/2], [self.l/2, self.l/2, -self.w/2, self.w/2], [-self.l/2, -self.l/2, self.w/2, -self.w/2]]
		self.sensor_shape = [[self.l/2, self.l/2 + 0.16, 0.04, 0.06], [self.l/2, self.l/2 + 0.16, 0.02, 0.02], [self.l/2, self.l/2 + 0.16, 0, 0], [self.l/2, self.l/2 + 0.16, -0.02, -0.02], [self.l/2, self.l/2 + 0.16, -0.04, -0.06], [-self.l/2, -self.l/2 - 0.16, -0.03, -0.03], [-self.l/2, -self.l/2 - 0.16, 0.03, 0.03]]

		self.walls = walls
		# Kinematic model
		#################
		# updates robot position and heading based on velocity of wheels and the elapsed time
		# the equations are a forward kinematic model of a two-wheeled robot - don't worry just use it

		#use this function to calculate intersection point with seg1 and seg2
	def how_far_seg2_from_seg1(self, seg1, seg2):
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
			coef2 = dy2/ dx2
			offset2 = seg2[2] - coef2 * seg2[0]
			minx2 = min(seg2[0], seg2[1])
			maxx2 = max(seg2[0], seg2[1])
			if seg1[0] > minx2 and seg1[0] < maxx2:
				y = coef2 * seg1[0] + offset2
				miny1 = min(seg1[2], seg1[3])
				maxy1 = max(seg1[2], seg1[3])
				if y > miny1 and y < maxy1:
					return seg1[0], y
		return None

	def collision(self,i):
		x = self.robots[i][-1][0]
		y = self.robots[i][-1][1]
		q = self.robots[i][-1][2]
		for s in self.robot_shape:
			ss = [x + s[0] * cos(q) + s[2] * sin(q), x + s[1] * cos(q) + s[3] * sin(q), y + s[2] * cos(q) - s[0] * sin(q), y + s[3] * cos(q) - s[1] * sin(q)]
			for w in self.walls:
				d = self.how_far_seg2_from_seg1(ss,w)
				if d != None:
					return True
			for j in range(len(self.robots)):
				if j != i:
					xx = robot[j][-1][0]
					yy = robot[j][-1][1]
					qq = robot[j][-1][2]
					for s in self.robot_shape:
						ss2 = [xx + s[0] * cos(qq) + s[2] * sin(qq), xx + s[1] * cos(qq) + s[3] * sin(qq), yy + s[2] * cos(qq) - s[0] * sin(qq), yy + s[3] * cos(qq) - s[1] * sin(qq)]
						v = self.how_far_seg2_from_seg1(ss,ss2)
						if v != None:
							return True
		return False

	def lidar_sensor(self, i):
		ret = []
		x = self.robots[i][-1][0]
		y = self.robots[i][-1][1]
		q = self.robots[i][-1][2]
		for a in range(0,360):
			angle = q + a / 57.2957795131
			ss = [x, x + 15 * cos(angle), y, y + 15 * sin(angle)]
			minv = 999999999
			for w in self.walls:
				v = self.how_far_seg2_from_seg1(ss,w)
				if v != None:
					d = ((ss[0] - v[0]) ** 2 + (ss[2] - v[1]) ** 2) ** 0.5
					if d < minv:
						minv = d
			for j in range(len(self.robots)):
				if j != i:
					xx = self.robots[j][-1][0]
					yy = self.robots[j][-1][1]
					qq = self.robots[j][-1][2]
					for s in self.robot_shape:
						ss2 = [xx + s[0] * cos(qq) + s[2] * sin(qq), xx + s[1] * cos(qq) + s[3] * sin(qq), yy + s[2] * cos(qq) - s[0] * sin(qq), yy + s[3] * cos(qq) - s[1] * sin(qq)]
						v = self.how_far_seg2_from_seg1(ss,ss2)
						if v != None:
							d = ((ss[0] - v[0]) ** 2 + (ss[2] - v[1]) ** 2) ** 0.5
							if d < minv:
								minv = d
			ret.append(minv)
		return ret

	def thymio_sensor(self, i):
		ret = []
		x = robot[i][0]
		y = robot[i][1]
		q = -robot[i][2]
		for s in self.sensor_shape:
			ss = [x + s[0] * cos(q) + s[2] * sin(q), x + s[1] * cos(q) + s[3] * sin(q), y + s[2] * cos(q) - s[0] * sin(q), y + s[3] * cos(q) - s[1] * sin(q)]
			minv = 99999999
			for w in self.walls:
				v = self.how_far_seg2_from_seg1(ss,w)
				if v != None:
					d = ((ss[0] - v[0]) ** 2 + (ss[2] - v[1]) ** 2) ** 0.5
					if d < minv:
						minv = d
			for j in range(len(self.robots)):
				if j != i:
					xx = robot[j][0]
					yy = robot[j][1]
					qq = robot[j][2]
					for s in self.robot_shape:
						ss2 = [xx + s[0] * cos(qq) + s[2] * sin(qq), xx + s[1] * cos(qq) + s[3] * sin(qq), yy + s[2] * cos(qq) - s[0] * sin(qq), yy + s[3] * cos(qq) - s[1] * sin(qq)]
						v = self.how_far_seg2_from_seg1(ss,ss2)
						if v != None:
							d = ((ss[0] - v[0]) ** 2 + (ss[2] - v[1]) ** 2) ** 0.5
							if d < minv:
								minv = d
			ret.append(minv)
		return ret

	def step(self, robot, instruction):
		x = robot[-1][0]
		y = robot[-1][1]
		q = robot[-1][2]

		x += cos(q)*(self.R*instruction[0]/2 + self.R*instruction[1]/2) * self.simulation_timestep
		y += sin(q)*(self.R*instruction[0]/2 + self.R*instruction[1]/2) * self.simulation_timestep
		q += (self.R*instruction[1] - self.R*instruction[0])/(2*self.L) * self.simulation_timestep
		robot.append([x,y,q])

	def save(self):
		to_print_w = ""
		for w in self.walls:
		    for j in range(3):
		        to_print_w += str(w[j]) + ','
		    to_print_w += str(w[3]) + '\n'
		to_print_w += "--\n"
		for w in self.robot_shape:
			for j in range(3):
				to_print_w += str(w[j]) + ','
			to_print_w += str(w[3]) + '\n'
		for w in self.sensor_shape:
			for j in range(3):
				to_print_w += str(w[j]) + ','
			to_print_w += str(w[3]) + '\n'

		to_print_c = ""
		for i in range(len(self.robots[0])):
			for robot in self.robots:
				to_print_c += str(robot[i][0]) + ',' + str(robot[i][1]) + ',' + str(robot[i][2]) + '\n'
			to_print_c += ("---\n")

		file = open("walls.dat", "w")
		file.write(to_print_w)
		file.close()
		file = open("trajectory.dat", "w")
		file.write(to_print_c)
		file.close()

	def simulate(self, instructions, sec):
		for cnt in range(int(sec / self.simulation_timestep)):
			for i in range(len(instructions)):
				self.step(self.robots[i], instructions[i])

if __name__ == "__main__":
	import matplotlib.pyplot as plt
	h = 1
	w = 1
	walls = []
	simulator = kinematic_simulator(walls, [[[-0.4,-0.4,0]], [[0.4,0,3.14]]])
	a = simulator.lidar_sensor(0)
	for i in range(len(a)):
            if a[i] != 999999999:
                plt.scatter(cos(i/57.3)*a[i],sin(i/57.3)*a[i])
	plt.show()
	simulator.simulate([[3, 3], [3, 3]], 5)
	simulator.save()
