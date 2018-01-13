# Vision2017

Camera initialization:
mjpg_streamer -o "output_http.so -w ./www -p 1180" -i "input_uvc.so -d /dev/video0 -f 30 -r 320x240 -n"

Camera Controls:

v4l2-ctrls --set-ctrl exposure_auto=1
turns off auto-exposure

v4l2-ctrls --set-ctrl exposure_absolute=50
sets exposure value to 50 (pretty dark)



