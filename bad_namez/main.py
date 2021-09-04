#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port, Stop
#from pybricks.ev3dev2.sound import Sound
from pybricks.robotics import DriveBase

import time
import math


class moving_robot():
    def __init__(self):
        self.x = 0 # i guess measured in cm
        self.y = 0
        self.orientation = 0 # we go with radiants lets say 0 means -> our nose aims towards y+
        self.control = EV3Brick()
        self.motor_a = Motor(Port.A)
        self.motor_b = Motor(Port.B)
        self.base = DriveBase(self.motor_a, self.motor_b, wheel_diameter=55.5, axle_track=104)

        self.sensor = None

    def move_to_point(self, x,y):
        # here we need to calculate how we need to move in order to position to (x,y)

        # calibration params
        rot_cal = 1
        move_cal = 1

        delta_x = x - self.x
        delta_y = y - self.y

        need_direction = math.atan2(delta_y, delta_x)


        #if (|need_direction - self.orientation| > 2*pi):
        #    rotation = None
        #else:
        #    rotation = None

        self.turn_by()


        distance = math.sqrt(delta_x**2 + delta_y**2)
        self.move_forward(distance)

        # update positioning and rotation
        self.oritentation = need_direction
        self.x = x
        self.y = y

    #def play_happy_tune(self):
    #    spkr = Sound()
    #    spkr.speak('Hello, I am Robot')
    #    spkr.play_file('R2D2a.wav',20)

    def turn_by(self, rad):
        # speed deg/s
        speed = 500
        # time ms
        time = 1000 * rad

        if rad < 0:
            speed = speed * -1

        self.base.turn(rad)
        #self.motor_a.run_time(speed, time,then=Stop.BRAKE)
        #self.motor_b.run_time(-speed, time,then=Stop.BRAKE)

    def move_forward(self, distance):
        #speed = 1000
        #self.motor_a.run_time(speed, time,then=Stop.BRAKE)
        #self.motor_b.run_time(speed, time,then=Stop.BRAKE)
        self.base.straight(-distance)


#ev3 = EV3Brick()
# Initialize a motor at port B.
#test_motor = Motor(Port.B)
# Play a sound.
#ev3.speaker.beep()
# Run the motor up to 500 degrees per second. To a target angle of 90 degrees.
# test_motor.run_target(50, 90)
# Play another beep sound.
# ev3.speaker.beep(1000, 50)

# test_motor.run(1000)

# time.sleep(3)
# ev3.speaker.beep()
# test_motor.brake()
if __name__ == "__main__":
    # straight
    # left
    # short dist
    # right long dist

    grad = 255/90
    advance = 1800/1060

    my_robot = moving_robot()
    my_robot.move_forward(700*advance)
    my_robot.turn_by(90*grad)

    my_robot.move_forward(700*advance)

