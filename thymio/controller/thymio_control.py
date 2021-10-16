#!/usr/bin/python3
import os
import math
from random import random
# initialize asebamedulla in background and wait 0.3s to let
# asebamedulla startup
os.system("(asebamedulla ser:name=Thymio-II &) && sleep 0.3")
# import matplotlib.pyplot as plt
import numpy as np
from time import sleep

import dbus
import dbus.mainloop.glib
from threading import Thread

from adafruit_rplidar import RPLidar # distance sensor
from picamera import PiCamera # camera control

from kinetic_simulator import kinetic_simulator
import traceback
import sys

import cv2

# represent the world
# we want to use a grid -> robot is positioned in a cell

# global setups

LIDAR = True
CAMERA = True

class Thymio:
    def __init__(self, lidar_sensor = True, camera_sensor = True):
        # genereal control from linux over thymio
        self.setup()

        # setting up the lidar setup
        if LIDAR:
            PORT_NAME = '/dev/ttyUSB0'
            self.lidar = RPLidar(None, PORT_NAME)
            self.scan_data = [0]*360
            self.exit_now = False

        # setting up the camera
        if CAMERA:
            self.camera = PiCamera()
            self.camera.start_preview()
            sleep(2)

            self.camera.resolution = (320, 240)
            self.camera.framerate = 24
            self.picture = np.empty((240, 320, 3), dtype=np.uint8)

        # distance sensors
        self.prox_horizontal = np.zeros(7)
        self.dist_sens = True

        # initial belief -> zero, zero is center
        self.x = 0
        self.y = 0
        self.q = 0 # robot heading with respect to x-axis in radians

        W = 2.0  # width of arena
        H = 1.0  # height of arena
        self.walls = [[-W/2, W/2, -H/2, -H/2], [-W/2, W/2, H/2, H/2], [W/2, W/2, -H/2, H/2], [-W/2, -W/2, H/2, -H/2]]
        self.simulator = kinetic_simulator(self.walls)

        self.left_wheel_velocity =  round(random()*20)   # robot left wheel velocity in radians/s
        self.right_wheel_velocity =  round(random()*20)  # robot right wheel velocity in radians/s

    def turn_off(self):
            if CAMERA:
                self.camera.stop_preview()
            self.dist_sens = False

            self.stop()
            self.stopAsebamedulla()

    def turn_around_center(self, speed): # speed in radiants per second
        #if self.left_wheel_velocity != speed or self.right_wheel_velocity != -speed:
        self.left_wheel_velocity = speed
        self.right_wheel_velocity = -speed
        self.drive()

    def drive_adj(self, left_wheel, right_wheel):
        #if left_wheel !=  self.left_wheel_velocity or right_wheel != self.right_wheel_velocity:
        self.left_wheel_velocity = round(left_wheel)
        self.right_wheel_velocity = round(right_wheel)
        self.drive()

    def drive(self):
        left_wheel = self.left_wheel_velocity
        right_wheel = self.right_wheel_velocity
        self.aseba.SendEventName("motor.target", [left_wheel, right_wheel])

    def stop(self):
        self.left_wheel_velocity =  0 # robot left wheel velocity in radians/s
        self.right_wheel_velocity =  0
        self.drive()

    def sens_dist(self):
        while True and self.dist_sens:
            # is an array with 5 entries for the 5 sensors
            self.prox_horizontal = np.array(self.aseba.GetVariable("thymio-II", "prox.horizontal"))
            sleep(0.1)

    def sens_lidar(self):
        while True and LIDAR:
            for scan in self.lidar.iter_scans():
                if(self.exit_now):
                    return
                for (_, angle, distance) in scan:
                    self.scan_data[min([359, math.floor(angle)])] = distance
            sleep(0.1)

    def sens_camera(self):
        while True and CAMERA:
            self.camera.capture(self.picture , 'bgr')
            print(self.scan_data)
            sleep(1)


