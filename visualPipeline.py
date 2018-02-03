from config import runConfig
import cv2
import numpy as np
import manipulateImageS as MI
import sys


"""
Standalone demo for vision processing

reads frame from mjpeg-streamer

displays:
    original
    mask
    original with mask outline
    original with line, telemetry
"""


class Configuration:
    def __init__(self):
        self.os = None
        self.camera = None
        self.calibration = None
        self.freqFrameNT = None
        self.vertx = None
        self.verty = None
        self.os, self.camera, self.calibration, self.freqFrameNT, self.vertx, self.verty = runConfig()

    def get_configuration(self, config_item):
        item = getattr(self, config_item, None)  # should be noted that getattr() only works for obj.attr and no further
        return item


class Display:
    def __init__(self):
        self.image_original = None
        self.image_hsv = None
        self.mask = None
        self.mask_dil_ero = None
        self.mask_threshold = None

    def create_display(self):
        cv2.namedWindow('original')
        cv2.namedWindow('hsv')
        cv2.namedWindow('mask')
        cv2.namedWindow('mask_dil_ero')
        cv2.namedWindow('mask_threshold')
        cv2.waitKey(0)












def main():
    config = Configuration()

    capture = acquire_capture(config)
    image, ret = acquire_image(capture)
    image_operations(image, config)


def image_operations(img_orig,config):
    img = np.copy(img_orig)  # HERE
    lower_bound = np.array(config.calibration["green"]["green_lower"])
    upper_bound = np.array(config.calibration["green"]["green_upper"])
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # HERE
    mask_orig = cv2.inRange(hsv, lower_bound, upper_bound)
    mask = np.copy(mask_orig)  # HERE
    mask_eroded_dilated = MI.dilateAndErode(mask, 5)
    mask = np.copy(mask_eroded_dilated)  # HERE
    ret, mask_threshold = cv2.threshold(mask, 127, 255, 0)
    mask = np.copy(mask_threshold)  # HERE


def acquire_capture(config):
    try:
        capture = cv2.videoCapture(config.camera)
    except:
        print("ERROR: Unable to open capture. Exiting.")
        sys.exit()
    return capture


def acquire_image(capture):
    image = None
    if capture.isOpened():
        ret, image = capture.read()
        if ret:
            return image
        else:
            print("WARNING: Capture read failed.")
    else:
        print("ERROR: Capture not opened.")
    return image, ret

if __name__ == '__main__':
    main()
