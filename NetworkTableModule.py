# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 13:21:14 2017

@author: Ithier
"""

def sendValues(sd, Angle, Distance, validCount):
    sd.putNumber('Angle', Angle)
    sd.putNumber('ValidCount', validCount)
    sd.putNumber('Distance', Distance)