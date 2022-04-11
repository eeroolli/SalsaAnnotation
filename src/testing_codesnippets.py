import os
import pandas as pd
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
