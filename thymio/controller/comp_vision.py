import  matplotlib.pyplot as plt
import cv2
import numpy as np
import apriltag
import math

from time import sleep

class robot_vision:
    def __init__(self) -> None:
        self.vision = None
        self.det_result = None
        self.detector = apriltag.Detector()
        H = 1
        W = 2
        self.centers = {
            0: (0.5 * W, 0 * H),
            1: (0.5 * W, -0.45 * H),
            2: (0.475 * W, -0.5 * H),
            3: (0.25 * W, -0.5 * H),
            4: (0 * W, -0.5 * H),
            5: (-0.25 * W, -0.5 * H),
            6: (-0.475 * W, -0.5 * H),
            7: (- 0.5 * W, -0.45 * H),
            8: (- 0.5 * W, 0 * H),
            9: (- 0.5 * W, 0.45 * H),
            10: (-0.475 * W, 0.5 * H),
            11: (-0.25 * W, 0.5 * H),
            12: (0 * W, 0.5 * H),
            13: (0.25 * W, 0.5 * H),
            14: (0.475 * W, 0.5 * H),
            15: (0.5 * W, 0.45 * H)
        }

        self.side= {
            0: 0,
            1: 0,
            2: 3,
            3: 3,
            4: 3,
            5: 3,
            6: 3,
            7: 2,
            8: 2,
            9: 2,
            10: 1,
            11: 1,
            12: 1,
            13: 1,
            14: 1,
            15: 0,
        }

        self.corners = {
            0:(-0.5 * W, 0.5 * H),
            1:(-0.5 * W, -0.5 * H),
            2:(0.5 * W, -0.5 * H),
            3:(0.5 * W, 0.5 * H)
        }
        self.corner_parts = [1,2,6,7,9,10,14,15]
        self.corners = {(1,2): 0, (6,7):1, (9,10):2, (14,15):3}


    def scan_vision(self):
        self.det_result = self.detector.detect(self.vision)

    def update_vision(self, picture):
        self.vision = picture

    def find_corners(self):
        # assume i can never see three corners at the same time -> otherwise give center corner
        # because then I am very far away from it
        number_of_tags = len(self.det_result)
        self.detected_corners = {}
        if len(self.det_result) > 0:
            for tag in range(number_of_tags - 1):
                # abusign that scan orders the tags in increasing order
                tag_pair = (self.det_result[tag].tag_id, self.det_result[tag+1].tag_id)
                if tag_pair in self.corners:
                    corner = self.corners[tag_pair]
                    c_center = self.det_result[tag+1].center[0] - self.det_result[tag].center[0] # approximate x pos of corner in picture --> roughly
                    self.detected_corners[corner] = c_center

    def get_center_tag(self):
        focus = self.vision.shape[1] / 2
        min_dist = float('inf')
        min_tag = None
        for tag in self.det_result:
            if tag.tag_id < 16:
                dist = abs(focus - tag.center[0])
                if dist < min_dist:
                    min_dist = dist
                    min_tag = tag.tag_id
        return min_tag

    def estimate_rotation(self):
        #if len(self.detected_corners) == 2:
        #    # most usual case I would say....
        #    # thisis what I am looking at
        #    # this is pretty superficial...
        focus = self.vision.shape[1] / 2

        # simple approach use most center tag to estimate the rot
        min_dist = float('inf')
        min_tag = None
        for tag in self.det_result:
            if tag.tag_id < 16:
                dist = abs(focus - tag.center[0])
                if dist < min_dist:
                    min_dist = dist
                    min_tag = tag.tag_id

        loc_center_tag = self.centers[min_tag]
        print(min_tag)
        return math.atan2(loc_center_tag[1],loc_center_tag[0])

    def get_side(self, picture):
        picture = cv2.cvtColor(picture, cv2.COLOR_BGR2GRAY)
        self.update_vision(picture)
        self.scan_vision()
        #self.side[self.get_center_tag()]
        # TODO: catch error when he can not see
        return self.side[self.get_center_tag()]


    def estimate_rotation(self, picture):
        self.update_vision(picture)
        self.scan_vision()
        return self.estimate_rotation()


if __name__ == '__main__':
    vision = robot_vision()
    image = cv2.imread('orientation_test/IMG_2887.png')

    img = image
    scale_percent = 20 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)

    # resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

    image = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

    vision.update_vision(image)
    vision.scan_vision()
    print(vision.estimate_rotation())
    pass




