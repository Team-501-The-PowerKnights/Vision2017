# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 11:52:35 2017

@author: Ithier
"""

import findTargetS as FT
import NetworkTableModule as NT
import cv2
import time
from networktables import NetworkTable
import logging
import numpy as np

url = 0             # CAMERA ADDRESS, 0 is local on Windows
debug = 1           # debug level
validCount = 0      # how many valid targets we've found
n = 0               # iterator
freqFramesNT = 10   # send to NetworkTables ever X frames

logging.basicConfig(level=logging.DEBUG)

def load_file():
    """
    loads npz file (camera calibration)
    returns float,int,int
    """
    filename = "imageValues.npz" # folder npz file is in. NPZ file contains hsv values and brightness value
    values = np.load(filename)
    brightness = float(values['brightness'])
    lower_bound = values['lower']
    upper_bound = values['upper']

try:
    NetworkTable.setIPAddress('10.5.1.2')
    NetworkTable.setClientMode()
    NetworkTable.initialize()
except:
    if debug == 1:
        print("Unable to initialize NetworkTables, exiting.")
        with open("vision_error.log", "w") as text_file:
            text_file.write("unable to initialize networktables. exited.")

try:
    sd = NetworkTable.getTable("Camera")
except:
    if debug ==1:
        print("unable to load camera table")

cap = cv2.VideoCapture(url) # capture camera, 0 is laptop cam, numbers after that are cameras attached
time.sleep(2)
# Check to make sure cap was initialized in capture
if debug:
    if cap.isOpened():
        print('Capture Initialized.')
    else:
        print('Capture Failed.')

while(cap.isOpened()):
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
