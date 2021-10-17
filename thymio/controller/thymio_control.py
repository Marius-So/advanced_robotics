#!/usr/bin/python3
import os
import math
from random import random
import time

import numpy as np
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
from picamera.array import PiRGBArray

from comp_vision import robot_vision

from kinematic_simulator import kinematic_simulator
import traceback
import sys

import cv2
from matplotlib import pyplot as plt

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
            sleep(0.1)

            self.camera.resolution = (320, 240)
            self.camera.framerate = 24
            self.picture = np.empty((240, 320, 3), dtype=np.uint8)

            self.robot_vision = robot_vision()

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
        self.simulator = kinematic_simulator(self.walls)

        self.left_wheel_velocity =  round(random()*20)   # robot left wheel velocity in angle/s
        self.right_wheel_velocity =  round(random()*20)  # robot right wheel velocity in angle/s

        self.loop_time = 0

    def turn_off(self):
            if CAMERA:
                self.camera.stop_preview()
            self.dist_sens = False

            self.stop()
            self.lidar.stop()
            self.stopAsebamedulla()

    def turn_around_center(self, speed): # speed in angle per second
        if self.left_wheel_velocity != speed or self.right_wheel_velocity != -speed:
            self.left_wheel_velocity = speed
            self.right_wheel_velocity = -speed
            self.drive()

    def rotate_by(self, speed): # speed in angle per second
        if self.left_wheel_velocity != speed or self.right_wheel_velocity != -speed:
            self.left_wheel_velocity = speed
            self.right_wheel_velocity = -speed
            self.drive()

    def rotate_by_degree(self, degree): # speed in angle per second
        if degree < 0:
            speed = 30
        else:
            speed = - 30

        time = (degree * 0.1 / (speed * 0.02 * 2))

        #if self.left_wheel_velocity != speed or self.right_wheel_velocity != -speed:
        self.left_wheel_velocity = speed
        self.right_wheel_velocity = -speed
        self.drive()

        sleep(abs(time))
        self.stop()



    def drive_adj(self, left_wheel, right_wheel):
        left_wheel = round(left_wheel)
        right_wheel = round(right_wheel)
        if left_wheel !=  self.left_wheel_velocity or right_wheel != self.right_wheel_velocity:
            self.left_wheel_velocity = left_wheel
            self.right_wheel_velocity = right_wheel
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
            sleep(0.01)

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
            # display the image on screen and wait for a keypress~
            sleep(1)

    def find_correct_rotation(self):
        # checks the lidar scan and gives back the four corners
        size = len(self.scan_data) - 1
        data = self.scan_data
        minima = []
        for idx in range(size+2):
            if data[(idx - 1) % size] > data[(idx) % size] <  data[(idx+1) % size] and data[(idx - 2) % size] > data[(idx) % size] <  data[(idx+2) % size]:
                minima.append(idx % size)
        return minima

    def align_robot(self):
        start_time = time.time()
        while True:
            minima = self.find_correct_rotation()
            if len(minima)==0:
                sleep(0.1)
                continue
            # basically rotate until one of the minima is close to 0
            #assert len(minima) == 4

            dist = [i -179 for i in minima]

            #req_rot = min(dist)
            #print(req_rot)
            req_rot = self.scan_data.index(min(self.scan_data))
            value = min(self.scan_data)
            if value == 0:
                continue
            print(self.scan_data)


            print(f'thsi is the index i go to {req_rot}')


            if abs(req_rot) > 4:
                if req_rot > 179:
                    #print(f'i will rotate to {-(req_rot-179)}')
                    self.rotate_by_degree(-(req_rot-360))
                #    return
                #else:
                #    print(f'i will rotate to {req_rot}')
                else:
                    self.rotate_by_degree(-req_rot)
                return
                #    return

            else:
                self.stop()
                break
            sleep(0.1)
            if time.time() - start_time > 20:
                return



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
        if LIDAR and min(self.scan_data[150:210]) < 150:
            return True

        for i in [0,2,4]:
            if self.prox_horizontal[i] > 500:
                return True
        return False
        #return any(i > 3000 for i in self.prox_horizontal)

#------------------- loop ------------------------
    def simulation_step(self):
        r_rad_speed = math.pi*self.right_wheel_velocity / 180
        l_rad_speed = math.pi*self.left_wheel_velocity /180
        coo = self.simulator.simulate(self.x, self.y, self.q, r_rad_speed, l_rad_speed, self.loop_time)[-1]
        if len(coo) == 3:
            self.x, self.y, self.q = coo

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
        self.loop_time = 0.1
        self.speed_correction = 1.15
        left_wheel_velocity = 0 * 90 * self.speed_correction
        right_wheel_velocity = 0 * 90* self.speed_correction
        self.drive_adj(left_wheel_velocity, right_wheel_velocity)
        sleep(1)

        for cnt in range(100):
            if cnt % 100==0:
                self.align_robot()
                print('i am aligned')
                print('i see wall')

                if CAMERA:
                    side = self.robot_vision.get_side(self.picture)
                    print(f'side is {side}')
                #break


            sleep(self.loop_time)



        #self.speed_correction = 1.15
        #start_time = time.time()
        #left_wheel_velocity = 0* 90 * self.speed_correction
        #right_wheel_velocity = 0* 90* self.speed_correction
        #self.drive_adj(left_wheel_velocity, right_wheel_velocity)
        #self.drive()
        #self.loop_time = 0.1
        #self.detected = False
        ##simple controller - change direction of wheels every 10 seconds (100*robot_timestep) unless close to wall then turn on spot
        #for cnt in range(800):
        #    if False and self.wall_detection():
        #        speed = 70
        #        self.turn_around_center(speed=speed)
        #        self.detected = True
        #    else:
        #        if False: #self.detected or cnt%100==0:
        #            self.detected = False
        #            left_wheel_velocity = random() * 200
        #            right_wheel_velocity = random() * 200
        #            self.drive_adj(left_wheel_velocity, right_wheel_velocity)
#
        #    self.simulation_step()
        #    if cnt%2==0:
        #        #print(f'x: {self.x}, y: {self.y}, rot : {(self.q%(2*math.pi)) *180/math.pi}')
        #        print(self.scan_data[179])
#
        #    sleep(self.loop_time)
#
        #print(f'time {time.time()- start_time}')
#
        #self.stop()
        #print(f'x: {self.x}, y: {self.y}, rot : {(self.q%(2*math.pi)) *180/math.pi}')
        #print(self.scan_data)

#----------------- loop end ---------------------

#------------------ Main -------------------------

def main():
    robot = None
    try:
        #robot.simu_time = 1/100
        robot = Thymio()
        robot.loop_time = 1/10

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

        # simulation = Thread(target=robot.simulation_step)
        # simulation.daemon = True
        # simulation.start()

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
