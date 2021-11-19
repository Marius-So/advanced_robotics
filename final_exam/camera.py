from picamera import PiCamera
from threading import Thread
from time import sleep
import numpy as np

class camera():
    def __init__(self):
        self.camera = PiCamera()
        self.camera.start_preview()
        sleep(0.1)
        self.camera.resolution = (320, 240)
        self.camera.framerate = 24
        self.picture = np.empty((240, 320, 3), dtype=np.uint8)
        self.fliped = self.picture
        camera_thread = Thread(target=self.camera_sensing)
        camera_thread_daemon = True
        camera_thread.start()

    def camera_sensing(self):
        while True:
            self.camera.capture(self.picture, 'bgr')
            self.fliped = np.flip(self.picture, 0)

    def __del__(self):
        self.camera.stop_preview()
        self.camera.close()

if __name__ == "__main__":
    a = camera()
    sleep(0.1)
    import matplotlib.pyplot as plt
    while True:
        plt.imshow(a.fliped)
        plt.show()
