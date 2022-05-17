
# This file contains functions used for videoprocessing
import os
# from os import mkdir   # using os.makedirs instead because it can create the whole path.
from os.path import exists, join, basename, splitext
import sys
import glob                       # help for finding files
from re import split              # regular expression string splitter
import subprocess  # subprocess wraps around regular os commands
import shutil                     # used for copying files in the os.
import utils

from configparser import ConfigParser, ExtendedInterpolation
cfg = ConfigParser(interpolation=ExtendedInterpolation())
cfg.read('config.ini')
cfg.read('src/config.ini')
if cfg.getboolean('installation', 'running_app_on_streamlit'):
  cfg.read('deployment/config_streamlit.ini')

def cut_video(input_video, output_video, start_mmss, duration_s):
  import subprocess
  # cut the parts of video that we cannot use
  subprocess.check_output(["ffmpeg", "-y -loglevel info -i", input_video, "-ss", start_mmss, "-t", duration_s, output_video])
  return output_video

def resize_video(new_height, video_in, clip_name, src_folder):
    video_name, video_ext = splitext(clip_name)
    print("\n ################################ \n")
    print("#     Resizing the video:     ")
    print("clip_name: ", clip_name)
    print("video_name: ", video_name, " extention: ", video_ext)
    
    if os.path.isfile(video_in):
      print("Found the input video_in")
    else:
      print("The input video does not exist.")
      # raise Exception("No input video file")

    print("new hight will be: ", new_height)
    root_path = cfg.get('installation', 'root_path')
    
    if cfg.getboolean('installation', 'running_app_on_colab'):
      resize_output_dir = os.path.join(root_path, src_folder ,"h" + str(new_height)) # in colab mass production
    if cfg.getboolean('installation', 'running_app_locally'):
      # in deployd version use one folder per video_id
      resize_output_dir = cfg.get('folders', 'output_dir')
    if cfg.getboolean('installation', 'running_app_on_streamlit'):
      #TODO: is it better with separate folder for each nickname?
      resize_output_dir = cfg.get('folders', 'output_dir')
         
    video_out = resize_output_dir + "/" + video_name + "_h" + str(new_height) + video_ext
    print("the output video will be: ", video_out)

    if not os.path.isdir(resize_output_dir):
      os.makedirs(resize_output_dir)
      print("Created a folder for resized video output:", src_folder, "/h",str(new_height) )
    else:
      print("Folder for resized video output:", src_folder, "/h",str(new_height) )
    
    if os.path.isfile(video_out):
      print("The video has been resized previously")
    else:
      print("The video is being resized, which takes often several minutes.")
      os.system("ffmpeg -i "+video_in+" -vf scale=-2:"+new_height+" -c:a copy "+video_out)    # the -2 ensures that width is a even number as required
                                                                                              # -c:a copy  copies the sound file. 
    return video_out



def get_video_fps(video, video_id):
  # Check for the speed of the video
  import os
  import subprocess
  from configparser import ConfigParser, ExtendedInterpolation
  
  cfg= ConfigParser(interpolation=ExtendedInterpolation())
  cfg.read('src/config.ini')
  default_fps = cfg.get('openpose', 'default_fps')
  print(f"The default_fps is {default_fps}")
  frames_per_s = default_fps            # if everything fails there is a default value
  
  if not os.path.isfile(video):
    print("There video is missing: \n ", video)
  else:
    print(f"ffprobe is checking fps in {video}")

  print(os.getcwd())
  command = f"/usr/bin/ffprobe -v 0 -of csv=p=0 -select_streams v:0 -show_entries stream=r_frame_rate {video}"
  print(command)
  text = subprocess.getoutput(command)
  print(f"The ffprobe r_frame_rate is {text}")
  frames, seconds = text.split("/")
#   frames, seconds = text[0].split("/", 2)
  frames_per_s = round(int(frames)/int(seconds), ndigits=2) 
  return frames_per_s

