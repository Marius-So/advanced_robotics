import matplotlib.pyplot as plt
import cv2
import numpy as np

def analyse_for_colours(image, k_size = 8):
    input_hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
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
    red_mask = mask0+mask1
    red_mask = cv2.threshold(red_mask, 1, 255, cv2.THRESH_BINARY)[1]
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)

    # blue
    lower_blue = np.array([110,50,50])
    upper_blue = np.array([130,255,255])
    blue_mask = cv2.inRange(input_hsv, lower_blue, upper_blue)
    blue_mask = cv2.threshold(blue_mask, 1, 255, cv2.THRESH_BINARY)[1]
    blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_OPEN, kernel)

    # green
    lower_green = np.array([50,50,50])
    upper_green = np.array([70,255,255])
    green_mask = cv2.inRange(input_hsv, lower_green, upper_green)
    green_mask = cv2.threshold(green_mask, 1, 255, cv2.THRESH_BINARY)[1]
    green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_OPEN, kernel)

    # yellow
    lower_yellow = np.array([25,50,50])
    upper_yellow = np.array([35,255,255])
    yellow_mask = cv2.inRange(input_hsv, lower_yellow, upper_yellow)
    yellow_mask = cv2.threshold(yellow_mask, 1, 255, cv2.THRESH_BINARY)[1]
    yellow_mask = cv2.morphologyEx(yellow_mask, cv2.MORPH_OPEN, kernel)

    return red_mask, blue_mask, green_mask, yellow_mask

def update_centers(self):
    for mask in self.masks:
        M = cv2.moments(self.masks[mask])
        if not round(M["m10"]):
            self.centers[mask] = int(M["m10"] / M["m00"]).self.masks[mask].shape[0]
        else:
            self.centers[mask] = None






