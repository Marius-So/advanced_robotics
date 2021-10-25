#!/usr/bin/python3
# standard libraries
import os
import math
from random import random
import time
from time import sleep, time
import traceback
import sys
import numpy as np

# thymio specifics
import dbus
import dbus.mainloop.glib
from adafruit_rplidar import RPLidar # distance sensor
from picamera import PiCamera # camera control

# our own written modules, present in the same folder for import
from threading import Thread
from comp_vision import robot_vision
from kinematic_simulator import kinematic_simulator
from Location import Location


# global setups
# initialize asebamedulla in background and wait 0.3s to let
# asebamedulla startup
os.system("(asebamedulla ser:name=Thymio-II &) && sleep 0.3")

# bools to completely disable sensors for debugging
LIDAR = True
CAMERA = True

# the robot class
class Thymio:
    def __init__(self, lidar_sensor = True, camera_sensor = True):
        # genereal control from linux over thymio
        self.setup()

        # setting up the lidar setup
        if LIDAR:
            PORT_NAME = '/dev/ttyUSB0'
            self.lidar = RPLidar(None, PORT_NAME)
            self.scan_data = [0]*360

        # setting up the camera
        if CAMERA:
            self.camera = PiCamera()
            self.camera.start_preview()
            sleep(0.1)

            self.camera.resolution = (320, 240)
            self.camera.framerate = 24
            self.picture = np.empty((240, 320, 3), dtype=np.uint8) # a bit wired that the dimensions are swapped...
            self.robot_vision = robot_vision()

        # distance sensors
        self.prox_horizontal = np.zeros(7)
        self.distance_sensor_on = True

        # ground sensors
        self.prox_vertical = np.zeros(2)
        self.vertical_sensor_on = True

        # initial belief of positioning -> zero, zero is center
        self.x = 0
        self.y = 0
        self.q = 0 # robot heading with respect to x-axis in radians

        # TODO: measure these
        W = 2.0  # width of arena
        H = 1.0  # height of arena
        self.walls = [[-W/2, W/2, -H/2, -H/2], [-W/2, W/2, H/2, H/2], [W/2, W/2, -H/2, H/2], [-W/2, -W/2, H/2, -H/2]]
        self.simulator = kinematic_simulator(self.walls)

        self.left_wheel_velocity =  0   # robot left wheel velocity in angle/s
        self.right_wheel_velocity =  0  # robot right wheel velocity in angle/s

        self.loop_time = 0.1 # this maybe needs to fixed at some point seconds
        self.time_measure = time.time()
        self.loc = Location(H,W,(0,0))

    def turn_off(self):
            if CAMERA:
                self.camera.stop_preview()
            self.distance_sensor_on = False

            self.stop_driving() # stop the robot from moving
            self.lidar.stop() # stop recording the lidar
            self.stopAsebamedulla() # disconnect from the thymio

    def turn_around_center(self, speed): # speed in angle per second
        # positive speed means clockwise, neg speed means turning anticlockwise
        if self.left_wheel_velocity != speed or self.right_wheel_velocity != -speed:
            self.left_wheel_velocity = speed
            self.right_wheel_velocity = -speed
            self.drive()

    def rotate_by_degree(self, degree, rot_speed = 30): # speed in angle per second
        if degree < 0:
            speed = abs(rot_speed)
        else:
            speed = - abs(rot_speed)

        # estimated time of rotating to rotate by specified angle
        rot_time = (degree * 0.1 / (speed * 0.02 * 2)) # hard coded wheel

        self.left_wheel_velocity = speed
        self.right_wheel_velocity = -speed
        self.drive()

        sleep(abs(rot_time)) # simple but working...
        self.stop_drivingstop()

    def drive_adj(self, left_wheel, right_wheel):
        # TODO: check if this method is needed or better than the normal one
        # TODO: can we read the wheel speed from the thymio?
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

    def play_sound(self):
        sound_name = 'R2D2a.wav'
        self.aseba.SendEventName("sound.play(1)")

    def stop_driving(self):
        self.left_wheel_velocity =  0
        self.right_wheel_velocity =  0
        self.drive()

    def distance_sensing(self):
        while True and self.distance_sensor_on:
            # is an array with 5 entries for the 5 sensors
            self.prox_horizontal = np.array(self.aseba.GetVariable("thymio-II", "prox.horizontal"))
            # TODO: I think this can be done better with scheduling the thread executions
            sleep(0.1)

    def ground_sensing(self):
        while True and self.vertical_sensor_on:
            # is an array with 5 entries for the 5 sensors
            self.prox_vertical = np.array(self.aseba.GetVariable("thymio-II", "prox.ground.reflected"))
            # TODO: I think this can be done better with scheduling the thread executions
            sleep(0.1)

    def lidar_sensing(self):
        while True and LIDAR:
            for scan in self.lidar.iter_scans():

                for (_, angle, distance) in scan:
                    self.scan_data[min([359, math.floor(angle)])] = distance
            # TODO: I think this can be done better with scheduling the thread executions
            sleep(0.1)

    def camera_sensing(self):
        while True and CAMERA:
            self.camera.capture(self.picture , 'bgr')
            # TODO: I think this can be done better with scheduling the thread executions
            # also we can take more frames
            sleep(1)

    def simulation(self):
        while True:
            self.simulation_step(time.time()-self.time_measure) # hopefully this is seconds
            self.time_measure = time.time()
            sleep(self.loop_time)

