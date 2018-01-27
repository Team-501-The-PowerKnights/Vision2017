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

os, camera_location, calibration, freqFramesNT, vertx, verty = runConfig()




def main():
    camera_table = nt_init()
    cap = cap_init(camera_location)
    rect_cnt = create_rect()
    run(cap, camera_table, calibration, freqFramesNT, rect_cnt)


def nt_init():
    #NetworkTables.setIPAddress('10.5.1.141')
    #NetworkTables.setClientMode()
    #NetworkTables.initialize(server='10.5.1.141')
    # port 1735
    try:
        NetworkTables.initialize(server='10.5.1.133')
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
    rectangle = np.zeros((200, 200, 3), np.uint8)
    cv2.rectangle(rectangle, (20, 20), (vertx, verty), (255, 255, 255), -1)
    rectangle = cv2.cvtColor(rectangle, cv2.COLOR_RGB2GRAY)

    ret, thresh = cv2.threshold(rectangle, 127, 255, cv2.THRESH_BINARY)
    img, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, 1)
    cnt = contours[0]
    return cnt


def nt_send(camera_table, Angle, Distance, validCount):
    try:
        camera_table.putNumber('Angle', Angle)
        camera_table.putNumber('ValidCount', validCount)
        camera_table.putNumber('Distance', Distance)
    except:
        print("Unable to send data to networktables.")


def cap_init(camera_location):
    try:
        #print("camera location is:" + camera_location)
        cap = cv2.VideoCapture("http://127.0.0.1:1180/?action=stream?dummy=param.mjpeg")
        time.sleep(2)
    except:
        print("Execption on VideoCapture init. Dying")
        sys.exit()
    return cap


def run(cap, camera_table, calibration, freqFramesNT, rect_cnt):
    validCount = 0
    n = 0
    while(cap.isOpened()):
        before_complete_run=datetime.now()
        before_read = datetime.now()
        ret, frame = cap.read()
        after_read = datetime.now()
        time_to_read = after_read-before_read
        #print("Microseconds to read the capture:", time_to_read.microseconds)
        if ret: # if frame succesfully read
            #try:
                before_run = datetime.now()
                Angle, Distance, validUpdate, Processed_frame, mask, cnt = FT.findValids(frame, calibration, rect_cnt)
                if validUpdate:
                    validCount += 1
                if n > freqFramesNT:
                    # Send to NetworkTable
                    nt_send(camera_table, Angle, Distance, validCount)
                    n = 0
                else:
                    n += 1
                after_run = datetime.now()
                time_to_run = after_run - before_run
                #print("microseconds to run findValids:",time_to_run.microseconds)
                after_complete_run = datetime.now()
                time_to_complete_run = after_complete_run - before_complete_run
                print("microseconds to complete run:", time_to_complete_run.microseconds)
            #except:
             #   print('There was an error with findValids')
    else:
        print('cap is not opened')


if __name__ == "__main__":
    # execute only if run as a script
    main()
