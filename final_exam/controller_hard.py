from os import name
from typing import Iterator
from hardware import input_output
import numpy as np
from time import sleep, time
from camera_analysis import analyse_for_colours, get_all_detections
from NN import NN
from Thymio import Thymio
import traceback

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
		#print(self.get_camera_output())
		# update sensor values
		prox_horizontal, ground_reflected, left_speed, right_speed, rx = self.get_sensor_values()
		# behavior when avoider
		if self.avoider:
			if rx == 1:
				self.set_colour('purple')
				self.set_speed(0,0)
				self.active = False

			# TODO: fix these values for the save zone
			if 400 < ground_reflected[1] < 700:
				self.set_colour('green')
				self.cur_colour = 'green'
				self.send_code(3)
				sleep(1)
				self.set_speed(0,0)
				self.lock_time = time() + 200

			elif self.cur_colour != 'blue':
				self.set_colour('blue')
				self.cur_colour = 'blue'
				self.lock_time = time()

			if self.cur_colour == 'green' and rx == 2:
				# we need to speed out of the safe zone
				#TODO: do leave save zone behavior
				self.must_leave = True
				self.lock_time = time()
				self.transmission_code = 3
				self.locked_sender = time() + 5
				self.send_code(self.transmission_code)

			if self.transmission_code == 3 and time() > self.locked_sender:
				self.transmission_code == 2
				self.send_code(self.transmission_code)

		# behavior when seeker
		else:
			if 200 < ground_reflected[1] < 700:
				self.set_colour('orange')
				self.cur_colour = 'orange'
				self.transmission_code == 3
				self.lock_time = time()

			elif self.cur_colour != 'red':
				self.set_colour('red')
				self.cur_colour = 'red'
				self.transmission_code == 1
				self.lock_time = time()

			self.send_code(self.transmission_code)

		# avoid the black tape we avoid the tape either way
		if ground_reflected[1] < 300:
			self.set_speed(-400,-400)
			sleep(1)
			if np.random.random() < 0.5:
				self.set_speed(-400,400)
			else:
				self.set_speed(400,-400)
			sleep(0.7)
			self.lock_time = time()

			#self.set_speed(0,0)

		if self.lock_time < time():
			if len(self.action_list) == 0:
				e =self.get_behavioral_moves()
				self.action_list = self.get_behavioral_moves()

			left_speed, right_speed, exec_sec  = self.action_list[0]
			self.lock_time = time() + exec_sec
			self.action_list = self.action_list[1:]

			factor = 1
			self.set_speed(left_speed*factor * (48/50), right_speed*factor)
		sleep(0.01)


	def get_behavioral_moves(self):
		observation = self.build_input(20)

		lidar = observation[:20]
		camera_obs = observation[20:45]

		if self.avoider:
			if self.must_leave:
				if sum(camera_obs[:5])>= 1:
					return [(-300,-300,2)]
				else:
					return [(300, 300, 2)]
			# when he sees red
			if sum(camera_obs[:5])>= 1:
				x = -500
				y = -300
				for idx, e in enumerate(camera_obs[:5]):
					if e == 1:
						if idx < 3:
							return [(x,y - (100 * idx), 1)]
						else:
							return [(x + ((idx-2)*100), x, 1)]

				# if he sees green
			if sum(camera_obs[17:18])>1:
				x = 500
				y = 200
				for idx, e in enumerate(camera_obs[:5]):
					if e == 1:
						if idx < 3:
							return [(y + (100 * idx), x, 1)]
						else:
							return [(x, x - ((idx-2) * 100), 1)]

			if max(lidar[:-5]+lidar[16:]) > 0.7:
				return [(500, 500, 4)]

			if max(lidar[5:16]) > 0.7:
				if np.random.random() > 0.5:
					return [(-350, -500, 3)]
				else:
					return [(-500, -350, 3)]

			if np.random.random() > 0.5:
				return [(500, 400, 1)]
			else:
				return [(400, 500, 1)]

		# HERE comes the Seeker
		else:
			#if np.random.random() > 0.5:
			#	return [(500,400,4)]
			#else:
			#	return [(400,500,4)]
			# seeing blue
			print(camera_obs[10:15])
			if sum(camera_obs[10:15])> 1:
				self.play_tune
				x = 500
				y = 300
				for idx, e in enumerate(camera_obs[10:15]):
					if e == 1:
						if idx < 3:
							return [(y + (100 * idx), x, 1)]
						else:
							return [(x, x - ((idx-2) * 100), 1)]

			if max(lidar[8:12]) > 0.7:
				print('here')
				return [(-500, 500, 1), (500, 500, 2)]

			if max(lidar[:3]+lidar[-3:]) > 0.7:
				return [(500, 500, 1)]


			if np.random.random() > 0.5:
				return [(500, 400, 1)]
			else:
				return [(400, 500, 1)]

	def run(self):
		count = 0
		while self.active:
			count+=1
			if count//100 == 0:
				pass
			self.mainloop()

	def stop(self):
		self.active = False

	def get_camera_output(self):
		#picture = self.picture
		#colour_masks = analyse_for_colours(picture)
		#return get_all_detections(colour_masks, bins=5, tr=0.01)
		return self.picture

	def build_input(self, ds=10):
		lidar_output = self.lidar_output
		camera_output = self.get_camera_output()
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
		elif ground_reflected[1]>200:
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
		robot = controller(avoider=False)
		robot.run()
	except KeyboardInterrupt:
		robot.set_speed(0,0)
		robot.set_colour('red')
	except Exception as e:
		robot.set_speed(0,0)
		robot.set_colour('red')
		print(traceback(e))
