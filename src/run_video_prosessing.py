# libraries needed from outside
import os
from os import mkdir
from os.path import exists, join, basename, splitext
import sys
import glob                       # help for finding files
from re import split              # regular expression string splitter
import subprocess  # subprocess wraps around regular os commands
import shutil                     # used for copying files in the os.
from VideoProcessing import check_path, stop_if_no_path 
# check also load_video_run_openpose(), which still has some bugs.
from VideoProcessing import load_video_run_openpose
from VideoProcessing import resize_video, delete_outputs, rename_json  
from configparser import ConfigParser, ExtendedInterpolation
cfg = ConfigParser(interpolation=ExtendedInterpolation())
cfg.read('config.ini')
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
input_dir = cfg.get('folders', 'input_dir')
input_video_fullsize_dir = cfg.get('folders', 'input_video_fullsize_dir')
input_video_resized_dir = cfg.get('folders', 'input_video_resized_dir')

check_path(input_video_fullsize_dir)
check_path(input_video_resized_dir)



### Variables that are calculated from other variables.
video_size = cfg.get('resize_video', 'video_size')
new_height = "".join([chr for chr in video_size if chr.isdigit()])  # used to resize


#fourth list of videos
video_list = ["1p_ThomasW_16012022_choreo1.mp4"]
# "1p_Daniele_16012022_choreo1.mp4",
# "1p_20211216_Francesca_Zeni.mp4",
# "1p_ThomasW_girl_16012022_choreo1.mp4",

if running_app_on_streamlit==True: 
  video_list = [uploaded_video_name]
  
print("\n ################################ \n")

for i in range(len(video_list)):
  clip_name = video_list[i]
  video_id = splitext(video_list[i])[0]
  video_in = os.path.join(input_video_fullsize_dir, clip_name)
  video_name, video_ext = splitext(video_in)
  video_resized = input_video_resized_dir + "/" + \
      video_id + '_' + video_size + video_ext
  print("video fullsize: ", video_in)
  print("video_resized: ", video_resized)
  print(video_ext)

  # Video Processing and OpenPose
  #from pathlib import Path as P
  output_main = os.path.join(root_path, output_dir)
  if not os.path.isdir(output_main):
    os.makedirs(output_main, exist_ok=True)

  output_op_dir = os.path.join(output_main, video_id)
  if not os.path.isdir(output_op_dir):
    os.makedirs(output_op_dir, exist_ok=True)

  print("Processing video", clip_name)

  video_resized = resize_video(new_height=new_height,
                               video_in=video_in,
                               clip_name=clip_name,
                               src_folder=input_dir)

  
  if cfg.getboolean('openpose', 'run_openpose') == True:
    delete_outputs(video_id=video_id, root_path=root_path,
                     output_dir=output_dir)
  
    load_video_run_openpose(video=video_resized)
  
  rename_json(video_id, root_path=root_path, output_dir=output_dir)

  # Creating the annotation file
  # TODO: make os independent. use shutil.copy(src, dst) and os.path()
  # !cp $script_path/AnnotationFile.py .
  # !python AnnotationFile.py $output_op_dir

  # Parsing JSON and adding information from annotation
  # Anot_file = output_op_dir + "/Annotation.json"
  # !cp $script_path/Parsing-Openpose-Annotation.py .
  # !python Parsing-Openpose-Annotation.py $video_id $output_op_dir $Anot_file
