import cv2
import numpy as np

class vision:
    def __init__(self) -> None:
        self.vision = None
        self.angle = None
        self.red_mask = None
        self.blue_mask = None
        self.yellow_mask = None
        self.green_mask = None
        self.updated = False

        self.masks = {'green': self.green_mask,
                    'blue': self.blue_mask,
                    'red': self.red_mask,
                    'yellow': self.yellow_mask}

        self.centers = {'green': None,
                    'blue': None,
                    'red': None,
                    'yellow': None}

    def update_vision(self, k_size = 8):
        input_hsv = cv2.cvtColor(self.vision, cv2.COLOR_BGR2HSV)
        kernel = np.ones((k_size, k_size), np.uint8)

        # lower mask (0-10)
        lower_red = np.array([0,50,50])
        upper_red = np.array([10,255,255])
        mask0 = cv2.inRange(input_hsv, lower_red, upper_red)

        # upper mask (170-180)
        lower_red = np.array([170,50,50])
        upper_red = np.array([180,255,255])
        mask1 = cv2.inRange(input_hsv, lower_red, upper_red)

        # join my masks
        self.red_mask = mask0+mask1
        self.red_mask = cv2.threshold(self.red_mask, 1, 255, cv2.THRESH_BINARY)[1]
        self.red_mask = cv2.morphologyEx(self.red_mask, cv2.MORPH_OPEN, kernel)

        # blue
        lower_blue = np.array([110,50,50])
        upper_blue = np.array([130,255,255])
        self.blue_mask = cv2.inRange(input_hsv, lower_blue, upper_blue)
        self.blue_mask = cv2.threshold(self.blue_mask, 1, 255, cv2.THRESH_BINARY)[1]
        self.blue_mask = cv2.morphologyEx(self.blue_mask, cv2.MORPH_OPEN, kernel)

        # green
        lower_green = np.array([50,50,50])
        upper_green = np.array([70,255,255])
        self.green_mask = cv2.inRange(input_hsv, lower_green, upper_green)
        self.green_mask = cv2.threshold(self.green_mask, 1, 255, cv2.THRESH_BINARY)[1]
        self.green_mask = cv2.morphologyEx(self.green_mask, cv2.MORPH_OPEN, kernel)

        # yellow
        lower_yellow = np.array([25,50,50])
        upper_yellow = np.array([35,255,255])
        self.yellow_mask = cv2.inRange(input_hsv, lower_yellow, upper_yellow)
        self.yellow_mask = cv2.threshold(self.yellow_mask, 1, 255, cv2.THRESH_BINARY)[1]
        self.yellow_mask = cv2.morphologyEx(self.yellow_mask, cv2.MORPH_OPEN, kernel)

    def update_centers(self):
        for mask in self.masks:
            M = cv2.moments(self.masks[mask])
            if not round(M["m10"]):
                self.centers[mask] = int(M["m10"] / M["m00"]).self.masks[mask].shape[0]
            else:
                self.centers[mask] = None

    def get_most_confident(self):
        biggest_ = 0
        best_mask = None
        for mask in self.masks:
            mass = np.sum(self.masks[mask])
            if mass :





# calculate x,y coordinate of center


print(cX)
print(cY)

    def update_vison(self, picture):
        self.vision = picture
        self.updated = True

    def get_most_likely_color(self):


    def get_rotation(self):


