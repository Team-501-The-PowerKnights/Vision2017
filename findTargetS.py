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

def findValids(img_orig, filename, debug):
    """
    Input: img_orig -> image, filename of npz file, whether we're in debug mode
    Output: angle -> float, distance -> float, validUpdate -> boolean of whether we've found
    correct targets, BFR_img -> image that has best fit rectangle drawn on it and lines for centering,
    mask_orig -> image of the mask, cnt -> list of contours found for targets
    
    This function uses the npz file values to create a mask of the target. It then
    finds valid targets, calculates the angle and distance, and visualizes the result
    """
    global angle, distance, validUpdate
    angle = 1000
    distance = 0
    validUpdate = False
    
    # Make copy of frame/image to work with
    img = np.copy(img_orig)
    
    # LOADING CALIBRATION FROM FILE -- TO FIX -- THIS IS A TEXT FILE
    values = np.load(filename)
    brightness = float(values['brightness'])
    lower_bound = values['lower']
    upper_bound = values['upper']
    
    # Create img with parameters
    img_darker = MI.darkenImage(img, brightness)
    hsv = cv2.cvtColor(img_darker, cv2.COLOR_BGR2HSV)
    mask_orig = cv2.inRange(hsv,lower_bound,upper_bound)
    
    mask= np.copy(mask_orig)
    
    # Clean up mask with dilate and erode and threshold
    mask = MI.dilateAndErode(mask, 5)
    maskc = np.copy(mask)
    ret,maskc = cv2.threshold(maskc,127,255,0)
    mask = np.copy(maskc)
    
    # Determine if there are any valid targets
    valid, cnt, Rect_coor, BFR_img, hull = VT.findValidTarget(img, mask, debug)

    if valid: 
        validUpdate = True
    
        # Find and draw center
        cx1, cy1 = IC.findCenter(cnt[0]) 
        cx2, cy2 = IC.findCenter(cnt[1])
        cx = (cx1 + cx2) / 2
        cy = (cy1 + cy2) / 2
        
        # Calculate angle and distance
        angle = IC.findAnglePeg(BFR_img, cx1, cx2, debug)
        distance = IC.findDistance(BFR_img, Rect_coor, debug)        
        
        # Visualize calculation
        if debug:
            MI.drawLine2Target(BFR_img, cx, cy)  
            MI.drawCrossHairs(BFR_img)          
    else:
        validUpdate = False
        BFR_img = img_orig
        if debug:
            print('No Valid Update')
            MI.drawCrossHairs(BFR_img)
    
    return angle, distance, validUpdate, BFR_img, mask_orig, cnt
