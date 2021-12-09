from picamera import PiCamera
from threading import Thread
from time import sleep
import numpy as np
from camera_analysis import analyse_for_colours, get_all_detections

class camera():
    def __init__(self):
        self.camera = PiCamera()
        self.camera.start_preview()
        sleep(0.1)
        self.camera.resolution = (224, 176)
        self.camera.framerate = 24
        self.picture = np.empty((176, 224, 3), dtype=np.uint8)
        camera_thread = Thread(target=self.camera_sensing)
        camera_thread_daemon = True
        camera_thread.start()

    def camera_sensing(self):
        while True:
            try:
                temp_img = np.empty((176, 224, 3), dtype=np.uint8)
                self.camera.capture(temp_img, 'rgb')
                self.picture = np.flip(np.flip(self.picture, 0),1)
                colour_masks = analyse_for_colours(temp_img, 3)
                temp_img = get_all_detections(colour_masks, bins=5, tr=0.001)
                self.picture = temp_img
            except Exception as e:
                print(e)
                sleep(2)
                pass


    def __del__(self):
        self.camera.stop_preview()
        self.camera.close()


if __name__ == "__main__":
    a = camera()
    sleep(0.1)
    import matplotlib.pyplot as plt
    from camera_analysis import analyse_for_colours

    picture = a.take_picture()
    masks = analyse_for_colours(picture)
    mask = np.concatenate(masks, axis=1)
    im = plt.imshow(picture)
    plt.show()

    while True:
        print('upd')
        picture = a.take_picture()
        masks = analyse_for_colours(picture)
        mask = np.concatenate(masks, axis=1)
        im.set_data(mask)

    plt.ioff() # due to infinite loop, this gets never called.
    plt.show()
