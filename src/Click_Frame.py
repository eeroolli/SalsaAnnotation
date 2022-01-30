"""
Make the manual annotation of the video, to get star and end of a figure
"""
import cv2
import pandas as pd
import os
import sys
sys.path.append('../')
import config # Make sure that this config is not in conflict with config.ini

from configparser import ConfigParser, ExtendedInterpolation
cfg = ConfigParser(interpolation=ExtendedInterpolation())
cfg.read('config.ini')

output_dir = cfg.get('folders', 'output_dir')  # Can we declare this variable only once?
input_dir = cfg.get('folders', 'input_dir')

PATH_OUTPUT = output_dir
video_id = config.VIDEO_ID
video_name = video_id + ".mp4"
FILE = os.path.join(input_dir, video_name)
PATH_ANNOT = os.path.join(output_dir, "Data_steps.csv")
wait_ms = 30

# Functions to get the state of the mouse
def print_frame(event, x, y, flags, *userdata):
    if event == cv2.EVENT_LBUTTONDOWN:
        time_list.append(cap.get(cv2.CAP_PROP_POS_MSEC))
        frame_list.append(cap.get(cv2.CAP_PROP_POS_FRAMES))

# Extracting the frames of a video to feed MediaPipe
cap = cv2.VideoCapture(FILE)
time_list = []
frame_list = []

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('frame',gray)
        cv2.setMouseCallback("frame", print_frame)

        if cv2.waitKey(wait_ms) & 0xFF == ord('q'):
            break
    else:
        break
cap.release()
cv2.destroyAllWindows()

time_list = [round(x, 2) for x in time_list]
data_annot = pd.DataFrame(
    {"Time_ms": time_list,
     "Frame": frame_list}
)

data_annot.to_csv(PATH_ANNOT, index=False)


