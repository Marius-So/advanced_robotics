#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port, Stop, Color
from pybricks.robotics import DriveBase

#from pybricks.pupdevices import ColorDistanceSensor
from pybricks.tools import wait

import time
import math
import random


class moving_robot():
    def __init__(self):
        self.control = EV3Brick()
        self.motor_a = Motor(Port.A)
        self.motor_b = Motor(Port.B)
        self.base = DriveBase(self.motor_a, self.motor_b, wheel_diameter=55.5, axle_track=104)
        self.base.settings(250,250)#, turn_rate, turn_acceleration)

        self.sensor_left = ColorSensor(Port.S1)
        self.sensor_center = ColorSensor(Port.S2)
        self.sensor_right = ColorSensor(Port.S3)

    def turn_by(self, rad):
        self.base.turn(rad)

    def move_forward(self, distance):
        self.base.straight(-distance)

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

            # Move the sensor around and see how
            # well you can detect colors.

            # Wait so we can read the value.
            wait(2000)

    def navigate_maze(self):
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

    def move_straight(self):
        # logic to check for black again if we lose it
        rot = 1
        # basically move straight as long as sensor_center is black
        while True:
            while self.sensor_center.color() == Color.BLACK:
                self.base.drive(-200,0)
                wait(200)

                if self.sensor_left.color():# and random:
                    pass
                elif self.sensor_right.color():
                    pass

            while self.sensor_center.color() == Color.WHITE:
                self.base.drive(0, rot * 50)







if __name__ == "__main__":
    grad = 237/90
    advance = 1800/1060

    my_robot = moving_robot()
    #my_robot.check_colour()
    my_robot.move_straight()
    #my_robot.turn_by(43.5*grad)
    #my_robot.move_forward(850*advance)
    #my_robot.turn_by(180*grad)
    #my_robot.move_forward(700*advance)

    #my_robot.turn_by(180*grad)
    # spkr = Sound()
    # spkr.speak('Hello, I am Robot')

