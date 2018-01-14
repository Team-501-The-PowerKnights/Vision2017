from config import runConfig


def main():
    print("INFO: initializingvision manager")
    os, cameraDevice, calibration, freqFrameNT = runConfig()
    print(os, cameraDevice, calibration, freqFrameNT)


if __name__ == "__main__":
    # execute only if run as a script
    main()

