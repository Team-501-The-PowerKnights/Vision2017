# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 11:52:35 2017

@author: Ithier
"""

import cv2
import time
import sys
sys.path.append('/usr/local/lib')
import logging

from config import runConfig
from networktables import NetworkTables
import findTargetS as FT

logging.basicConfig(level=logging.DEBUG)

os, camera_location, calibration, freqFramesNT = runConfig()




def main():
    camera_table = nt_init()
    cap = cap_init(camera_location)
    print(cap.isOpened())
    run(cap, camera_table, calibration, freqFramesNT)


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
    try:
        print("camera location is: " + camera_location)
        cap = cv2.VideoCapture('http://127.0.0.1:1180/?action=stream?dummy=param.mjpeg')
        if cap.isOpened():
            print("Opened")
    except:
        print("Execption on VideoCapture init. Dying")
        sys.exit()
    return cap


def run(cap, camera_table, calibration, freqFramesNT):
    validCount = 0
    n = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret: # if frame succesfully read
            #try:
            Angle, Distance, validUpdate, Processed_frame, mask, cnt = FT.findValids(frame, calibration)
            if validUpdate:
                validCount += 1
            if n > freqFramesNT:
                # Send to NetworkTable
                nt_send(camera_table, Angle, Distance, validCount)
                n = 0
            else:
                n += 1
                
            #except:
            #    print('There was an error with findValids')
    else:
        print('cap is not opened')


if __name__ == "__main__":
    # execute only if run as a script
    main()