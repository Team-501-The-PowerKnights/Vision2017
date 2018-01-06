# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 11:52:35 2017

@author: Ithier
"""

import findTargetS as FT
import cv2

directory = 'C:/Users/Ithier/Documents/FIRST/2017/Off Season/'

filename = directory + 'imageValues.npz' #folder npz file is in
pic = 'target.png'

picture = directory + pic
debug = 1
#############################################################################
    
# Create resizable window for camera 
cv2.namedWindow('Camera Frame', cv2.WINDOW_NORMAL)
img = cv2.imread(picture)
# Process image
Angle, Distance, validUpdate, Processed_frame, mask, cnt = FT.findValids(img, filename, debug)
try:
    cv2.drawContours(picture, [cnt[0]], 0, (0,0,255), 2)
except:
    print("No valid contours")

try:
    cv2.drawContours(picture, [cnt[1]], 0, (255,0,255), 2)
except:
    print("No second valid contour")
    
    # Display the resulting frame
cv2.imshow('Camera Frame', Processed_frame)
cv2.imshow('Mask', mask)
    
if cv2.waitKey(0) & 0xFF == ord('q'):
    cv2.destroyAllWindows()
