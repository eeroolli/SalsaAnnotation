"""
Make the manual annotation of the video, to get the start and end of each figure
run this file from Repo root with command 
$ python ./src/Click_Frame2.py

"""
import cv2
import pandas as pd
import os
import time

# from global_ import video_id, PATH_OUTPUT, video_size, sample

from configparser import ConfigParser, ExtendedInterpolation
cfg = ConfigParser(interpolation=ExtendedInterpolation())
cfg.read('src/config.ini')
wait_ms = 30

ROOT_DIR = cfg.get('installation', 'root_path')

# We could use the openpose.mp4 stickfigure, but it is difficult to be precise.
# The manual annotation is more precise using the non-stickfigure video.
video_size =cfg.get('resize_video', 'video_size') 
video_id = cfg.get("click_frame", 'video_id')
video_name = video_id + "_" + video_size + ".mp4"
input_video_resized_dir = cfg.get('click_frame', 'input_video_resized_dir')
VIDEO_FILE = os.path.join(input_video_resized_dir, video_name)

if os.path.isfile(VIDEO_FILE): 
    print("Input video is OK.")
else:
    print(f"Can't find {VIDEO_FILE}")


file_name = cfg.get('output_data', 'click_data')
#PATH_OUTPUT = os.path.join(input_video_resized_dir, video_id)
PATH_OUTPUT = cfg.get('click_frame', 'output_dir')

PATH_ANNOT = os.path.join(PATH_OUTPUT, file_name)

# Functions to get the state of the mouse
def print_frame(event, x, y, flags, *userdata):
    if event == cv2.EVENT_LBUTTONDOWN:
        time_list.append(cap.get(cv2.CAP_PROP_POS_MSEC))
        frame_list.append(cap.get(cv2.CAP_PROP_POS_FRAMES))

print("  Now you need to manually click on the image of the dancer to")
print("  mark where the choreography STARTS, every 1 beat (of 123-567-),")
print("  and where each repetition of choreography ends. Eleven clicks ")
print("  for a choreography, turn, new eleven clicks and so fort.")
time.sleep(4)
print("  Grab your mouse and get ready.")
print("  press q to quit. ")

time.sleep(1)



# Extracting the frames of a video to feed MediaPipe
cap = cv2.VideoCapture(VIDEO_FILE)
time_list = []
frame_list = []

while (cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('frame', gray)
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

# Check if the number of clicks is correct for the choreography.
#TODO: this should be a function of the choregraphy used and not a fixed number.
correct_number_of_clicks = 11
# sometimes we use videos with only one repetition of the choreography - like vier from left.
# therefore the correct number is not always multiplied by 4.
if len(data_annot) % correct_number_of_clicks == 0:
    print("number of clicks seems correct")
    data_annot.to_csv(PATH_ANNOT, index=False)   #overwrites existing csv file.
else:
    print(f"You did {len(data_annot)} clicks. The number should be divisible by {correct_number_of_clicks}")
    print("your results are not saved. Please rerun the script for this file.") 
# os.makedirs(PATH_OUTPUT)








