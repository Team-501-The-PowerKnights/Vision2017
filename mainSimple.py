# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 11:52:35 2017

@author: Ithier
"""

import cv2
import time
import sys
import logging

from config import runConfig
from networktables import NetworkTables
import findTargetS as FT

logging.basicConfig(level=logging.DEBUG)

os, camera_location, calibration, freqFramesNT = runConfig()

def main():
    camera_table = nt_init()
    cap = cap_init(camera_location)
    run(cap, camera_table, calibration, freqFramesNT)


def nt_init():
    try:
        init = True
        NetworkTable.setIPAddress('10.5.1.141')
        NetworkTable.setClientMode()
        NetworkTable.initialize()
    except:
        print("Unable to initialize network tables.")
        init = False
    try:
        camera_table = NetworkTable.getTable("Camera")
    except:
        print("unable to get camera networktable")
        init = False
    if not init:
        time.sleep(1)
        print("retrying nt_init().")
        return nt_init()
    else:
        return camera_table


def nt_send(camera_table, Angle, Distance, validCount):
    try:
        camera_table.putNumber('Angle', Angle)
        camera_table.putNumber('ValidCount', validCount)
        camera_table.putNumber('Distance', Distance)
    except:
        print("Unable to send data to networktables.")


def cap_init(camera_location):
    vid_cap = True
    retries = 0
    cap = None
    try:
        cap = cv2.VideoCapture(camera_location)
    except:
        print("unable to start video capture, will retry.")
        vid_cap = False
    while cap.isOpened() and retries < 10:
        print('Cap open successful')
        print('cap.grab(): ' + str(cap.grab()))
        break
    else:
        print('Cap open failed')
        retries += 1
        time.sleep(1)
        vid_cap = False
    if vid_cap:
        return cap
    else:
        print("video capture failed. exiting.")
        sys.exit()


def run(cap, camera_table, calibration, freqFramesNT):
    validCount = 0
    n = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret: # if frame succesfully read
            try:
                Angle, Distance, validUpdate, Processed_frame, mask, cnt = FT.findValids(frame, calibration)
                if validUpdate:
                    validCount += 1
                if n > freqFramesNT:
                    # Send to NetworkTable
                    nt_send(camera_table, Angle, Distance, validCount)
                    n = 0
                else:
                    n += 1
                
            except:
                print('There was an error with findValids')
