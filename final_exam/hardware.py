from camera import camera
from lidar import lidar
from Thymio import Thymio
from time import sleep

class input_output(Thymio, camera, lidar):
    def __init__(self):
        camera.__init__(self)
        lidar.__init__(self)
        Thymio.__init__(self)

def test_Comunications(io, msg):
    #This enables the prox.comm rx value to zero, gets overwritten when receiving a value    
    while True:
        send = io.send_code(msg)
        received = io.get_sensor_values()[4]
        print("received: " + str(received))


if __name__ == '__main__':
    io = input_output()
    sleep(1)
    #print(io.lidar_output)
    test_Comunications(io,1)
