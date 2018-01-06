# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 11:52:35 2017

@author: Ithier
"""

import findTargetS as FT
import NetworkTableModule as NT
import cv2
import time

directory = 'C:/Users/Ithier/Documents/FIRST/2017/Off Season/'
filename = directory + 'imageValues.npz' # folder npz file is in. NPZ file contains hsv values and brightness value
url = 0
debug = 1
validCount = 0 # how many valid targets we've found
n = 0
freqFramesNT = 10 # how often we're sending to network tables

#############################################################################
from networktables import NetworkTable
import logging

#if NetworkTable._staticProvider is None:
try:
    logging.basicConfig(level=logging.DEBUG)
    NetworkTable.setIPAddress('10.5.1.2')
    NetworkTable.setClientMode()
    NetworkTable.initialize()
except:
    if debug == 1:
        print("Network tables has already been initialized")


sd = NetworkTable.getTable("Camera")
#############################################################################
cap = cv2.VideoCapture(url) # capture camera, 0 is laptop cam, numbers after that are cameras attached
time.sleep(2)
# Check to make sure cap was initialized in capture
if debug:
    if cap.isOpened():
        print('Cap succesfully opened')
        print(cap.grab())
    else:
        print('Cap initialization failed')
    
    # Create resizable window for camera 
    cv2.namedWindow('Camera Frame', cv2.WINDOW_NORMAL)

while(cap.isOpened()):
    # Capture frame-by-frame
    #    ret returns true or false (T if img read correctly); frame is array of img    
    ret, frame = cap.read()
    
    if ret == True: # if frame succesfully read
        if frame is None: # if no frame print a blank image
            if debug:
                print('Frame is None')
                Processed_frame = cv2.imread('1.png', 1)
                mask = Processed_frame
    
        else:
            try:
                # Process image
                Angle, Distance, validUpdate, Processed_frame, mask, cnt = FT.findValids(frame, filename, debug)
            
                if validUpdate: 
                    validCount += 1
                
                if n > freqFramesNT:
                    # Send to NetworkTable
                    NT.sendValues(sd, Angle, Distance, validCount)
                    n = 0
                else:
                    n += 1
                
            except:
                Processed_frame = cv2.imread('1.jpg', 1)
                mask = Processed_frame
                if debug:
                    print('There was an error with findValids')
    
    if debug:    
        # Display the resulting frame
        cv2.imshow('Camera Frame', Processed_frame)
        cv2.imshow('Mask', mask)
    
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break
    
# When capture done, release it
cap.release() # !! important to do
if debug:
    cv2.destroyAllWindows()
