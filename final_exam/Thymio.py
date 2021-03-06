#!/usr/bin/python3

import threading
import dbus
import dbus.mainloop.glib
import sys
import os
import time
import sys
import numpy as np

thymio_colour = {
    'red': [32,0,0],
    'orange': [32,32,0],
    'blue': [0,0,32],
    'green': [0,32,0],
    'purple': [32,0,32],
    'off': [0,0,0]
}

class Thymio(object):
    def __init__(self, filename='thympi.aesl'):
        # initialize asebamedulla in background and wait 0.3s to let
        # asebamedulla startup (!!bad habit to wait...)
        os.system("(asebamedulla ser:name=Thymio-II &) && sleep 0.3")

        # init the dbus main loop
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

        # get stub of the aseba network
        bus = dbus.SessionBus()
        asebaNetworkObject = bus.get_object('ch.epfl.mobots.Aseba', '/')

        # prepare interface
        self.asebaNetwork = dbus.Interface(
            asebaNetworkObject,
            dbus_interface='ch.epfl.mobots.AsebaNetwork'
        )

        # load the file which is run on the thymio
        self.asebaNetwork.LoadScripts(
            filename,
            reply_handler=self.dbusReply,
            error_handler=self.dbusError
        )

        # initialize some variables which can be used in the main loop
        # to set thymio states
        self.left_speed = 0
        self.right_speed = 0
        self.rx = -1

        self.prox_horizontal = 0
        self.ground_ambiant = 0
        self.ground_reflected = 0
        self.ground_delta = 0
        self.run_on = True

        self.turn_off_leds()
        #enables the prox.com communication
        self.send_event( "prox.comm.enable", [1])
        # TODO: check for error when using  -> prox.comm.
        #enables the prox.comm rx value to zero
        self.send_event("prox.comm.tx",[0])
        self.send_event("prox.comm.rx",[0])

    def __del__(self):
        self.set_speed(0,0)
        self.set_colour('off')
        os.system("pkill -n asebamedulla")
        sys.exit()

    def send_event(self, name, inp):
        self.asebaNetwork.SendEventName(
            name,
            inp,
            reply_handler=self.dbusReply,
            error_handler=self.dbusError
        )

    def get_variable(self, name, var):
        return self.asebaNetwork.GetVariable(name, var)

    def turn_off_leds(self):
        self.send_event('leds.prox.v',[0,0])
        self.send_event('leds.buttons',[0,0,0,0])
        self.send_event('leds.prox.h',[0,0,0,0,0,0,0])
        self.send_event('leds.circle',[0,0,0,0,0,0,0])
        self.send_event('leds.rc',[0])
        self.send_event('leds.temperature',[0,0])

    def set_speed(self, l_speed, r_speed):
        self.send_event('motor.target',[l_speed, r_speed])

    def play_tune(self):
        self.asebaNetwork.SendEventName("sound.play",[3])

    def dbusReply(self):
        # dbus replys can be handled here.
        # Currently ignoring
        pass

    def dbusError(self, e):
        # dbus errors can be handled here.
        # Currently only the error is logged. Maybe interrupt the mainloop here
        print('dbus error: %s' % str(e))

    def get_sensor_values(self):
        # read and display acc sensors
        #self.acc = self.asebaNetwork.GetVariable('thymio-II', 'acc')
        prox_horizontal = self.get_variable('thymio-II', 'prox.horizontal')
        ground_ambiant = self.get_variable('thymio-II', 'prox.ground.ambiant')
        ground_reflected = self.get_variable('thymio-II', 'prox.ground.reflected')
        ground_delta = self.get_variable('thymio-II', 'prox.ground.delta')
        left_speed = self.get_variable("thymio-II", "motor.left.speed")
        right_speed = self.get_variable("thymio-II", "motor.right.speed")

        # sending and receiving information
        received = self.get_variable("thymio-II", "prox.comm.rx")
        if received is not None:
            rx = received[0]

        return np.array(prox_horizontal), np.array(ground_reflected), np.array(left_speed), np.array(right_speed), np.array(rx)

    def send_code(self, code):
        self.asebaNetwork.SendEventName("prox.comm.tx", [code])

    def set_colour(self, colour):
        self.send_event('leds.bottom.left',thymio_colour[colour])
        self.send_event('leds.bottom.right',thymio_colour[colour])
        self.send_event('leds.top',thymio_colour[colour])

    def test_Comunications(self, msg):
    #This enables the prox.comm rx value to zero, gets overwritten when receiving a value
        while True:
            received = 999
            self.send_code(msg)
            all_values = self.get_sensor_values()
            received = all_values[4]
            print("received: " + str(received))
            print("send: " + str(msg))
            print(all_values)

    def test_other(self):
        self.set_colour('purple')
        self.set_speed(0,0)
        self.get_sensor_values()
        for colour in ['red','orange','blue','green','purple']:
            time.sleep(3)
            print(colour)
            self.set_colour(colour)
            self.set_speed(0,0)
            self.get_sensor_values()



def main():
    # check command-line arguments
    # create and run controller
    thymioController = Thymio()
    thymioController.set_colour('purple')
    thymioController.set_speed(0,0)
    for colour in ['red','orange','blue','green','purple']:
        time.sleep(3)
        print(colour)
        thymioController.set_colour(colour)
        thymioController.set_speed(0,0)
        thymioController.get_sensor_values()

if __name__ == '__main__':
    main()
    #tm = Thymio()
    #tm.test_Comunications(19)
    #tm.test_other()
