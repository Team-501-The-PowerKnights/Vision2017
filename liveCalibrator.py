import cv2
import numpy as np
from config import runConfig



def nothing(x):
    pass


def init_capture():
    try:
        cap = cv2.VideoCapture('http://localhost:1180/?action=stream?dummy=param.mjpg')
        return cap
    except:
        print('capture failed.')


def init_window(calibration):

    hl, sl, vl = calibration['green']['green_lower']
    hh, sh, vh = calibration['green']['green_upper']

    # Create a black image, a window
    cv2.namedWindow('image')

    # create trackbars for color change
    cv2.createTrackbar('H_low', 'image', 0, 255, nothing)
    cv2.createTrackbar('H_high', 'image', 0, 255, nothing)
    cv2.createTrackbar('S_low', 'image', 0, 255, nothing)
    cv2.createTrackbar('S_high', 'image', 0, 255, nothing)
    cv2.createTrackbar('V_low', 'image', 0, 255, nothing)
    cv2.createTrackbar('V_high', 'image', 0, 255, nothing)

    # set trackbars to values in the calibration file so we're close
    cv2.setTrackbarPos('H_low', 'image', hl)
    cv2.setTrackbarPos('S_low', 'image', sl)
    cv2.setTrackbarPos('V_low', 'image', vl)
    cv2.setTrackbarPos('H_high', 'image', hh)
    cv2.setTrackbarPos('S_high', 'image', sh)
    cv2.setTrackbarPos('V_high', 'image', vh)

    # create switch for ON/OFF functionality
    switch = '0 : OFF \n1 : ON'
    cv2.createTrackbar(switch, 'image',0,1,nothing)

    return switch


def main():
    _, _, calibration, _, _, _ = runConfig()
    cap = init_capture()
    switch = init_window(calibration)
    run(cap, switch)


def run(cap, switch):

    while True:
        img = None
        try:
            if cap.isOpened():
                _, img = cap.read()
                hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            else:
                print('cannot open capture')
        except:
            print('capture read exception')

        # get current positions of four trackbars
        hl = cv2.getTrackbarPos('H_low','image')
        hh = cv2.getTrackbarPos('H_high','image')
        sl = cv2.getTrackbarPos('S_low', 'image')
        sh = cv2.getTrackbarPos('S_high', 'image')
        vl = cv2.getTrackbarPos('V_low','image')
        vh = cv2.getTrackbarPos('V_high','image')
        lower_bound = np.array([hl, sl, vl])
        upper_bound = np.array([hh, sh, vh])

        s = cv2.getTrackbarPos(switch,'image')
        if s == 0:
            pass
        else:
            img = cv2.inRange(hsv,lower_bound,upper_bound)
        # print("img is", img)
        cv2.imshow('image', img)
        k = cv2.waitKey(15) & 0xFF
        if k == 27:
            break
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # execute only if run as a script
    main()