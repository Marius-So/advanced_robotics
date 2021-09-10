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

	def check_colour(self):
		while True:
			# Read the color.
			color = self.sensor_center.color()
			#ambient = self.sensor_b.ambient()
			#reflection = self.sensor_b.reflection()
			#rgb = self.sensor_b.rgb()
			# color_2 = self.sensor_a.color()
			# ambient_2 = self.sensor_a.ambient()
			# reflection_2 = self.sensor_a.reflection()
			# rgb_2 = self.sensor_a.rgb()
			#color_3 = self.sensor_center.color()
			#ambient_3 = self.sensor_c.ambient()
			#reflection_3 = self.sensor_c.reflection()
			#rgb_3 = self.sensor_c.rgb()
			# Print the measured color.
			print(color==Color.WHITE)
			print(type(color))
			#print(color==Color.White)
			# print(color_2, ambient_2, reflection_2, rgb_2)
			#print(color_3, ambient_3, reflection_3, rgb_3)
			wait(2000)

	def detect(self):
		while True:
			wait(2000) # this is our 'event loop'
			# Read the color.
			color = self.sensor_b.color()
			ambient = self.sensor_b.ambient()
			reflection = self.sensor_b.reflection()
			rgb = self.sensor_b.rgb()
			color_2 = self.sensor_a.color()
			ambient_2 = self.sensor_a.ambient()
			reflection_2 = self.sensor_a.reflection()
			rgb_2 = self.sensor_a.rgb()
			# Print the measured color.
			print(color, ambient, reflection, rgb)
			print(color_2, ambient_2, reflection_2, rgb_2)
			# Move the sensor around and see how
			# well you can detect colors.
			# Wait so we can read the value.


	def naviguate(self):
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

#def print_csv(data):
#	with open('ur file.csv','wb') as out:
#		csv_out=csv.writer(out)
#    	csv_out.writerow(['name','num'])
#    	for row in data:
#    	    csv_out.writerow(row)

if __name__ == "__main__":
	my_robot = moving_robot()
	my_robot.naviguate()
	#my_robot.gatherSensorInfo()
	#my_robot.check_colour()
	#my_robot.turn_by(43.5*grad)
	#my_robot.move_forward(850*advance)
	#my_robot.turn_by(180*grad)
	#my_robot.move_forward(700*advance)
	#my_robot.turn_by(180*grad)
	# spkr = Sound()
	# spkr.speak('Hello, I am Robot')
