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

		self.sensor_left = ColorSensor(Port.S1)
		self.sensor_center = ColorSensor(Port.S2)
		self.sensor_right = ColorSensor(Port.S3)

		self.rot = 1
		self.plan_executed = False
		# need to have a map, and to remember where it is and where it looks towards
		# self.map

	def edit_direction(self, update):
		self.direction += (self.direction + update) % 4

	def find_line(self):
		while self.sensor_center.color() != Color.BLACK:
			self.base.drive(0, self.rot * 150)
			if self.sensor_left.color() == Color.BLACK:
				self.rot = 1
			if self.sensor_right.color() == Color.BLACK:
				self.rot = -1

	def turn_left(self, rad):
		self.base.turn(90 * grad)
		self.edit_direction(-1)
		# need to think about editing rot

	def turn_right(self, rad):
		self.base.turn(-90 * grad)
		self.edit_direction(1)

	def turn_around(self, rad):
		self.base.turn(190 * grad)
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

	def move_forward(self, distance):
		self.base.straight(-distance*advance)

	def move_to_next_interception(self, dist=150):
		if self.direction % 2 == 0:
			dist = 150
		else:
			dist = 200

		while dist > 0:
			while self.sensor_center.color() == Color.BLACK and dist>0:
				dist = dist - 1
				self.base.drive(-200,0)
				wait(3)
				print(dist)
				if self.sensor_left.color() == Color.BLACK:
					self.rot = -1
				if self.sensor_right.color() == Color.BLACK:
					self.rot = 1
			self.find_line()
		print('done')


	def follow_plan(self, plan):
		while not self.plan_executed:
			next_move = plan[0] # move straight between any two moves
			processing = True
			while processing:
				while self.sensor_center.color() == Color.BLACK:
					# move on with plan

					pass
				# when
				self.find_line()

if __name__ == "__main__":
	my_robot = moving_robot()
	plan = [0, 2,2,1,1,0]
	#[0,1,2,0] # 0 left, 1 straigt, 2 right, 3 would be turn 180 degree
	my_robot.move_to_next_interception()
	my_robot.turn_right(90)
	my_robot.move_to_next_interception()
	my_robot.turn_left(90)
	my_robot.move_to_next_interception()
	my_robot.turn_around(90)
