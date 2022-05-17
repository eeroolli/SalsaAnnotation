import os
import pandas as pd
import sys
from configparser import ConfigParser, ExtendedInterpolation

cfg = ConfigParser(interpolation=ExtendedInterpolation())
cfg.read('src/config.ini')

running_app_on_streamlit = cfg.getboolean('installation', 'running_app_on_streamlit')
# this script works only with Streamlit
assert running_app_on_streamlit == True

running_app_locally = cfg.getboolean('installation', 'running_app_locally')

if running_app_on_streamlit==True and running_app_locally==False:
    cfg.read('deployment/config_streamlit.ini')
  
parent_path = cfg.get('installation', 'parent_path')
root_path = cfg.get('installation', 'root_path')
script_path = cfg.get('installation', 'script_path')


print(root_path)
print(script_path)

# from Inference2 import enc_label, check_pred, transf_data


# from datetime import datetime


# def clean(string):
#     import re
#     clean_string = string.replace("/", "-").replace(" ", "_") 
#     clean_string = re.sub("""[/{/}!();:'/" \,<>?@#$%^&*~]""", "", clean_string)
#     clean_string = clean_string.strip()
#     clean_string = clean_string.lstrip("_") #starting a name with _ leads to funny names in Markdown
#     return clean_string

# coreo = "_First"
# video_background = "Black"
# dance_role = "Leader/Male"
# salsa_style = "NY/On2"
# uploaded_filename = "Testing_Up }load_to_s3.mp4"

# from datetime import datetime
# now = datetime.now().strftime("%Y%m%d%H%M")
# print(now)

# success_text = f"You have just successfully uploaded {uploaded_filename}, which will be renamed to:" 
# print(success_text)

# changing_video_name = clean(f"{coreo}_{video_background}_{dance_role}_{salsa_style}_{uploaded_filename}")
# print(changing_video_name)

def keep_only_words(messy_string):
    import re
    # keep only words, dash and white space
    clean_string = re.sub(r'\[|\]', '', messy_string)
    clean_string = re.sub(r'\W', ' ', clean_string)
    clean_string = re.sub(r'\s+', ' ', clean_string)
    clean_string = re.sub(r'^\s|\s$', '', clean_string)
    return clean_string

def make_list_from_string(string):
    new_list = keep_only_words(string).split(sep=" ")
    return new_list

import re
ch = cfg.get('annotation', 'coreo')
ch = re.sub(r'\[|\]|\"|\'', '', ch)
ch = re.sub(r'^\s|\s$', '', ch).split(sep=",")
print(ch)
choreography = []
for item in ch:
    choreography = choreography + [item, item] 
print(choreography)



from configparser import ConfigParser, ExtendedInterpolation
cfg = ConfigParser(interpolation=ExtendedInterpolation())
cfg.read('src/config.ini')
cfg.get('openpose', 'default_fps')


# Input arguments
EXECUTION_ARGUMENTS_N = len(sys.argv)-1
print(f"The number of arguments given is {EXECUTION_ARGUMENTS_N}" )
if EXECUTION_ARGUMENTS_N == 4:
  video_id = sys.argv[1]



def cut_video(input_video, output_video, start_mmss, duration_s):
  import subprocess
  # cut the parts of video that we cannot use
  subprocess.check_output("ffmpeg -y -loglevel info -i $input_video -ss $start_mmss -t $duration $output_video")
  return output_video


# from VideoProcessing import get_video_fps
def get_video_fps(video):
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

print(os.getcwd())
# "output_op_1p/1p_ThomasW_girl_right/openpose.mp4"
video = "/home/eero_ds/SalsaAnnotation/output_op_1p/1p_ThomasW_girl_right/openpose.mp4"
frames_per_s = get_video_fps(video)

print(frames_per_s)

