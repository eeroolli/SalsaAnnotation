# from functools import cache
import streamlit as st
import pandas as pd
# from Inference import *
import boto3
import os
import sys
from datetime import datetime
import validators
# import matplotlib.pyplot as plt
# import seaborn as sns
# sns.set_theme(style="darkgrid")
# sns.set()
from PIL import Image

from configparser import ConfigParser, ExtendedInterpolation

cfg = ConfigParser(interpolation=ExtendedInterpolation())
cfg.read('src/config.ini')
cfg.read('deployment/config_streamlit.ini')
st.write(f"config.ini has these sections:, {cfg.sections()} \n")

running_app_on_streamlit = cfg.getboolean('installation', 'running_app_on_streamlit')
   
if running_app_on_streamlit:
    parent_path = cfg.get('installation', 'parent_path')
    root_path = cfg.get('installation', 'root_path')
    script_path = cfg.get('installation', 'script_path')

st.write(f"Using {root_path} as root_path")
st.write(f"Using  {script_path}  as script_path")

st.write(f"sys.path is now:  {sys.path}")

# this might not be necessary as one can also use .. and deal with paths during import.
if not script_path in sys.path:  # otherwise will add anew with every run of script.
    sys.path.append(script_path)
    st.write("Added script_path to search path.")
    st.write(f"sys.path is now:  {sys.path}")

# libraries needed from outside
from os.path import splitext
from re import split              # regular expression string splitter

# these are saved into script_path. import first after sys.path is changed.
from src.VideoProcessing import check_path, stop_if_no_path 
# check also load_video_run_openpose(), which still has some bugs.
from src.VideoProcessing import load_video_run_openpose
from src.VideoProcessing import resize_video, delete_outputs, rename_json  

### getting some parameters

output_dir = cfg.get('folders', 'output_dir') 
input_dir = cfg.get('folders', 'input_dir')
input_video_fullsize_dir = cfg.get('folders', 'input_video_fullsize_dir')
input_video_resized_dir = cfg.get('folders', 'input_video_resized_dir')

st.write(f"output_dir is {output_dir}  input_dir is {input_dir} ")
st.write(f"input_video_fullsize_dir is {input_video_fullsize_dir} input_video_resized_dir is {input_video_resized_dir}")

# check_path(input_video_fullsize_dir)
# check_path(input_video_resized_dir)

### Variables that are calculated from other variables.
video_size = cfg.get('resize_video', 'video_size')
new_height = "".join([chr for chr in video_size if chr.isdigit()])  # used to resize

#fourth list of videos
# video_list = [uploaded_video_name]
# "1p_Daniele_16012022_choreo1.mp4",
# "1p_20211216_Francesca_Zeni.mp4",
# "1p_ThomasW_girl_16012022_choreo1.mp4",

#######################


# In terminal$ streamlit run upload_file_to_S3.py
# will open the webpage with the possibility to upload a file.
# This python script defines the webpage.

# github does not allow for opening files this big. The video needs to stored in the S3 Bucket.
# skeleton_video_file = open("https://salsaannotation.s3.eu-central-1.amazonaws.com/video/Ana_skeleton_with_music.mp4", "rb")
# I have managed to save a video to S3 from the sharelit cloud.  
# DONE Try using Boto3 which is the python interface to AWS.  (I think I have done that previosly)

# this deals with the upload and download of files from S3
s3 = boto3.client('s3')


#################################
# Functions
#################################
 
@st.cache(ttl=600) # this is a function because when the result exist it is not run again
def get_file_from_s3(get_file_name, save_file_name):
    s3.download_file(
        Bucket="salsaannotation", 
        Key=get_file_name,
        Filename=save_file_name 
        )
    
# the file will be downloaded only once, as it now is using a cached function.
# earlier it was happen every time user touched/run the app.
get_file_from_s3(
        get_file_name="video/Ana_skeleton_with_music.mp4", 
        save_file_name="ana_skeleton_with_music.mp4"
        )

# This works also from Streamlit cloud. 
# both use folder from root without /
s3.upload_file(
    Filename="visualization/1P-Ana_skeleton_subtitled.mp4",
    Bucket="salsaannotation",
    Key = "video/testing_upload_to_s3.mp4",
    )


# Allow upload video
#@st.cache(allow_output_mutation=True, ttl=600)
def save_file_to_S3(file_path, save_as="video/saved_from_streamlit_cloud.mp4"):
    # col1.write(filename)
    col1.write(save_as)
    try:
        s3.upload_file(
            Filename= file_path,
            Bucket="salsaannotation",
            Key = save_as,
            ) 
        # file_path = S3_folder + "/" + uploaded_file.name
        # with open(file_path,'wb') as f:
        #     f.write(uploaded_file.getbuffer())
        return 1
    except:
        col1.write("Failed to save the uploaded file on S3.")
        return 0

# Remove every thing that can be a problem in a file name or a AWS key.
def clean(string):
    import re
    clean_string = string.replace("/", "-")
    clean_string = string.replace(" ", "_") 
    clean_string = re.sub("""[/{/}!();:'/"\,<>?@#$%^&*~]""", "", clean_string)
    clean_string = clean_string.strip()
    clean_string = clean_string.lstrip("_") #starting a name with _ leads to funny names in Markdown
    return clean_string

def get_data():
    return []

##################################################

st.title('Send a video, get a Stick Figure')

#three columns and their relative width
col1, col2 = st.columns([4, 4])

col1.write("This app will allow you to upload a video. You will in 10 minutes receive an email with a link to a videofile that contains your processed video.")

