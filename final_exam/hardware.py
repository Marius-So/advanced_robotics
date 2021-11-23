from camera import camera
from lidar import lidar
from Thymio import Thymio
from camera_analysis import analyse_for_colours
import time
import numpy as np

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
    from camera_analysis import mask
    import matplotlib.pyplot as plt
    from time import sleep

    io = input_output()
    sleep(1)
    picture = io.take_picture()
    start = time.time()
    mask(picture)
    print(time.time()- start)
    start = time.time()
    y = analyse_for_colours(picture)
    print(time.time()- start)

    plt.imshow(np.concatenate(y))
    plt.show()
    #print(io.lidar_output)
    #test_Comunications(io,1)
