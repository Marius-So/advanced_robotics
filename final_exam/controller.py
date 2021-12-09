from os import name
from hardware import input_output
import numpy as np
from time import sleep, time
from camera_analysis import analyse_for_colours, get_all_detections
from NN import NN
from Thymio import Thymio

class controller(input_output,):
    def __init__(self, avoider=True, genes = []):
        input_output.__init__(self)
        # TODO: type of contoller

        self.active = True
        self.locked_sender = time()
        self.diffspeed = 0


        self.set_colour('red')
        self.cur_colour = 'red'
        self.transmission_code = 1
        # then we create the feed forward network based on the genes
        # TODO: create nn based on the genes
        self.NN = NN(genes, input_neurons=39, hidden_neurons=10, output_neurons=10)

    def mainloop(self):
        # update sensor values
        prox_horizontal, ground_reflected, left_speed, right_speed, rx = self.get_sensor_values()
        if 200 < ground_reflected[1] < 700:
            self.set_colour('orange')
            self.cur_colour = 'orange'

        elif self.cur_colour != 'red':
            self.set_colour('red')
            self.cur_colour = 'red'

        self.send_code(self.transmission_code)

        # here comes the wheel input based on the genes
        # TODO: for now we just send random wheel speeds
        d = self.build_input(30)
        if d[-2] == 1:
            self.set_speed(-400,-400)
            sleep(1)
            if np.random.random() < 0.5:
                self.set_speed(-400,400)
            else:
                self.set_speed(400,-400)
            sleep(0.7)
            self.lock_time = time()
        else:
            l_sp, r_sp = self.NN.forward_propagation(d)
            speed_factor = 50
            if l_sp == -r_sp:
                speed_factor=10
            self.diffspeed =(r_sp-l_sp)*speed_factor
            self.set_speed(l_sp *speed_factor * (48/50), r_sp*speed_factor)

    def run(self):
        while self.active:
            self.mainloop()

    def stop(self):
        self.active = False

    def build_input(self, ds=10):
        lidar_output = self.lidar_output
        camera_output = self.result
        prox_horizontal, ground_reflected, left_speed, right_speed, rx = self.get_sensor_values()
        output = []
        lidar_output2 = [float('inf')] * 360
        tmps = time()
        for i in range(360):
            if time() - lidar_output[(i + 180)%360][1] < 0.7:
                lidar_output2[(i + int(0.23*self.diffspeed*(tmps-lidar_output[(i + 180)%360][1])))%360] = lidar_output[(i + 180)%360][0]

        for i in range(0, 360, ds):
            for j in range(i, i + ds):
                m = float('inf')
                if lidar_output2[j] < m:
                    m = lidar_output2[j]
            if m == float('inf') or m > 1000:
                output.append(0)
            else:
                output.append(1 - m/2000)
        for i in camera_output:
            for j in i:
                output.append(j)

        if ground_reflected[1]>700:
            output.append(0)
            output.append(0)
        elif ground_reflected[1]>300:
            # hard coded safe zone
            output.append(0)
            output.append(1)
        else:
            output.append(1)
            output.append(0)
        return output

if __name__ == "__main__":
    try:
        genes = np.loadtxt('seeker.txt', delimiter=', ')
        robot = controller(avoider=False, genes=genes)
        robot.run()
    except KeyboardInterrupt:
        robot.set_speed(0,0)
        robot.set_colour('red')
