#!/usr/bin/python3
import os
import math
from random import random
# initialize asebamedulla in background and wait 0.3s to let
# asebamedulla startup
os.system("(asebamedulla ser:name=Thymio-II &) && sleep 0.3")
import matplotlib.pyplot as plt
import numpy as np
from time import sleep

import dbus
import dbus.mainloop.glib
from threading import Thread

from adafruit_rplidar import RPLidar # distance sensor
from picamera import PiCamera # camera control

from kinetic_simulator import kinetic_simulator

# represent the world
# we want to use a grid -> robot is positioned in a cell

# global setups

class Thymio:
    def __init__(self, lidar_sensor = True, camera_sensor = True):
        # genereal control from linux over thymio
        self.aseba = self.setup()

        # setting up the lidar setup
        PORT_NAME = '/dev/ttyUSB0'
        self.lidar = RPLidar(None, PORT_NAME)

        self.scan_data = [0]*360
        self.exit_now = False

        # setting up the camera
        self.camera = PiCamera()
        self.camera.start_preview()
        sleep(2)

        self.camera.resolution = (320, 240)
        self.camera.framerate = 24
        self.sens_camera = None

        # initial belief -> zero, zero is center
        self.x = 0
        self.y = 0
        self.q = 0 # robot heading with respect to x-axis in radians

        W = 2.0  # width of arena
        H = 1.0  # height of arena
        self.walls = [[-W/2, W/2, -H/2, -H/2], [-W/2, W/2, H/2, H/2], [W/2, W/2, -H/2, H/2], [-W/2, -W/2, H/2, -H/2]]
        self.simulator = kinetic_simulator(self.walls)

        self.left_wheel_velocity =  random()   # robot left wheel velocity in radians/s
        self.right_wheel_velocity =  random()  # robot right wheel velocity in radians/s

    def turn_off(self):
            self.camera.stop_preview()
            self.stopAsebamedulla()

    def turn_around_center(self, speed): # speed in radiants per second
        if self.left_wheel_velocity != speed or self.right_wheel_velocity != -speed:
            self.left_wheel_velocity = speed
            self.right_wheel_velocity = -speed
            self.drive()

    def drive_adj(self, left_wheel, right_wheel):
        if left_wheel !=  self.left_wheel_velocity or right_wheel != self.right_wheel_velocity:
            self.drive()

    def drive(self):
        print("Left_wheel_speed: " + str(self.left_wheel_speed))
        print("Right_wheel_speed: " + str(self.right_wheel_speed))

        left_wheel = self.left_wheel_speed
        right_wheel = self.right_wheel_speed

        self.aseba.SendEventName("motor.target", [left_wheel, right_wheel])

    def stop(self):
        self.left_wheel_velocity =  0 # robot left wheel velocity in radians/s
        self.right_wheel_velocity =  0
        self.drive()

    def sens_dist(self):
        while True:
            # is an array with 5 entries for the 5 sensors
            self.prox_horizontal = self.aseba.GetVariable("thymio-II", "prox.horizontal")
            sleep(0.01)

    def sens_lidar(self):
        while True:
            for scan in self.lidar.iter_scans():
                if(self.exit_now):
                    return
                for (_, angle, distance) in scan:
                    self.scan_data[min([359, math.floor(angle)])] = distance
            sleep(0.1)

    def sens_camera(self):
        while True:
            self.sens_camera = np.empty((240, 320, 3), dtype=np.uint8)
            self.camera.capture(self.sens_camera , 'bgr')
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
        return asebaNetwork

    def stopAsebamedulla(self):
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
        return any(i > 3000 for i in self.prox_horizontal)


#------------------- loop ------------------------
    def simulation_step(self, time):
        self.x, self.y, self.q = self.simulator.simulate(self, self.x, self.y, self.q, self.right_wheel_velocity, self.left_wheel_velocity, time)

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
        loop_time = 0.1
        #simple controller - change direction of wheels every 10 seconds (100*robot_timestep) unless close to wall then turn on spot
        for cnt in range(1000):
            if self.wall_detection():
                print('detected a wall')
                speed = 0.4
                self.turn_around_center(speed=speed)
            else:
                if cnt%50==0:
                    left_wheel_velocity = random()
                    right_wheel_velocity = random()
                    self.drive_adj()
            self.simulation_step(loop_time)
            sleep(loop_time)

#----------------- loop end ---------------------

#------------------ Main -------------------------

def main():
    #robot_loop = 1/10
    #simu_loop = 1/100
    robot = Thymio()

    # starting robot sensors
    #lidar_thread = Thread(target=robot.sens_lidar)
    #lidar_thread.daemon = True
    #lidar_thread.start()

    thymio_thread = Thread(target=robot.sens_dist)
    thymio_thread.daemon = True
    thymio_thread.start()

    camera_thread = Thread(target=robot.sens_camera)
    camera_thread.daemon = True
    camera_thread.start()

    robot.simple_control()

    ##starting loop
    #while True:
    #    robot.simple_control()
    robot.turn_off()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Stopping robot")
        exit_now = True
        sleep(1)
        os.system("pkill -n asebamedulla")
        print("asebamodulla killed")
    except Exception as e:
        print("Stopping robot")
        print(e)
        exit_now = True
        sleep(1)
        os.system("pkill -n asebamedulla")
        print("asebamodulla killed")
