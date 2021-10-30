from adafruit_rplidar import RPLidar, RPLidarException
from math import floor
from threading import Thread
import sys
import os
import dbus
import dbus.mainloop.glib

class io_robot(object):
    def __init__(self, filename='thympi.aes1'):
        #thymio
        os.system("(asebamedulla ser:name=Thymio-II &) && sleep 0.3")
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        bus = dbus.SessionBus()
        asebaNetworkObject = bus.get_object('ch.epfl.mobots.Aseba', '/')
        self.asebaNetwork = dbus.Interface(asebaNetworkObject, dbus_interface='ch.epfl.mobots.AsebaNetwork')
        self.asebaNetwork.LoadScripts(filename, reply_handler=self.dbusReply, error_handler=self.dbusError)
        #lidar
        self.lidar = RPLidar(None, '/dev/ttyUSB0')
        self.lidar_output = {}
        lidar_thread = Thread(target=self.lidar_sensing)
        lidar_thread_daemon = True
        lidar_thread.start()

        #camera

    def __del__(self):
        #thymio
        os.system("pkill -n asebamdulla")
        #lidar
        self.lidar.stop()
        #camera

    def dbusReply(self):
        pass

    def dbusError(self, e):
        print("dbus error  : " + str(e))

    def get_thymio_sensor(self):
        return self.asebaNetwork.GetVariable('thymio-II', 'prox.horizontal')

    def get_ground_sensor(self):
        return self.asebaNetwork.GetVariable('thymio-II', 'prox.ground.reflected')

    def lidar_sensing(self):
        while True:
            try:
                for scan in self.lidar.iter_scans():
                    for (__, angle, distance) in scan:
                        self.lidar_output[floor(angle)] = distance
            except RPLidarException:
                self.lidar.stop()
                self.lidar = RPLidar(None, '/dev/ttyUSB0')

    def set_speed(self, l_speed, r_speed):
        self.asebaNetwork.SetVariable('thymio-II', 'motor.left.target', [l_speed])
        self.asebaNetwork.SetVariable('thymio-II', 'motor.right.target', [r_speed])
