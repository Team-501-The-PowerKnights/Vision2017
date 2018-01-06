# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 18:30:36 2017

@author: Ithier

This file contains functions for all of the calculations needed for the vision 
processing in the 2017 game
"""
import cv2
import math
from collections import Counter 

def findAnglePeg(image, cx1, cx2, debug):   
    """
    Input: image, cx1 -> float center coordinate of one rectangle, cx2 -> float center coordinate
    of second rectangle, debug -> boolean
    Output: angle -> float
    
    This function finds the robot's angle relative to the peg
    
    """
    global horizontal_cameraFOV, vertical_cameraFOV 
    global h,w,c
    global font
    horizontal_cameraFOV = 61 # degrees
    vertical_cameraFOV = 34.3 # degrees
    
    cx = (cx1 + cx2) / 2.0
    
    h, w, c = image.shape # h = height, w = width, c = channel
    offsetpx = (w/2.0) - cx # offset from center of camera image to center of target (pixels)
    
    angle= int(horizontal_cameraFOV * (offsetpx / w)*100.0)/100.0 
    
    if debug:
        font = cv2.FONT_HERSHEY_SIMPLEX
        image = cv2.putText(image,'Angle: ' + str(angle) + ' deg',(20,85), font, 1,(0,0,255),2,cv2.LINE_AA)
    
    return angle

def findDistance(image, Rect_coor, debug): ############## NEED TO UPDATE VARIABLES #############
    pegHeight = 13.25/12.0 # ft
    targetWidth = 2 # inches
    cameraHeight = 1.5 # ft
    robot2camera = 1.5 # distance from front of robot to camera (ft)
    
    def distance(targetActual, imagePx, targetPx, cameraFOV):
        totalDistance = (((targetActual*imagePx)/targetPx)/2.0) / \
    			math.tan(((cameraFOV*math.pi)/180.0)/2.0)
        totalDistance = int((totalDistance*100.0)/12.0)/100.0  # make into 2 decminal pt and ft
        return totalDistance 
    
    def fixDistance(x): # use polynomial fit to adjust for error
        pass
    
    def targetPixelWidth():
        # In Rect coor indexing first number is countour, second is corner, third is whether it's x or y
        w1 = math.fabs(Rect_coor[0][1][0] - Rect_coor[0][0][0])
        w2 = math.fabs(Rect_coor[0][2][0] - Rect_coor[0][3][0])
        w3 = math.fabs(Rect_coor[1][1][0] - Rect_coor[1][0][0])
        w4 = math.fabs(Rect_coor[1][2][0] - Rect_coor[1][3][0])
        width = (w1 + w2 + w3 + w4)/ 4.0 # avg the widthes of the two targets
        return width
        
    totalDistance_W = distance(targetWidth, w, targetPixelWidth(), horizontal_cameraFOV) # diagonal distance from camera to tower (ft)
    
    try:
        distance_horizontal = math.sqrt(totalDistance_W**2.0 - (pegHeight - cameraHeight)**2.0) - robot2camera # distance from front of robot to tower
        distance_final = int(fixDistance(distance_horizontal*12)*100.0)/100.0 # in
    except:
        distance_final = totalDistance_W*12.0 #in
        if debug:
            print("May be error with distance calculation")
    
    if debug:
        font = cv2.FONT_HERSHEY_SIMPLEX
        image = cv2.putText(image,'Distance: ' + str(distance_final) + ' in',(20,50), font, 1,(0,0,255),2,cv2.LINE_AA)
    
    return distance_final
    
    
def findCenter(cnt):
    M = cv2.moments(cnt)
    # FIND CENTROID Cx = M10/M00, Cy = M01/M00
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/ M['m00'])
    return cx, cy

# Take corner coordinates and organize them in a specific order for easier computations later  
# This is necessary because the corners are returned in a different order each time they are determined
def organizeCorners(corners):
    
    # Save coordinates to variable Rect_coor where corner 0 is the top left corner and the rest are numbered clockwise
    def saveCoordinates(topLeftX, topLeftY, topRightX, topRightY, bottomRightX, bottomRightY, bottomLeftX, bottomLeftY):
        Rect_coor = []
        for i in range(0,4):
            Rect_coor.append([])    
        Rect_coor[0].append(topLeftX)
        Rect_coor[0].append(topLeftY)
        Rect_coor[1].append(topRightX)
        Rect_coor[1].append(topRightY)
        Rect_coor[2].append(bottomRightX)
        Rect_coor[2].append(bottomRightY)
        Rect_coor[3].append(bottomLeftX)
        Rect_coor[3].append(bottomLeftY)
        return Rect_coor
        
    # Determine x coordinates
    corners2 = list(corners.ravel())
    x = []
            
    for i in range(0, len(corners2), 2):
        x.append(corners2[i])
        
    ''' There are three different cases that need to be considered: 1) There are no repeats in the x coordinates
    meaning that you may have an array like [100, 200, 105, 202]  2) There is one repeat in the x coordinates such as
    [100, 100, 200, 202]  3) There are two repeats in the x coordinates such as [100, 200, 100, 200]. The number of 
    duplicates determines the methods to be used to determine the order of the coordinates. This is done below
    '''
    # Check for duplicate and find value
    duplicate = len(x) != len(set(x)) # returns True of False on whether there is a duplicate in the x array
    c = Counter(x).items() # gives array listing the numbers in the array and how many times they occur
    c = list(c)
    doubleVal = [] # this list keeps track of the VALUES of the x coordinates that are repeated. It will be empty if there are no repeats
    if len(c) == 2: # there are two repeats in the x coordinates
        doubleVal.append(c[0][0])
        doubleVal.append(c[1][0])
        doubleVal.sort()
    elif len(c) == 3: # there is one repeat in the x coordinates
        for i in range(0,len(c)):
            if c[i][1] == 2:
                doubleVal.append(c[i][0])
                break
    
    # Determine if repeat number is max or min in array (ie whether it is a top right or bottom right corner (max) or
    # whether it is a top left or bottom left corner (min))
    if len(doubleVal) > 0:
        maximum = max(x) == doubleVal[0] # returns True if it is a maximum (a right corner) or False if it isn't (meaning it is a left corner)
        
    # Find top right and bottom right coordinates
    #     find the indices for the two right corners
    if duplicate: # if duplicate exists
        if len(doubleVal) == 1: # if there is one duplicate
            if maximum: # the duplicate is of a right corner
                indices = [i for i, a in enumerate(x) if a == doubleVal[0]]
                maxXind = indices[0]
                secMaxXind = indices[1]
            else: # the duplicate is of a left corner
                maxXind = x.index(max(x))
                copy = x[:]
                copy.pop(maxXind)
                secMaxVal = max(copy)
                secMaxXind = x.index(secMaxVal)
        else: # there are two duplicates
            indices = [i for i, a in enumerate(x) if a == doubleVal[1]]
            maxXind = indices[0]
            secMaxXind = indices[1]
    else: # there are not duplicates
        maxXind = x.index(max(x))
        copy = x[:]
        copy.pop(maxXind)
        secMaxVal = max(copy)
        secMaxXind = x.index(secMaxVal)
        
    #     determine which index is top and by default is bottom by looking at corresponding 
    # y values to the x coordinates 
    # based on OpenCV coordinate system, top left of pic is (0,0) and x increases as it moves right and y increases as you move down
    if corners2[maxXind*2 + 1] > corners2[secMaxXind*2 + 1]: 
        topRightX = x[secMaxXind]
        topRightY = corners2[secMaxXind*2 + 1]
        bottomRightX = x[maxXind]
        bottomRightY = corners2[maxXind*2 + 1]
    else: 
        bottomRightX = x[secMaxXind]
        bottomRightY = corners2[secMaxXind*2 + 1]
        topRightX = x[maxXind]
        topRightY = corners2[maxXind*2 + 1]
                
    # Find top left and bottom left coordinates
    if duplicate:
        if len(doubleVal) == 1:
            if not maximum:
                indices = [i for i, a in enumerate(x) if a == doubleVal[0]]
                minXind = indices[0]
                secMinXind = indices[1]
            else: 
                minXind = x.index(min(x))
                copy = x[:]
                copy.pop(minXind)
                secMinVal = min(copy)
                secMinXind = x.index(secMinVal)
        else:
            indices = [i for i, a in enumerate(x) if a == doubleVal[0]]
            minXind = indices[0]
            secMinXind = indices[1]
    else:
        minXind = x.index(min(x))
        copy = x[:]
        copy.pop(minXind)
        secMinVal = min(copy)
        secMinXind = x.index(secMinVal)
        
    #     determine which index is top and by default is bottom
    if corners2[minXind*2 + 1] > corners2[secMinXind*2 + 1]:
        topLeftX = x[secMinXind]
        topLeftY = corners2[secMinXind*2 + 1]
        bottomLeftX = x[minXind]
        bottomLeftY = corners2[minXind*2 + 1]
    else: 
        bottomLeftX = x[secMinXind]
        bottomLeftY = corners2[secMinXind*2 + 1]
        topLeftX = x[minXind]
        topLeftY = corners2[minXind*2 + 1]
            
    # Save Coordinates in Proper Order  
    Rect_coor = saveCoordinates(topLeftX, topLeftY, topRightX, topRightY, bottomRightX, bottomRightY, bottomLeftX, bottomLeftY)
    return Rect_coor



