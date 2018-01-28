import cv2
import numpy as np
from config import runConfig
import sys
import manipulateImageS as MI


def main():

    if len(sys.argv) < 2:
        print("Filename required")
        sys.exit()
    _, _, calibration, _, _, _ = runConfig()
    lower_bound = np.array(calibration["green"]["green_lower"])
    upper_bound = np.array(calibration["green"]["green_upper"])

    img_orig = cv2.imread(sys.argv[1])
    img = img_orig
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask_orig = cv2.inRange(hsv, lower_bound, upper_bound)
    mask = np.copy(mask_orig)

    mask_eroded_dilated = MI.dilateAndErode(mask, 5)
    mask = np.copy(mask_eroded_dilated)
    ret, mask_threshold = cv2.threshold(mask, 127, 255, 0)

    cv2.imwrite('generator_original_frame.png', img_orig)
    cv2.imwrite('generator_original_mask.png', mask_orig)
    cv2.imwrite('generator_mask_eroded_dilated.png', mask_eroded_dilated)
    cv2.imwrite('generator_mask_threshold.png', mask_threshold)


if __name__ == "__main__":

    main()