col2.subheader("Choreographies:")
col2.markdown("Play this video if you want to learn to record the first choreography:")
col2.markdown("https://drive.google.com/file/d/1tX5dczXymc4EjAB0A9-5mkPx-pvV412n/view?usp=sharing")
    
col2.markdown("The Second Choreography is not out yet")
col2.markdown("At this stage we can only use videos that contain one of the predefined choreograpies. ")
col2.subheader("FAQ")
col2.markdown("https://salsa.eero.no   ") 

col2.subheader("Background Examples:")
# show the skeleton video as example
# downloaded from S3
col2.text('Black Background')
# skel_bytestream = skeleton_video_file.read()
col2.video("ana_skeleton_with_music.mp4")

# from the repo
col2.write("Original Background:")
col2.video("./visualization/Ana_h540_clip_for_Streamlit.mp4")

with st.sidebar:
    with st.form("user-info", clear_on_submit=True):      
        nickname = st.text_input("What is your nickname? We use it as part of the filename.",
                                        key="nickname", 
                                        max_chars=12
                                        )
        coreo = st.radio("Which choreography did you dance on the video?",
                                        ("First", "Second"),
                                        key="coreo"
                                        )
        video_background = st.radio("What kind of background should the stickfigure video have?",
                                            ("Black", "Original"),
                                            key="video_background"
                                            )
        email = st.text_input("To which email do you want have the link sent to?",
                                    key="email"
                                    )
        salsa_style = st.selectbox("Which style of Salsa do you dance normally or best?",
                                    ("Cuban", "LA/On1", "NY/On2",
                                    "All above", "Other"),
                                    key="salsa_style"
                                    ) 
        if nickname + email is None: 
            st.write("You really should answer the questions.")
        else:   
            submitted = st.form_submit_button(label="Submit answers", 
                            help="Submit info before uploading the video"
                            )
            skeleton_on_black_background = False
            if video_background=="Black":
                skeleton_on_black_background = True



# dance_role = st.sidebar.selectbox("Which role do you normally dance?",
#                                     ("Follower/Female", "Leader/Male"),
#                                     key="dance_role"
#                                     )



#TODO: consider to allow upload of video, only if questions are answered. 
# I tried with if submitted: but it did not work

# limiting the available types is a good for security
# uploaded_file is a stream. To get the name use uploaded_file.name 

uploaded_file = col1.file_uploader("Upload Video", 
                                       type=["mp4","avi","mov", "wmv", "mkv"],
                                       accept_multiple_files=False)
if uploaded_file is not None:
    upload_timestamp = datetime.now().strftime("%Y%m%d%H%M")
    # col1.write(f"Timestamp: {upload_timestamp})
    changing_video_name = clean(f"{nickname}_{coreo}_{video_background}_{salsa_style}_{upload_timestamp}_{uploaded_file.name}")
    changing_video_name = os.path.join("video/", changing_video_name)  
    uploaded_video_name = uploaded_file.name 
    video_list = [uploaded_video_name]      # this list is parsed later, makes it possible to process one or many videos  
    #saving the object as a file in streamlit for saving to S3
    uploaded_file_path = os.path.join("temp",uploaded_file.name)
    with open(uploaded_file_path,"wb") as f:
        f.write(uploaded_file.getbuffer())
    
       
    col1.write(f"You have just uploaded {uploaded_file.name}.")
    # the streamlit .video() accepts the object as it is
    col1.video(uploaded_file)  
    # col1.write(f"It will be saved on S3 as {changing_video_name}.") 
  
    
    if save_file_to_S3(uploaded_file_path, save_as=changing_video_name):
        col1.write("Successfully Saved to S3.")
    
    if validators.email(email)==False:
        col1.write(f"Your email is not valid {email}. If you want to have the link sent to you, you need to refill the form.")

        
    col1.write("""Start anew by clicking on the X under the "Browse files" button and fill in the form again""")    

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
           

else:
    col1.write("Start by answering a few questions in the sidebar.")
    col1.write("You can upload up to four different videos of one person dancing the same choreography.")
    col1.write("If you have several videos upload them one by one.")
        
##############################################################################
## Processing the video file
##############################################################################


# check also load_video_run_openpose(), which still has some bugs.
# run after config.ini to get the path right


  


  # Creating the annotation file
  # TODO: make os independent. use shutil.copy(src, dst) and os.path()
  # !cp $script_path/AnnotationFile.py .
  # !python AnnotationFile.py $output_op_dir

  # Parsing JSON and adding information from annotation
  # Anot_file = output_op_dir + "/Annotation.json"
  # !cp $script_path/Parsing-Openpose-Annotation.py .
  # !python Parsing-Openpose-Annotation.py $video_id $output_op_dir $Anot_file
  
    


            
        
        #TODO: In addition data should be saved on S3. Perhaps 
        # read a csv 
        # add a line for each new video
        # write csv  OR
        # use a pickled dataframe
        # get_data().append(
        #     {"video_file": uploaded_file.name, 
        #     "coreo": coreo, 
        #     "video_background": video_background,
        #     "email": email,
        #     "dance_role": dance_role,
        #     "salsa_style": salsa_style         
        #     })

        # st.write(pd.DataFrame(get_data()))
 
# Running the prediction
# col3.text('Our predictions :')

# fig, ax = plt.subplots(1, 3)
# for i in range(3):
#     prediction = check_pred(i)
#     ax[i] = sns.barplot(y = 'name',x='values', data = prediction,order = prediction.sort_values('values',ascending=False).name)
#     ax[i].set(xlabel='Confidence %')

# col3.pyplot(fig)
# os.remove('video-test/' + uploaded_file.name)

##############################################
# Answer questions
# https://discuss.streamlit.io/t/save-user-input-into-a-dataframe-and-access-later/2527/3

