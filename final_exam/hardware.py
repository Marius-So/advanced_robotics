from picamera import PiCamera
from threading import Thread
from time import sleep, time
import numpy as np
from math import floor
from adafruit_rplidar import RPLidar, RPLidarException

class input_output():
    def __init__(self):
        #camera
        self.camera = PiCamera()
        self.camera.start_preview()
        sleep(0.1)
        self.camera.resolution = (320, 240)
        self.camera.framerate = 24
        self.picture = np.empty((240, 320, 3), dtype=np.uint8)
        self.fliped = self.picture
        camera_thread = Thread(target=self.camera_sensing)
        camera_thread_daemon = True
        camera_thread.start()

        #lidar
        self.lidar = RPLidar(None, '/dev/ttyUSB0')
        self.lidar_output = {}
        lidar_thread = Thread(target=self.lidar_sensing)
        lidar_thread_daemon = True
        lidar_thread.start()

    def camera_sensing(self):
        while True:
            self.camera.capture(self.picture, 'rgb')
            #self.fliped = np.flip(self.picture, 0)

    def lidar_sensing(self):
        while True:
            try:
                for scan in self.lidar.iter_scans():
                    for (__,angle, distance) in scan:
                        self.lidar_output[floor(angle)] = distance, time()
            except RPLidarException:
                self.lidar.stop()
                self.lidar = RPLidar(None, '/dev/ttyUSB0')

    def __del__(self):
        #camera
        self.camera.stop_preview()
        self.camera.close()
        #lidar
        self.lidar.stop()
        print("test")


if __name__ == "__main__":
    a = input_output()
    sleep(0.1)
    import matplotlib.pyplot as plt
    from camera_analysis import analyse_for_colours
    while True:
        a.fliped = np.flip(a.picture, 0)
        red_mask, blue_mask, green_mask, yellow_mask = analyse_for_colours(a.fliped)
        plt.imshow(a.fliped)
        plt.show()
