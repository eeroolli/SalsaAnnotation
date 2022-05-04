"""
Make the manual annotation of the video, to get the start and end of each figure
run this file from Repo root with command 
$ python ./src/Click_Frame2.py

"""
import os

# from global_ import video_id, PATH_OUTPUT, video_size, sample

from configparser import ConfigParser, ExtendedInterpolation
from utils import manual_click_frame, check_path, get_choreography

cfg = ConfigParser(interpolation=ExtendedInterpolation())
cfg.read('src/config.ini')
wait_ms = 40

ROOT_DIR = cfg.get('installation', 'root_path')

# We could use the openpose.mp4 stickfigure, but it is difficult to be precise.
# The manual annotation is more precise using the non-stickfigure video.
#TODO: Add a option to give the file name as 
video_size =cfg.get('resize_video', 'video_size') 
video_id = cfg.get("click_frame", 'video_id')
video_name = video_id + "_" + video_size + ".mp4"
input_video_resized_dir = cfg.get('click_frame', 'input_video_resized_dir')
VIDEO_FILE = os.path.join(input_video_resized_dir, video_name)

#TODO: make a list of videos in the folder and compare it with the list of csv files
#TODO: show only those files that are still missign a csv file.

if os.path.isfile(VIDEO_FILE): 
    print("Input video is OK.")
else:
    print(f"Can't find {VIDEO_FILE}")

choreo = ""
choreo = get_choreography("coreo")
print(choreo)
number_of_clicks_per_choreo = len(choreo)+1
print(f"\n  Based on the choreo saved in config.ini")
print(f"  the correct number of clicks per choreo is {number_of_clicks_per_choreo}.")


file_name = cfg.get('output_data', 'click_data')
#PATH_OUTPUT = os.path.join(input_video_resized_dir, video_id)
PATH_OUTPUT = cfg.get('click_frame', 'output_dir')
PATH_ANNOT = os.path.join(PATH_OUTPUT, file_name)

############################### 


manual_click_frame(VIDEO_FILE = VIDEO_FILE,
                   OUTPUT_CSV_FILE= PATH_ANNOT,
                   video_id = video_id)







