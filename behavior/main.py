#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port, Stop, Color
from pybricks.robotics import DriveBase
from random import randrange
#from pybricks.pupdevices import ColorDistanceSensor
from pybricks.tools import wait
import csv

import time
import math
import random
from sokobanSolver import State, SokobanSolver

#grad = 237/90
grad = 267/90
advance = 1800/1060

class moving_robot():
	def __init__(self):
		self.control = EV3Brick()
		self.motor_a = Motor(Port.A)
		self.motor_b = Motor(Port.B)
		self.base = DriveBase(self.motor_a, self.motor_b, wheel_diameter=55.5, axle_track=104)

		self.sensor_left = ColorSensor(Port.S1)
		self.sensor_center = ColorSensor(Port.S2)
		self.sensor_right = ColorSensor(Port.S3)

		self.rot=1
		self.speed = 150 # faster when not moving can

		self.base.settings(self.speed, self.speed)#, turn_rate, turn_acceleration)

	def turn_by(self, rad):
		self.base.turn(rad)

	def move_forward(self, distance):
		self.base.straight(-distance*advance)

	def turn(self, moove, previous):
		if moove == previous:
			return 0
		if moove == "up":
			if previous == "right":
				return 90
			if previous == "down":
				return 180
			return -90
		if moove == "right":
			if previous == "up":
				return -90
			if previous == "down":
				return 90
			return 180
		if moove == "down":
			if previous == "up":
				return 180
			if previous == "right":
				return -90
			return 90

		if moove == "left":
			if previous == "up":
				return 90
			if previous == "right":
				return 180
			return -90



	def follow_line(self, backward):
		#self.base.straight(50*backward)
		while True:
			#print('left: ' + str(self.sensor_left.color()))
			#print('right: ' + str(self.sensor_right.color()))
			while self.sensor_center.color() == Color.BLACK:
				if self.sensor_left.color() == Color.BLACK:
					return

				if self.sensor_right.color() == Color.BLACK:
					return

				self.base.drive(backward * self.speed, 0)
				#print('after')
			self.find_line()

	def naviguate(self, mooves, init_direction):
		previous = init_direction
		for moove in range(len(mooves)):
			if mooves[moove] == 'can':
				if mooves[moove + 2] == 'can' and mooves[moove + 1] == mooves[moove - 1]:
					self.follow_line(-1)
				else:
					self.follow_line(-1)
					self.base.straight(270)
					self.follow_line(1)
					self.base.straight(-200)

			else:
				angle_to_rotate = self.turn(mooves[moove], previous)
				print(angle_to_rotate)
				previous = mooves[moove]
				self.turn_by(angle_to_rotate*grad)
				self.follow_line(-1)
				self.base.straight(-270)

	def find_line(self):
		while self.sensor_center.color() != Color.BLACK:
			self.base.drive(0, self.rot * self.speed)
			if self.sensor_left.color() == Color.BLACK:
				self.rot = 1
			if self.sensor_right.color() == Color.BLACK:
				self.rot = -1

if __name__ == "__main__":
	##### initialising robot
	my_robot = moving_robot()

	# initialisiing the maze
	cans = [(1,2)]
	robot = (3,0)
	target = [(3,3)]
	board = [[0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0]]

	# solving the maze
	init_state = State(cans,robot, -1)
	solver = SokobanSolver(board, target, robot, cans)
	solution = solver.solve_sokoban(init_state)
	plan = solver.recursive_print_traject(solution, len(solution) - 1, -1)[:-1]
	print(plan)

	# run the plan
	my_robot.naviguate(plan, 'up')