############## Bus and aseba setup ######################################
    def setup(self):
        print("Setting up")
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        bus = dbus.SessionBus()
        asebaNetworkObject = bus.get_object('ch.epfl.mobots.Aseba', '/')

        asebaNetwork = dbus.Interface(
            asebaNetworkObject, dbus_interface='ch.epfl.mobots.AsebaNetwork'
        )
        # load the file which is run on the thymio
        asebaNetwork.LoadScripts(
            'thympi.aesl', reply_handler=self.dbusError, error_handler=self.dbusError
        )

        # scanning_thread = Process(target=robot.drive, args=(200,200,))
        # asebaNetwork.SendEventName('motor.target',[10, 20])
        self.aseba = asebaNetwork

    def stopAsebamedulla(self):
        self.stop()
        os.system("pkill -n asebamedulla")

    def dbusReply(self):
        # dbus replys can be handled here.
        # Currently ignoring
        pass

    def dbusError(self, e):
        # dbus errors can be handled here.
        # Currently only the error is logged. Maybe interrupt the mainloop here
        print("dbus error: %s" % str(e))


#------------------- Main ------------------------

#-------------- Obstacle avoidance ---------------
# maybe this is possible to check all the time with a slave process but idk
    def wall_detection(self):
        for i in [0,2,4]:
            if self.prox_horizontal[i] > 3000:
                return True
        return False
        #return any(i > 3000 for i in self.prox_horizontal)


#------------------- loop ------------------------
    def simulation_step(self, time):
        coo = self.simulator.simulate(self.x, self.y, self.q, self.right_wheel_velocity, self.left_wheel_velocity, time)[-1]
        if len(coo) == 3:
            self.x, self.y, self.q

    def loop(self):
        # get next move / plan moves


        # move / execute

        # simulate new positon

        # sensing

        # correction

        # map update

        # obstackle avoidance -> input: to get next move

        # robot.drive(200, 200)
        print("nothing to do.. zzz")
        sleep(5)
        #robot.stop()

    def simple_control(self):
        left_wheel_velocity = round(random() * 20)
        right_wheel_velocity = round(random() * 20)
        self.drive_adj(left_wheel_velocity, right_wheel_velocity)
        self.drive()
        loop_time = 0.1
        #simple controller - change direction of wheels every 10 seconds (100*robot_timestep) unless close to wall then turn on spot
        for cnt in range(200):
            while self.wall_detection():
                speed = 30
                self.turn_around_center(speed=speed)
            else:
                if cnt%50==0:
                    left_wheel_velocity = random() * 20
                    right_wheel_velocity = random() * 20
                    self.drive_adj(left_wheel_velocity, right_wheel_velocity)
            self.simulation_step(loop_time)
            sleep(loop_time)

#----------------- loop end ---------------------

#------------------ Main -------------------------

def main():
    robot = None
    try:
            #robot_loop = 1/10
        #simu_loop = 1/100
        robot = Thymio()

        # starting robot sensors
        if LIDAR:
            lidar_thread = Thread(target=robot.sens_lidar)
            lidar_thread.daemon = True
            lidar_thread.start()

        thymio_thread = Thread(target=robot.sens_dist)
        thymio_thread.daemon = True
        thymio_thread.start()

        if CAMERA:
            print('camera is on')
            camera_thread = Thread(target=robot.sens_camera)
            camera_thread.daemon = True
            camera_thread.start()

        robot.simple_control()
        robot.turn_off()

    except KeyboardInterrupt:
        print("Stopping robot")
        if robot is not None:
            robot.turn_off()
        exit_now = True
        sleep(1)
        os.system("pkill -n asebamedulla")
        print("asebamodulla killed")
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        if robot is not None:
            robot.turn_off()
        print("Stopping robot")
        print(e)
        exit_now = True
        sleep(1)
        os.system("pkill -n asebamedulla")
        print("asebamodulla killed")

if __name__ == '__main__':
    main()
