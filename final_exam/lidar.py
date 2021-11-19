from adafruit_rplidar import RPLidar, RPLidarException
from time import time

class lidar():
	def __init__(self):
		self.lidar = RPLidar(None, '/dev/ttyUSB0')
		self.lidar_output = {}
		self.start_time = time()
		lidar_thread = Thread(target=self.lidar_sensing)
		lidar_thread_daemon = True
		lidar_thread.start()

	def lidar_sensing(self):
		while True:
			try:
				for scan in self.lidar.iter_scans():
					for (__, angle, distance) in scan:
						self.lidar_output[floor(angle)] = distance, time() - self.start_time()
			except RPLidarException:
				self.lidar.stop()
				self.lidar = RPLidar(None, '/dev/ttyUSB0')