def load_video_run_openpose(video, video_id):
  #requires that video_id and connected variables are set.
  from configparser import ConfigParser, ExtendedInterpolation
  cfg = ConfigParser(interpolation=ExtendedInterpolation())
  #cfg.read('config.ini')
  cfg.read('src/config.ini')
  #print('config.ini has these sections:', cfg.sections(), "\n")   
  print("\n ################################ \n")
  print("#     Run OpenPose:     ")
  # # Check for the speed of the video
  # # if everything fails there is a default value
  # default_fps = cfg.getint('openpose', 'default_fps')
  
  if not os.path.isfile(video):
    print("There video is missing: \n ", video)
  else:
    print(f"The Video input to Openpose is: \n {video}") 

  # print(f"Working directory is: {os.getcwd()}")
  
  # # cut the parts of video that we cannot use
  # !ffmpeg -y -loglevel info -i "input_original/youtube.mp4" -ss $start_mmss -t $duration "input_original/video.mp4"
  
  # detect poses
  output_op_dir = cfg.get('folders', 'output_dir')
  op_video = output_op_dir + "/openpose.avi"
  op_json = output_op_dir + "/" + video_id + "/json"  # video_id is a global variable calculated in a loop.

  if not os.path.exists(op_json): 
    os.makedirs(op_json)

  skeleton_on_black_background = cfg.getboolean('openpose', 'skeleton_on_black_background')
  print(f"Skeleton on black ground is: {skeleton_on_black_background}")
  print(" ")  
  if skeleton_on_black_background==True: 
    os.system("cd openpose && ./build/examples/openpose/openpose.bin --video "+video+" --write_json --number_people_max 1 "+op_json+" --display 0 --disable_blending  --write_video "+op_video)
  elif skeleton_on_black_background==False: 
    os.system("cd openpose && ./build/examples/openpose/openpose.bin --video "+video+" --write_json --number_people_max 1 "+op_json+" --display 0  --write_video "+op_video)
  else:
    raise Exception("You need to set the variable skeleton_on_black_background") 

  
  # convert the result into MP4
  print(" ")
  print("============================== ")
  print("Converting the stickfigure video to mp4 ")
  print(" ")

  op_video_mp4 = output_op_dir + "/openpose.mp4"

  if os.path.isfile(op_video): 
    os.system("ffmpeg -y -loglevel info -i "+op_video+" "+op_video_mp4) #convert avi til mp4
    os.remove(op_video)  # remove avi
  else:
    print("Something went wrong, as there was no output video from Openpose.")
    print("the output_op_dir contains:")
    print(os.listdir(output_op_dir))

  print(" ")
  print("Creating single frame images ")
  print("============================== ")
  print(" ")


def delete_outputs(video_id, root_path, output_dir):
    # delete output_files from Openpose if they were already created
    print("\n ################################ \n")
    print("Deleting old output files from the ", output_dir, video_id, " folder")
    # create a list of files to delete
    delete_files = glob.glob(os.path.join(root_path, output_dir, video_id, "json", "*.json"))
    delete_files.extend(glob.glob(os.path.join(root_path, output_dir, video_id, "*.mp4")))
    delete_files.extend(glob.glob(os.path.join(root_path, output_dir, video_id, "*.MOV")))
    # delete_files.extend(glob.glob(os.path.join(root_path, "output_op", clip_name, "*.avi")))
    # print("avi: ", delete_files[-1:])
    [os.remove(x) for x in delete_files]

    print("\n Now the output folder contains only these files:")
    print(glob.glob(os.path.join(root_path, output_dir, video_id, "json", "*.json")))


def rename_json(video_id, root_path, output_dir):
    print("\n ################################ \n")
    print("#     Rename JSON files:     ")
    ## Better names for JSON
    # find all json files and change the name
    # os.chdir(original_working_dir)
    print(os.getcwd())
    paths_json = glob.glob(os.path.join(root_path, output_dir, video_id, "json", "*.json"))
    paths_json = sorted(paths_json, reverse=True)

    print("there are ", len(paths_json), " json files to rename")
    if len(paths_json)>0:
      for old_file in paths_json:
          frame_number = old_file[-21:-15]  # counting backwards is safest, because folder names change
          # print(f"Frame {frame_number}")
          # print(f"Old name {old_file}")
          new_file_name = os.path.join(root_path, output_dir, video_id, "json") + "/frame-" + frame_number + ".json"
          # print(f"New name {new_file_name}")
          os.rename(old_file, new_file_name)

      print(" ")
      print("All json are now renamed.")
    else:
      print("nothing to be done.")  
    print("============================== ")

    # delete old names
    # [os.remove(x) for x in paths_json]
    print(" ")
    
def play_video_in_colab(video_show):
  #video_show should be a full path.
  # this only plays compressed files!
  from IPython.display import HTML
  from base64 import b64encode
  if os.path.isfile(video_show):
      print("The videofile to be shown does exist.")
      print("Note that this player is not able to play large uncompressed videos.")
  else:
      print("The videofile to be shown does NOT exist.")

  mp4 = open(video_show,'rb').read()
  data_url = "data:video/mp4;base64," + b64encode(mp4).decode()
  HTML("""
  <video width=300 controls>
        <source src="%s" type="video/mp4">
  </video>
  """ % data_url)

