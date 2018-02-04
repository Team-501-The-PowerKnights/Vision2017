# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 11:52:35 2017

@author: Ithier
"""

import cv2
import numpy as np
import time
import sys
sys.path.append('/usr/local/lib')
import logging
from datetime import datetime

from config import runConfig
from networktables import NetworkTables
import findTargetS as FT

logging.basicConfig(level=logging.DEBUG)

os, camera_location, calibration, freqFramesNT, vertx, verty = runConfig(None)




def main():
    camera_table = nt_init()
    cap = cap_init(camera_location)
    rect_cnt = create_rect()
    run(cap, camera_table, calibration, freqFramesNT, rect_cnt)  # main loop contained here. will not return to main.


def nt_init():
    #NetworkTables.setIPAddress('10.5.1.141')
    #NetworkTables.setClientMode()
    #NetworkTables.initialize(server='10.5.1.141')
    # port 1735
    try:
        NetworkTables.initialize(server='10.5.1.193')
        init = True
    except:
        print("Unable to initialize network tables.")
        init = False
    try:
        camera_table = NetworkTables.getTable("Camera")
    except:
        print("unable to get camera networktable")
        NetworkTables.stop()
        NetworkTables.destroy()
        init = False
    if not init:
        time.sleep(1)
        print("retrying networktables initialization.")
        return nt_init()
    else:
        return camera_table

def create_rect():
    """
    Creates a rectangle and performs appropriate processing to provide a target

    returns the contour object of the rectangle
    """
    rectangle = np.zeros((350, 350, 3), np.uint8)
    cv2.rectangle(rectangle, (20, 20), (vertx, verty), (255, 255, 255), -1)
    rectangle = cv2.cvtColor(rectangle, cv2.COLOR_RGB2GRAY)
    ret, thresh = cv2.threshold(rectangle, 127, 255, cv2.THRESH_BINARY)
    img, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, 1)
    cnt = contours[0]
    return cnt


def nt_send(camera_table, Angle, validCount, validUpdate):
    try:
        camera_table.putNumber('Angle', Angle)
        camera_table.putNumber('ValidCount', validCount)
        camera_table.putBoolean('ValidUpdate', validUpdate)
    except:
        print("Unable to send data to networktables. Continuing.")


def cap_init(camera_location):
    try:
        cap = cv2.VideoCapture(eval(camera_location))
        time.sleep(1)
    except:
        print("Exception on VideoCapture init. Dying")
        sys.exit()
    return cap


def run(cap, camera_table, calibration, freqFramesNT, rect_cnt):
    validCount = 0
    n = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret:  # if frame successfully read
            try:
                Angle, Distance, validUpdate, Processed_frame, mask, cnt = FT.findValids(frame, calibration, rect_cnt)
                if validUpdate:
                    validCount += 1
                if n > freqFramesNT:
                    nt_send(camera_table, Angle, validCount, validUpdate)
                    n = 0
                else:
                    n += 1
            except:
                print('There was an error with findValids. Continuing.')
        else:
            print('Unable to read frame. Continuing.')
    else:
        print('Capture is not opened. Ending Program.')


if __name__ == "__main__":
    # execute only if run as a script
    main()
