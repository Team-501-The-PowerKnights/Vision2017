# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 12:15:18 2017

@author: Ithier
"""
import cv2
import numpy as np
import imageCalculationsS as IC
from heapq import nlargest
import manipulateImageS as MI

def zeroVariables(image):
    BFR_img = image
    hull = [0,0]
    return BFR_img, hull

def isValidShape(contour, rect_cnt):
    matchThreshold = 0.35

    match_quality = cv2.matchShapes(rect_cnt, contour, 2, 0)
    if match_quality < matchThreshold:
        return True
    else:
        return False


def findValidTarget(image, mask, rect_cnt):
    numContours = 6
    BFR_img = np.copy(image)
    areas = []
    hull = []
    cnt = []
    Rect_coor = []
    count = 0
    goodTarget = 0
    
    # find contours
    _, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # take numContours longest contours
    biggestContours = nlargest(numContours, contours, key=len) 
    
    # Determine area of each contour and sort by largest to smallest
    for i in range(0,len(biggestContours)):
        if len(biggestContours[i]) > 3:
            contourMoment = cv2.moments(biggestContours[i])
            contourArea = contourMoment['m00']
            areas.append(contourArea) 
    areas = np.array(areas)
    area_indices = np.argsort(areas) # gives indices of smallest to largest contours in biggestContours
    
    
    if len(areas) > 0:
        # Check for validity of contours in order of largest area to smallest
        rev_indices = list(reversed(area_indices))  # gives indices of largest to smallest contours in biggestContours
        ind = 0  # keeps track of what index we're on within the index list rev_indices
        i = rev_indices[0]  # index of biggestContours that we're testing
        for n in range(0, len(rev_indices)):
            if count == 1:  # count determines whether we stay in the while loop or not as does whether we've found 2 "good targets"
                break
            while goodTarget < 2 and count == 0:
                # Find BFR
                box, hull_indiv, corners, BFR_img = MI.bestFitRect(BFR_img, biggestContours[i])
                
                if len(corners) == 4:
                    # Determine if contour meets specs
                    appropriateCnt = isValidShape(biggestContours[i], rect_cnt)
                    
                    if appropriateCnt:
                        cnt.append(biggestContours[i])
                        hull.append(hull_indiv)
                        Rect_coor.append(IC.organizeCorners(corners))
                        goodTarget += 1
                        
                if i == area_indices[0] or goodTarget == 2: # if we've reached the end of our index list or we've found two good targets 
                    count = 1
                    ind = -1
                
                ind += 1
                i = rev_indices[ind]
        
    if len(cnt) == 2:
        valid = True
    elif len(cnt) == 1:
        valid = False
        BFR_img, hull = zeroVariables(image)
    else:
        valid = False
        BFR_img, hull = zeroVariables(image)
        cnt = [0,0]

    return valid, cnt, Rect_coor, BFR_img, hull