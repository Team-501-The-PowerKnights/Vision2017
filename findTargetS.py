# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 12:01:06 2017

@author: Ithier
"""

import cv2
import numpy as np
import manipulateImageS as MI 
import imageCalculationsS as IC
import validateTargetS as VT

def findValids(img_orig, calibration):
    """
    Input: img_orig -> image, filename of npz file, whether we're in debug mode
    Output: angle -> float, distance -> float, validUpdate -> boolean of whether we've found
    correct targets, BFR_img -> image that has best fit rectangle drawn on it and lines for centering,
    mask_orig -> image of the mask, cnt -> list of contours found for targets
    
    This function uses the npz file values to create a mask of the target. It then
    finds valid targets, calculates the angle and distance, and visualizes the result
    """

    debug = calibration["debug"]["debug"]
    search = calibration["search"]["search"]

    global angle, distance, validUpdate
    angle = 1000
    distance = 0
    validUpdate = False
    
    img = np.copy(img_orig)
    print(calibration["green"]["green_lower"])
    print(calibration["green"]["green_upper"])
    lower_bound = np.array(calibration["green"]["green_lower"])
    upper_bound = np.array(calibration["green"]["green_upper"])

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask_orig = cv2.inRange(hsv,lower_bound,upper_bound)
    
    mask = np.copy(mask_orig)
    
    # Clean up mask with dilate and erode and threshold
    mask_eroded_dilated = MI.dilateAndErode(mask, 5)
    mask = np.copy(mask_eroded_dilated)
    ret, mask_threshold = cv2.threshold(mask, 127, 255, 0)
    mask = np.copy(mask_threshold)

    if debug:
        cv2.imwrite('original_frame.jpg', img_orig)
        cv2.imwrite('original_mask.jpg', mask_orig)
        cv2.imwrite('mask_eroded_dilated.jpg', mask_eroded_dilated)
        cv2.imwrite('mask_threshold', mask_threshold)

    # Determine if there are any valid targets
    if search:
        valid, cnt, Rect_coor, BFR_img, hull = VT.findValidTarget(img, mask)

        if valid:
            validUpdate = True
    
        # Find and draw center
            cx1, cy1 = IC.findCenter(cnt[0])
            cx2, cy2 = IC.findCenter(cnt[1])
            cx = (cx1 + cx2) / 2
            cy = (cy1 + cy2) / 2
        
        # Calculate angle and distance
            angle = IC.findAnglePeg(BFR_img, cx1, cx2)
            distance = IC.findDistance(BFR_img, Rect_coor)

        else:
            validUpdate = False
            BFR_img = img_orig
            print("No Valid targets found")
        return angle, distance, validUpdate, BFR_img, mask_orig, cnt
    else:
        return 0, 0, 0, img_orig, mask_orig, [0, 0]
