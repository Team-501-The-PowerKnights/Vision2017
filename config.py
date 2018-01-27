import sys
import configparser
config = configparser.ConfigParser()


def runConfig():
   """
   reads a  configuration file (config.ini) in standard format.
   [header]
   config_item  = value

   quotations are not required.
   """
   die=0
   print("INFO: reading configuration from config.ini")
   try:
      config.read('config.ini')
   except:
      print("ERROR: Unable to read config.ini Dying.")
      sys.exit(1)
   try:
      os = config['os']['operatingSystem']
      camera = config['camera']['cameraDevice']
      red_upper = config['mask']['red_upper']
      red_upper = red_upper.split(",")
      red_lower = config['mask']['red_lower']
      red_lower = red_lower.split(",")
      blue_upper = config['mask']['blue_upper']
      blue_upper = blue_upper.split(",")
      blue_lower = config['mask']['blue_lower']
      blue_lower = blue_lower.split(",")
      green_upper = config['mask']['green_upper']
      green_upper = list(map(int, green_upper.split(',')))
      green_lower = config['mask']['green_lower']
      green_lower = list(map(int, green_lower.split(',')))
      freqFrameNT = config['framerate']['freqFrameNT']
   except:
      print("ERROR: config.ini does not contain correct parameters. see ./config.correct ")
      sys.exit(1)

   if not os:
      print("INFO: os configuration not present")
   if not camera:
      print("ERROR: camera configuration not present")
      die=1
   sacrificial = None
   try:
      sacrificial=red_upper[2]
      sacrificial=red_lower[2]
      sacrificial=blue_upper[2]
      sacrificial=blue_lower[2]
      sacrificial=green_upper[2]
      sacrificial=green_lower[2]
   except IndexError:
      print("ERROR: calibration configuration incomplete")
      die=1
   if not sacrificial:
      die=1
   if not freqFrameNT:
      print("INFO: framerate not specified, using default of 10.")
      freqFrameNT = 10
   if die > 0:
      print("FATAL ERROR: unable to load vision configuration. Exiting.")
      sys.exit(1) 

   red = {"red_upper":red_upper, "red_lower":red_lower }
   blue = {"blue_upper":blue_upper, "blue_lower":blue_lower }
   green = {"green_upper":green_upper, "green_lower":green_lower }
   calibration = {"red":red, "blue":blue, "green":green}

   return os, camera, calibration, freqFrameNT