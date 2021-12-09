from os import name
from typing import Iterator
from hardware import input_output
import numpy as np
from time import sleep, time
from camera_analysis import analyse_for_colours, get_all_detections
from NN import NN
from Thymio import Thymio
import traceback
from behaviour_avoider import get_behavioural_moves

class controller(input_output,):
    def __init__(self, avoider=True, genes = []):
        input_output.__init__(self)
        # TODO: type of contoller

        self.active = True
        self.avoider = avoider
        self.locked_sender = time()
        self.lock_time = time()
        self.action_list = []

        if self.avoider:
            self.set_colour('blue')
            self.cur_colour = 'blue'
            self.transmission_code = 2
            self.must_leave = False

        else:
            self.set_colour('red')
            self.cur_colour = 'red'
            self.transmission_code = 1

    def mainloop(self):
        self.send_code(1)
        #print(self.get_camera_output())
        # update sensor values
        prox_horizontal, ground_reflected, left_speed, right_speed, rx = self.get_sensor_values()
        # behavior when avoider
        if self.avoider:
            if rx == 1 and self.cur_colour == 'blue':
                self.set_colour('purple')
                self.set_speed(0,0)
                self.active = False

            # TODO: fix these values for the save zone
            if 400 < ground_reflected[1] < 700:
                self.set_colour('green')
                self.cur_colour = 'green'
                self.send_code(3)
                self.set_speed(0,0)
                self.lock_time = time() + 200

            elif self.cur_colour != 'blue':
                self.set_colour('blue')
                self.cur_colour = 'blue'
                self.lock_time = time()

            if self.cur_colour == 'green' and rx == 2:
                # we need to speed out of the safe zone
                #TODO: do leave save zone behavior
                if ground_reflected[1] > 400:
                    self.must_leave = True
                    self.set_speed(200,200)
                    self.lock_time = time()
                    self.transmission_code = 3
                    self.locked_sender = time() + 5
                    sleep(2)

            if self.transmission_code == 3 and time() > self.locked_sender:
                self.transmission_code == 2

            self.send_code(self.transmission_code)

        # avoid the black tape we avoid the tape either way
        if ground_reflected[1] < 400:
            factior = 1
            if left_speed < 0: factior = -1
            self.set_speed(factior*-400,factior*-400)
            sleep(0.5)
            if np.random.random() < 0.5:
                self.set_speed(-400,400)
            else:
                self.set_speed(400,-400)
            sleep(0.7)
            self.lock_time = time()

        if self.lock_time < time():
            if len(self.action_list) == 0:
                observation = self.build_input(20)
                self.action_list = get_behavioural_moves(observation)

            left_speed, right_speed, exec_sec  = self.action_list[0]
            self.lock_time = time() + exec_sec
            self.action_list = self.action_list[1:]
            self.set_speed(left_speed * (48/50), right_speed)

    def run(self):
        count = 0
        while self.active:
            count+=1
            if count//100 == 0:
                pass
            self.mainloop()

    def stop(self):
        self.active = False

    def build_input(self, ds=10):
        lidar_output = self.lidar_output
        camera_output = self.result
        print(camera_output)
        prox_horizontal, ground_reflected, left_speed, right_speed, rx = self.get_sensor_values()
        output = []
        for i in range(0, 360, ds):
            for j in range(i, i + ds):
                m = float('inf')
                if time() - lidar_output[(j + 180)%360][1] < 0.5 and lidar_output[(j + 180)%360][0] < m:
                    m = lidar_output[(j + 180)%360][0]
                    # TODO: hard codedthreshold
            if m == float('inf') or m > 1999 or (1 - m/2000) < 0.5:
                output.append(0)
            else:
                output.append(1 - m/2000)
        for i in camera_output:
            for j in i:
                output.append(j)

            # TODO remove hard code
        if ground_reflected[1]>700:
            output.append(0)
            output.append(0)
        elif ground_reflected[1]>300:
            # hard coded safe zone
            output.append(0)
            output.append(1)
        else:
            #TODO: hard code for testing on black floor
            output.append(1)
            output.append(0)
        return output

if __name__ == "__main__":
    try:
        robot = controller(avoider=True)
        robot.run()
    except KeyboardInterrupt:
        robot.set_speed(0,0)
        robot.set_colour('red')
    except Exception as e:
        robot.set_speed(0,0)
        robot.set_colour('red')
        print(traceback(e))