# ----------- behavior support -------------
    def find_correct_rotation(self):
        # TODO: maybe this is a bit overkill
        # checks the lidar scan and gives back the four corners
        size = len(self.scan_data) - 1
        data = self.scan_data
        minima = []
        for idx in range(size+2):
            if data[(idx - 1) % size] > data[(idx) % size] <  data[(idx+1) % size] and data[(idx - 2) % size] > data[(idx) % size] <  data[(idx+2) % size]:
                minima.append(idx % size)
        return minima

# ---------- actual robot behaviours ------------
    def align_robot(self):
        # robot behavior to align it within the rectangle
        # it will rotate its back to the closest wall detected by the lidar
        start_time = time()
        while True:
            minima = self.find_correct_rotation()
            if len(minima)==0:
                sleep(0.1)
                continue
            req_rot = self.scan_data.index(min(self.scan_data))
            value = min(self.scan_data)

            if value == 0:
                # check to outrule errors in the lidar detection
                continue
            tolerance = 4
            if abs(req_rot) > tolerance and abs(req_rot) < (360 - tolerance):
                if req_rot > 179:
                    self.rotate_by_degree(-(req_rot-360))
                else:
                    self.rotate_by_degree(-req_rot)
                return
            else:
                self.stop_driving()
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
        self.stop_driving()
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
        # 1st order collision avoidance by LIDAR -> must be bigger than 0!
        if LIDAR and 0 < min(self.scan_data[150:210]) < 150:
            return True

        else:
            for i in [0,2,4]:
                if self.prox_horizontal[i] > 500:
                    return True
        return False

#------------------- loop ------------------------
    def simulation_step(self, simulation_time):
        # TODO: check this properly and try to align simu and reality
        print('left_wheel_speed')
        print(self.right_wheel_velocity)
        print(self.aseba.GetVariable("thymio-II", "motor.left.pwm"))
        r_rad_speed = math.pi*self.right_wheel_velocity / 180
        l_rad_speed = math.pi*self.left_wheel_velocity /180
        coo = self.simulator.simulate(self.x, self.y, self.q, r_rad_speed, l_rad_speed, simulation_time)[-1]
        if len(coo) == 3:
            self.x, self.y, self.q = coo

    def simple_control(self):
        # this here needs to be fixed, maybe with schduling the execution of the inner loop or so
        self.loop_time = 0.1
        # self.speed_correction = 1.15
        left_wheel_velocity = 0
        right_wheel_velocity = 0
        self.drive_adj(left_wheel_velocity, right_wheel_velocity)


        self.time_measure = time.time()
        for cnt in range(100): # supposed to be 10s -> well its not
            if cnt % 100==0:
                print(f'x : {self.x}, y: {self.y}, q: {self.q}')
                if cnt == 30:
                    left_wheel_velocity = 0
                    right_wheel_velocity = 0
                    self.drive_adj(left_wheel_velocity, right_wheel_velocity)
                #self.align_robot()
                #print('i am aligned')
                #print('i see wall')
                #if CAMERA:
                #    side = self.robot_vision.get_side(self.picture)
                #    print(f'side is {side}')
                #    self.q = side * math.pi/2
                pass

            sleep(self.loop_time)


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
            lidar_thread = Thread(target=robot.lidar_sensing)
            lidar_thread.daemon = True
            lidar_thread.start()

        thymio_thread = Thread(target=robot.distance_sensing)
        thymio_thread.daemon = True
        thymio_thread.start()

        thymio_thread_vertical = Thread(target=robot.ground_sensing)
        thymio_thread_vertical.daemon = True
        thymio_thread_vertical.start()

        if CAMERA:
            print('camera is on')
            camera_thread = Thread(target=robot.camera_sensing)
            camera_thread.daemon = True
            camera_thread.start()

        simulation = Thread(target=robot.simulation_step)
        simulation.daemon = True
        simulation.start()

        robot.simple_control() # execute the progamm
        print('im done here')
        robot.turn_off()

    except KeyboardInterrupt:
        print("Stopping robot")
        if robot is not None:
            robot.turn_off()
        sleep(1)
        os.system("pkill -n asebamedulla")
        print("asebamodulla killed")
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        if robot is not None:
            robot.turn_off()
        print("Stopping robot")
        print(e)
        sleep(1)
        os.system("pkill -n asebamedulla")
        print("asebamodulla killed")

if __name__ == '__main__':
    main()


# ------------ old code ------------------

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
