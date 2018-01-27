# Vision2017

Camera initialization:
mjpg_streamer -o "output_http.so -w ./www -p 1180" -i "input_uvc.so -d /dev/video0 -f 30 -r 320x240 -n"

Camera Controls:

v4l2-ctl --set-ctrl exposure_auto=1

turns off auto-exposure

v4l2-ctl --set-ctrl exposure_absolute=15

sets exposure value to 15 (very dark)

v4l2-ctl --set-ctrl white_balance_temperature_auto=0

v4l2-ctl --set-ctrl white_balance_temperature=5280


CV2 MUST SEE A .MJPG EXTENSION A LA:

http://localhost:1180/?action=stream?dummy=param.mjpg




