"""
Run this file from repo root
python ./src/run_video_prosessing.py

It is necessary to run Click_frame2.py before this script.
"""
# libraries needed from outside
import os
from os import mkdir
from os.path import exists, join, basename, splitext
import sys
import glob                       # help for finding files
from re import split              # regular expression string splitter
import subprocess                # subprocess wraps around regular os commands
from utils import check_path, stop_if_no_path 

from configparser import ConfigParser, ExtendedInterpolation
cfg = ConfigParser(interpolation=ExtendedInterpolation())

cfg.read('src/config.ini')
print('config.ini has these sections:', cfg.sections(), "\n")

if cfg.getboolean('installation', 'running_app_on_colab'):
    from google.colab import drive
    drive.mount('/content/gdrive')

    if os.path.isdir('/content/gdrive/MyDrive'):    
        google_drive_path = cfg.get('folders','google_drive_path')
    else:
        print("There is a problem google_drive_path.")
    
    script_path = os.path.join(
        google_drive_path, "2021-DSR-Porfolio", "python_scripts")
    root_path = os.path.join(google_drive_path,  "DanceApp")
    
if cfg.getboolean('installation', 'running_app_locally'):
    parent_path = cfg.get('installation', 'parent_path')
    root_path = cfg.get('installation', 'root_path')
    script_path = cfg.get('installation', 'script_path')


print("Using ", root_path, " as root_path")
here = os.getcwd()
print(here)
print("Using ", script_path, " as script_path")

# this might not be necessary as one can also use .. and deal with paths during import.
if not script_path in sys.path:  # otherwise will add anew with every run of script.
    sys.path.append(script_path)
    print("Added script_path to search path.")
    print("sys.path is now: ", sys.path)

output_dir = cfg.get('folders', 'output_dir') 
output_main = os.path.join(root_path, output_dir)
if not os.path.isdir(output_main):
    os.makedirs(output_main, exist_ok=True)


video_list = ["1p_ThomasW_girl_right.mp4",
"1p_ThomasW_girl_left.mp4",
"1p_ThomasW_girl_front.mp4",
"1p_ThomasW_girl_back.mp4",]


for i in range(len(video_list)):
  print("\n ################################ ")
  print(" ################################ \n")
  clip_name = video_list[i]
  video_id = splitext(video_list[i])[0]
  print(f"video_id is {video_id}")
  print("+++++++++++++++++++++++++++++++++++++++")
  output_op_dir = os.path.join(output_main, video_id)
  if not os.path.isdir(output_op_dir):
    os.makedirs(output_op_dir, exist_ok=True)
  
  print("\n ################################ \n")
  # Creating the annotation file
  subprocess.run(["python", "src/AnnotationFile2.py", output_op_dir])
  
  print("\n ################################ \n")
  # Parsing JSON and adding information from annotation
  Anot_file = output_op_dir + "/Annotation.json"
  subprocess.run(["python", "src/Parsing-Openpose-Annotation2.py", video_id, output_op_dir, output_op_dir, Anot_file])

  print("\n ################################ \n")
  # reduce jitter and normalize the data
  #!cp $script_path/Data_preparation2.py .
  subprocess.run(["python", "src/Data_preparation2.py", video_id, output_op_dir])
  
