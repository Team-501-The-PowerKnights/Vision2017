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
      mask = config['mask']['mask']
      mask = mask.split(",")
   except:
      print("ERROR: config.ini does not contain correct parameters. see ./config.py ")
      sys.exit(1)

   if not os:
      print("INFO: os configuration not present")
   if not camera:
      print("ERROR: camera configuration not present")
      die=1
   sacrificial = None
   try:
      sacrificial=mask[2]
   except IndexError:
      print("ERROR: mask configuration incomplete")
      die=1
   if not sacrificial:
      die=1

   if die > 0:
      print("FATAL ERROR: unable to load vision configuration. Exiting.")
      sys.exit(1) 

   return os, camera, mask


