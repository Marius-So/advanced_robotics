#!/usr/bin/python3

import threading
import dbus
import dbus.mainloop.glib
import sys
import os


class ThymioController(object):
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
        self.l_speed = 0
        self.r_speed = 0

        self.left_speed = 0
        self.right_speed = 0
        self.acc = 0

        self.prox_horizontal = 0
        self.ground_ambiant = 0
        self.ground_reflected = 0
        self.ground_delta = 0
        self.run_on = True


    def set_speed(self, l_speed, r_speed):
        self.l_speed = l_speed
        self.r_speed = r_speed
        self.asebaNetwork.SendEventName(
            'motor.target',
            [self.l_speed, self.r_speed],
            reply_handler=self.dbusReply,
            error_handler=self.dbusError
        )

    def play_tune(self):
        self.asebaNetwork.SendEventName("sound.play(1)")

    def stopAsebamedulla(self):
        # stop the asebamedulla process
        # !!dbus connection will fail after this call
        os.system("pkill -n asebamedulla")

    def run(self):
        # run event loop all 20ms
        threading.Timer(0.02, self.mainLoop).start()

    def dbusReply(self):
        # dbus replys can be handled here.
        # Currently ignoring
        pass

    def dbusError(self, e):
        # dbus errors can be handled here.
        # Currently only the error is logged. Maybe interrupt the mainloop here
        print('dbus error: %s' % str(e))

    def mainLoop(self):
        # read and display acc sensors
        #self.acc = self.asebaNetwork.GetVariable('thymio-II', 'acc')
        self.prox_horizontal = self.asebaNetwork.GetVariable('thymio-II', 'prox.horizontal')
        self.ground_ambiant = self.asebaNetwork.GetVariable('thymio-II', 'prox.ground.ambiant')
        self.ground_reflected = self.asebaNetwork.GetVariable('thymio-II', 'prox.ground.reflected')
        self.ground_delta = self.asebaNetwork.GetVariable('thymio-II', 'prox.ground.delta')
        self.left_speed = self.asebaNetwork.GetVariable("thymio-II", "motor.left.speed")
        self.right_speed = self.asebaNetwork.GetVariable("thymio-II", "motor.right.speed")
        # print the readed sensor values
        print(self.prox_horizontal)
        # increase the counter
        # reschedule mainLoop
        if self.run_on:
            self.run()


def main():
    # check command-line arguments
    #if len(sys.argv) != 2:
    #    print('Usage %s FILE' % sys.argv[0])
    #    return

    # create and run controller
    thymioController = ThymioController()
    thymioController.run()

if __name__ == '__main__':
    main()
