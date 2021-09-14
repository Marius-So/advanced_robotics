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
grad = 267/90
advance = 1800/1060

class moving_robot():
	def __init__(self):
		self.control = EV3Brick()
		self.motor_a = Motor(Port.A)
		self.motor_b = Motor(Port.B)
		self.base = DriveBase(self.motor_a, self.motor_b, wheel_diameter=55.5, axle_track=104)
		self.base.settings(200,200)#, turn_rate, turn_acceleration)

		self.sensor_left = ColorSensor(Port.S1)
		self.sensor_center = ColorSensor(Port.S2)
		self.sensor_right = ColorSensor(Port.S3)

		self.rot = 1
		# need to have a map, and to remember where it is and where it looks towards

	def turn_by(self, rad):
		self.base.turn(rad)

	def move_forward(self, distance):
		self.base.straight(-distance*advance)

	def turn_left(self):
		pass

	def turn_right(self):
		pass

	def move_straight(self):
		self.base.drive(-200,0)
		straight -= 1

	def plan_route(self):
		#gives_list_of_turns.
		pass

	def follow_route(self, plan):
		if plan[0] != 1:
			force_turn = True
			straight = -1
		else:
			force_turn = False
			straight = 100
			plan = plan[1:]

		while plan:
			next_action = plan[0]
			while self.sensor_center.color() == Color.BLACK:
				self.base.drive(-200,0)
				straight -= 1

				if self.sensor_left.color() == Color.BLACK or force_turn:
					self.rot = 1
					if straight < 0 and next_action == 0:
						self.move_forward(130)
						self.turn_by(50*grad)
						plan = plan[1:]
						force_turn = False
						print('i go left')

					if straight < 0 and next_action == 1:
						plan = plan[1:]
						straight = 100
						print('i go straight')

				if self.sensor_right.color() == Color.BLACK or force_turn:
					self.rot = -1
					if straight < 0 and next_action == 2:
						self.move_forward(130)
						self.turn_by(-50*grad)
						plan = plan[1:]
						force_turn = False
						print('i go right')

					if straight < 0 and next_action == 1:
						plan = plan[1:]
						straight = 100
						print('i go straight')

				wait(100)
				# follow the plan

			while self.sensor_center.color() == Color.WHITE: #make robot middle on black again
					self.base.drive(0, self.rot * 150)
					if self.sensor_left.color() == Color.BLACK:
						self.rot = 1
					if self.sensor_right.color() == Color.BLACK:
						self.rot = -1
					wait(100)

	def take_decision(self, left, right, straight, plan):
		pass


	def navigate(self):
		turn_cond = 0.333
		rot = 1 #turn right by default if middle dont detect black
	 	straight = 100 # used to not check to often when to turn (to keep probability)
	 	while True:
			while self.sensor_center.color() == Color.BLACK: # while middle detect black go forward
				self.base.drive(-200,0)
				straight -= 1
				condition = random.random()

				if self.sensor_left.color() == Color.BLACK:# and random:
					rot = 1
					if straight <= 0 and condition < turn_cond:
						self.move_forward(130)
						self.turn_by(50*grad)
						rot = 1
					straight = 100

				if self.sensor_right.color() == Color.BLACK:
					rot = -1
					if straight <= 0 and condition > 1-turn_cond:
						self.move_forward(130)
						self.turn_by(-50*grad)
						rot = -1
					straight = 100


			while self.sensor_center.color() == Color.WHITE: #make robot middle on black again
				self.base.drive(0, rot * 150)
				if self.sensor_left.color() == Color.BLACK:
					rot = 1
				if self.sensor_right.color() == Color.BLACK:
					rot = -1
			wait(100)

	def gatherSensorInfo(self):
		my_data = []
		dist = 0
		for _ in range(50):
			my_data = my_data + [(dist, self.sensor_left.ambient(), self.sensor_left.reflection(), self.sensor_left.color())]
			self.move_forward(2)
			dist = dist + 2
			wait(200)
		for e in my_data: print(e)
		#print_csv(my_data)


if __name__ == "__main__":
	my_robot = moving_robot()
	plan = [0, 2,2,1,1,0]
	#[0,1,2,0] # 0 left, 1 straigt, 2 right, 3 would be turn 180 degree
	my_robot.follow_route(plan)
