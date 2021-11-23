from camera import camera
from lidar import lidar
from Thymio import Thymio
from time import sleep

class input_output(Thymio, camera, lidar):
    def __init__(self):
        camera.__init__(self)
        lidar.__init__(self)
        Thymio.__init__(self)

if __name__ == '__main__':
    io = input_output()
    sleep(1)
    print(io.lidar_output)
