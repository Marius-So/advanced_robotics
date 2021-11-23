import matplotlib.pyplot as plt
import cv2
import numpy as np

def diff(a,b):
    res = a - b
    if res < 0:
        return -res
    return res

def mask(img, k_size = 8):
    ret = []
    pas = int(len(img[0])/8)
    for k in range(0, len(img[0]), pas):
        npurple = 0
        nblue = 0
        norange = 0
        nred = 0
        ngreen = 0
        for j in range(k, k + pas):
            for i in range(len(img)):
                r = img[i][j][0]
                g = img[i][j][1]
                b = img[i][j][2]
                if r > 150 and r > g and r > b:
                    nred += 1
                    img[i][j] = [255,0,0]
                if b > 100 and b > r and b>g:
                    nblue += 1
                    img[i][j] = [0,0,255 ]
                if g > 100 and g > r and g>b:
                    ngreen += 1
                    img[i][j] = [0,255, 0]
                if  diff(b,g) < 25 and r > 80 and b > 80 and r > g:
                    npurple += 1
                    img[i][j] = [130, 0, 130]
                if r > 80 and r > g and g > b:
                    norange += 1
                    img[i][j] = [255,125,0]
        print("purple", npurple, "green", ngreen, "red", nred, "orange", norange)
        if max(nred,nblue,norange,npurple,ngreen) == norange and norange > 10:
            ret.append("orange")
        elif max(nred, nblue,norange,npurple,ngreen) == npurple and npurple > 10:
            ret.append("npurple")
        elif max(nred, nblue, norange,npurple,ngreen) == nred  and nred > 10:
            ret.append("red")
        elif max(nred, nblue, norange, npurple,ngreen) == nblue and nblue > 10:
            ret.append("blue")
        elif max(nred, nblue, norange, npurple, ngreen) == ngreen and ngreen > 10:
            ret.append("green")
        else:
            ret.append("nothing")
    return ret

a = """
def get_centers(masks):
    ret = []
    for mask in masks:
        M = cv2.moments(mask)
        if not round(M["m10"]):
            ret.append(int(M["m10"] / M["m00"]))
        else:
            ret.append(None)
    return ret

def get_center(mask):
    n = 0
    si = 0
    sj = 0
    for i in range(len(mask)):
        for j in range(len(mask[i])):
            if mask[i][j] == 255:
                si += i
                sj += j
                n += 1
    if n > 5:
        return (si/n, sj/n)
    return (None, None)
"""

import matplotlib.pyplot as plt
import cv2
import numpy as np

def analyse_for_colours(image, k_size = 5):
    input_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    kernel = np.ones((k_size, k_size), np.uint8)

    # upper mask (170-180)
    lower_red = np.array([155,100,50])
    upper_red = np.array([185,255,255])
    mask1 = cv2.inRange(input_hsv, lower_red, upper_red)

    # join my masks
    red_mask = mask1#mask0+
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)

     # orange
    lower_orange = np.array([80,50,50])
    upper_orange = np.array([110,255,255])
    orange_mask = cv2.inRange(input_hsv, lower_orange, upper_orange)
    orange_mask = cv2.morphologyEx(orange_mask, cv2.MORPH_OPEN, kernel)

    # blue
    # define range of blue color in HSV
    lower_blue = np.array([110,50,0])
    upper_blue = np.array([130,255,255])
    # Threshold the HSV image to get only blue colors
    blue_mask = cv2.inRange(input_hsv, lower_blue, upper_blue)
    blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_OPEN, kernel)

    # green
    lower_green =  np.array([50,50,50])
    upper_green = np.array([70,255,255])
    green_mask = cv2.inRange(input_hsv, lower_green, upper_green)
    green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_OPEN, kernel)

    # purple
    lower_purple = np.array([140,70,70])
    upper_purple = np.array([160,255,255])
    purple_mask = cv2.inRange(input_hsv, lower_purple, upper_purple)
    purple_mask = cv2.morphologyEx(purple_mask, cv2.MORPH_OPEN, kernel)

    return red_mask, orange_mask, blue_mask, green_mask, purple_mask

def update_centers(self):
    for mask in self.masks:
        M = cv2.moments(self.masks[mask])
        if not round(M["m10"]):
            self.centers[mask] = int(M["m10"] / M["m00"]).self.masks[mask].shape[0]
        else:
            self.centers[mask] = None







