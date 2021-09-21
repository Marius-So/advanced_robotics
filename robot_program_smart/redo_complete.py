#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port, Stop, Color
from pybricks.robotics import DriveBase
from random import randrange
#from pybricks.pupdevices import ColorDistanceSensor
from sokoban_solver import *
from pybricks.tools import wait
import csv

import time
import math
import random

# we want to be able to give commands to turn left, right straight. additional to it always trying to get back to the black line

# maybe we build a robot -> always when middle sensor sees white rotate back on black,
# otherwise we have the options to move straight one width (or rather till detecting corners)
# when detecting make it aware of the options.


#grad = 237/90
grad = 257/90
advance = 1800/1060

class moving_robot():
	def __init__(self):
		self.control = EV3Brick()
		self.motor_a = Motor(Port.A)
		self.motor_b = Motor(Port.B)
		self.base = DriveBase(self.motor_a, self.motor_b, wheel_diameter=55.5, axle_track=104)

		self.speed = 200
		self.base.settings(self.speed, self.speed)#, turn_rate, turn_acceleration)
		self.direction = 0 # looks north 1 east, 2 south, 3 west
		self.horizontal = 0
		self.vertical = 0

		self.ver_dist = {-1: 760, 0: 760, 1:670, 2: 600, 3: 600}
		self.hor_dist = {-1: 250, 0: 250, 1:250, 2: 250, 3: 250}

		self.sensor_left = ColorSensor(Port.S1)
		self.sensor_center = ColorSensor(Port.S2)
		self.sensor_right = ColorSensor(Port.S3)

		self.rot = 1
		self.plan_executed = False
		# need to have a map, and to remember where it is and where it looks towards
		# self.map

	def edit_direction(self, update):
		self.direction = (self.direction + update + 4) % 4

	def update_pos(self):
		# we have 4 directions
		if self.direction % 2 == 0:
			if self.direction == 0:
				self.horizontal += 1
			else:
				self.horizontal -= 1
			# we move horizzontal
		else:
			if self.direction == 1:
				self.vertical -= 1
			else:
				self.vertical += 1
		pass

	def find_line(self):
		while self.sensor_center.color() != Color.BLACK:
			self.base.drive(0, self.rot * 150)
			if self.sensor_left.color() == Color.BLACK:
				self.rot = 1
			if self.sensor_right.color() == Color.BLACK:
				self.rot = -1
		self.base.reset()

	def turn_left(self):
		self.base.turn(90 * grad)
		self.edit_direction(-1)
		# need to think about editing rot

	def turn_right(self):
		self.base.turn(-90 * grad)
		self.edit_direction(1)

	def turn_around(self):
		self.base.turn(180 * grad)
		self.edit_direction(2)

	def rotate_to(self, direction):
		move = ((self.direction - direction) + 4) % 4
		if move == 3:
			# right
			self.turn_right()
		if move == 2:
			# 2 right
			self.turn_around()
		if move == 1:
			# left
			self.turn_left()

	#def move_forward(self, distance):
	#	self.base.straight(-distance*advance)

	def move_to_next_interception(self, dist=150):
		print('direction: ' + str(self.direction))
		if self.direction % 2 == 0:
			edit = 0
			if self.direction == 2: edit = 1
			dist = self.ver_dist.get(self.horizontal - edit)
		else:
			edit = 0
			if self.direction == 1: edit = 1
			dist = self.hor_dist.get(self.vertical - edit)

		print('dist to go: ' + str(dist))
		while dist + self.base.distance() > 0:
			self.base.drive(-200,0)
			while self.sensor_center.color() == Color.BLACK and (dist + self.base.distance()) >0:
				if self.sensor_left.color() == Color.BLACK:
					self.rot = -1
				if self.sensor_right.color() == Color.BLACK:
					self.rot = 1
			dist = dist + self.base.distance()
			self.find_line()
		self.update_pos()

	def push_can(self):
		self.move_to_next_interception()
		deduct = 100
		if self.direction % 2 == 0:
			dist = self.hor_dist.get(self.horizontal) - 100
			back_dist = dist
		else:
			dist = self.ver_dist.get(self.vertical) - 100
			back_dist = dist

		while dist + self.base.distance() > 0:
			self.base.drive(-200,0)
			while self.sensor_center.color() == Color.BLACK and (dist + self.base.distance()) >0:
				if self.sensor_left.color() == Color.BLACK:
					self.rot = -1
				if self.sensor_right.color() == Color.BLACK:
					self.rot = 1

			dist = dist + self.base.distance()
			self.find_line()

		while back_dist - self.base.distance() > 0:
			self.base.drive(200,0)
			while self.sensor_center.color() == Color.BLACK and (back_dist - self.base.distance()) >0:
				if self.sensor_left.color() == Color.BLACK:
					self.rot = -1
				if self.sensor_right.color() == Color.BLACK:
					self.rot = 1

			dist = back_dist - self.base.distance()
			self.find_line()

	def follow_plan(self, plan):
		if plan:
			next_move = plan[0] # move straight between any two moves
			if next_move == 'up':
				self.rotate_to(0)
				self.move_to_next_interception()
				time.sleep(3)
				print('done up')
			if next_move == 'right':
				self.rotate_to(1)
				self.move_to_next_interception()
				time.sleep(3)
				print('done left')
			if next_move == 'down':
				self.rotate_to(2)
				self.move_to_next_interception()
				time.sleep(3)
				print('done down')
			if next_move == 'left':
				self.rotate_to(3)
				self.move_to_next_interception()
				time.sleep(3)
				print('done right')
			if next_move == 'can':
				self.push_can()
				time.sleep(3)
				print('done can')#
			self.follow_plan(plan[1:])


if __name__ == "__main__":
	my_robot = moving_robot()
	my_robot.direction = 2
	my_robot.horizontal = 3
	my_robot.vertical = 3
	plan = ['right', 'down', 'right']#, 'left']# , 'can', 'up', 'up', 'right', 'right', 'down', 'left', 'can', 'left']
	my_robot.follow_plan(plan)

