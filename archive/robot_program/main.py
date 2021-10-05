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
import test.py

#grad = 237/90
grad = 267/90
advance = 1800/1060

class moving_robot():
	def __init__(self):
		self.control = EV3Brick()
		self.motor_a = Motor(Port.A)
		self.motor_b = Motor(Port.B)
		self.base = DriveBase(self.motor_a, self.motor_b, wheel_diameter=55.5, axle_track=104)
		self.base.settings(300,300)#, turn_rate, turn_acceleration)

		self.sensor_left = ColorSensor(Port.S1)
		self.sensor_center = ColorSensor(Port.S2)
		self.sensor_right = ColorSensor(Port.S3)

	def turn_by(self, rad):
		self.base.turn(rad)

	def move_forward(self, distance):
		self.base.straight(-distance*advance)

	#def turn(moove, previous):
	#	if moove == previous:
	#		return 0
	#	if moove == "up":
	#		if previous == "right":
	#			return 90
	#		if previous == "down":
	#			return 180
	#		return -90
	#	if moove == "right":
	#		if previous == "up":
	#			return -90
	#		if previous == "down":
	#			return 90
	#		return 180
	#	if moove == "down":
	#		if previous == "up":
	#			return 180
	#		if previous == "right":
	#			return 90
	#		return -90
	#	if moove == "left":
	#		if previous == "up":
	#			return 90
	#		if previous == "right":
	#			return 180
	#		return -90
#
	#def naviguate(self, mooves):
	#	previous = up
	#	for moove in mooves:
	#		if moove == can:
	#			done = False
    #            while done == False:
    #                if self.sensor_left.color() == BLACK:
    #                    if self.sensor_center.color() == BLACK
    #                        done = True
    #                    else:
    #                        while self.sensor_center.color() != BLACK:
    #                            self.base.drive(0, - 150)
    #                if self.sensor_right.color() == LEFT:
    #                    f self.sensor_center.color() == BLACK
    #                        done = True
    #                    else:
    #                        while self.sensor_center.color() != BLACK:
    #                            self.base.drive(0, 150)
    #                self.base.drive(10, 0)
	#			done = False
    #            while done == False:
    #                if self.sensor_left.color() == BLACK:
    #                    if self.sensor_center.color() == BLACK
    #                        done = True
    #                    else:
    #                        while self.sensor_center.color() != BLACK:
    #                            self.base.drive(0, - 150)
    #                if self.sensor_right.color() == LEFT:
    #                    f self.sensor_center.color() == BLACK
    #                        done = True
    #                    else:
    #                        while self.sensor_center.color() != BLACK:
    #                            self.base.drive(0, 150)
    #                self.base.drive(-10, 0)
	#		else:
	#			angle_to_rotate = turn(moove, previous)
	#			previous = moove
	#			self.turn_by(angle_to_rotate*grad)
	#			done = False
	#			while done == False:
	#				if self.sensor_left.color() == BLACK:
	#					if self.sensor_center.color() == BLACK
	#						done = True
	#					else:
	#						while self.sensor_center.color() != BLACK:
	#							self.base.drive(0, - 150)
	#				if self.sensor_right.color() == LEFT:
	#					f self.sensor_center.color() == BLACK
    #                        done = True
    #                    else:
    #                        while self.sensor_center.color() != BLACK:
    #                            self.base.drive(0, 150)
	#				self.base.drive(10, 0)
#
#
#
#
	#	rot = 1 #turn right by default if middle dont detect black
	#	straight = 100 # used to not check to often when to turn (to keep probability)
	#	while True:
	#		while self.sensor_center.color() == Color.BLACK: # while middle detect black go forward
	#			self.base.drive(-200,0)
	#			straight -= 1
	#			condition = random.random()
#
	#			if self.sensor_left.color() == Color.BLACK:# and random:
	#				rot = 1
	#				if straight <= 0 and condition < turn_cond:
	#					self.move_forward(130)
	#					self.turn_by(50*grad)
	#					rot = 1
	#				straight = 100
#
	#			if self.sensor_right.color() == Color.BLACK:
	#				rot = -1
	#				if straight <= 0 and condition > 1-turn_cond:
	#					self.move_forward(130)
	#					self.turn_by(-50*grad)
	#					rot = -1
	#				straight = 100
#
#
	#		while self.sensor_center.color() == Color.WHITE: #make robot middle on black again
	#			self.base.drive(0, rot * 150)
	#			if self.sensor_left.color() == Color.BLACK:
	#				rot = 1
	#			if self.sensor_right.color() == Color.BLACK:
	#				rot = -1
	#		wait(100)

	def gatherSensorInfo(self):
		my_data = []
		dist = 0
		for _ in range(50):
			my_data = my_data + [(dist, self.sensor_left.ambient(), self.sensor_left.reflection(), self.sensor_left.color())]
			self.move_forward(2)
			dist = dist + 2
			wait(200)
		for e in my_data: print(e)
		print_csv(my_data)


board = [   [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0]]

x = len(board[0]) - 1
y = len(board) - 1
target = [(3,3)]

if __name__ == "__main__":
	cans = [(2,3)]
	robot = [(1,3)]
	begining = State(cans,robot, -1)
	a = solve_sokoban(begining)
	b = recursive_print_traject(a, len(a) - 1, -1))
	my_robot.naviguate(b)
