from adafruit_rplidar import RPLidar, RPLidarException
from time import time
from threading import Thread
from math import floor

class lidar():
    def __init__(self):
        self.lidar = RPLidar(None, '/dev/ttyUSB0')
        self.lidar_output = {}
        self.local_time = time()
        lidar_thread = Thread(target=self.lidar_sensing)
        lidar_thread_daemon = True
        lidar_thread.start()

    def lidar_sensing(self):
        while True:
            try:
                for scan in self.lidar.iter_scans():
                    for (__, angle, distance) in scan:
                        self.lidar_output[floor(angle)] = distance, time()
                self.local_time = time()
            except RPLidarException:
                self.lidar.stop()
                self.lidar = RPLidar(None, '/dev/ttyUSB0')
