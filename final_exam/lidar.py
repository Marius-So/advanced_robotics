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

if __name__ == "__main__":
    my_lidar_object = lidar()
    import matplotlib.pyplot as plt
    from time import sleep
    from math import cos, sin
    sleep(1)
    while (True):
        for i in list(my_lidar_object.lidar_output.keys()):
            if time() - my_lidar_object.lidar_output[i][1] < 1:
                plt.scatter(cos(i/57.3)*my_lidar_object.lidar_output[i][0], sin(i/57.3)*my_lidar_object.lidar_output[i][0], color="blue")
        plt.scatter(0,0,color="green")
        plt.show()
