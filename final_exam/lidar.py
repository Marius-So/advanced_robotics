from adafruit_rplidar import RPLidar, RPLidarException
from time import time
from threading import Thread
from math import floor, inf

class lidar():
    def __init__(self):
        self.lidar = RPLidar(None, '/dev/ttyUSB0')
        self.lidar_output = {}
        self.local_time = time()
        lidar_thread = Thread(target=self.lidar_sensing)
        lidar_thread_daemon = True
        lidar_thread.start()

    def lidar_sensing(self):
		for i in range(360):
			self.lidar_output[i] = inf, time()
        while True:
            try:
                for scan in self.lidar.iter_scans():
                    for (__, angle, distance) in scan:
                        self.lidar_output[floor(angle)] = distance, time()
                self.local_time = time()
            except RPLidarException:
                self.lidar.stop()
                self.lidar = RPLidar(None, '/dev/ttyUSB0')

    def __del__(self):
        self.lidar.stop()

"""
------------------------------
how to use:
    from lidar import lidar
    my_lidar_object = lidar()
    print(my_lidar_object.lidar_output)
    print(my_lidar_object.local_time)
------------------------------
"""
