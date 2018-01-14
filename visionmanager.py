from config import runConfig





def main():
   print("INFO: initializingvision manager")
   os, cameraDevice, red_upper, red_lower, blue_upper, blue_lower, green_upper, green_lower = runConfig()



if __name__ == "__main__":
    # execute only if run as a script
    main()

