# BOTO3 works. 
import streamlit as st
import pandas as pd
# from Inference import *
import boto3
import os
# import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="darkgrid")
sns.set()
from PIL import Image

# In terminal$ streamlit run upload_file_to_S3.py
# will open the webpage with the possibility to upload a file.
# This python script defines the webpage.

# parameters
# S3_folder = "salsaannotation/video/"

# github does not allow for opening files this big. The video needs to stored in the S3 Bucket.
# skeleton_video_file = open("https://salsaannotation.s3.eu-central-1.amazonaws.com/video/Ana_skeleton_with_music.mp4", "rb")
# I have managed to save a video to S3 from the sharelit cloud.  
# DONE Try using Boto3 which is the python interface to AWS.  (I think I have done that previosly)


# this deals with the upload and download of files from S3
s3 = boto3.client('s3')

# TODO : make this to a function? or just move to below and use variables.
s3.download_file(
    Bucket="salsaannotation", 
    Key="video/Ana_skeleton_with_music.mp4",
    Filename="downloaded_from_s3.mp4" 
    )

# This works also from Streamlit. 
# s3.upload_file(
#     Filename="visualization/1P-Ana_skeleton_subtitled.mp4",
#     Bucket="salsaannotation",
#     Key = "video/testing_upload_to_s3.mp4",
#     )

@st.cache(allow_output_mutation=True, ttl=600)

# def read_video(filename):
#     with fs.open(filename, "rb") as f:
#         return f.read()
    
# skel_bytestream = read_video("downloaded_from_s3.mp4")


# Allow upload video
def save_uploaded_file(uploaded_file):
    try:
        changing_video_name = f"{coreo}_{video_background}_{dance_role}_{salsa_style}_{uploaded_file.name}"
        s3.upload_file(
            Filename= uploaded_file.name,
            Bucket="salsaannotation",
            Key = "video/testing_video_upload.mov",
            ) 
        # file_path = S3_folder + "/" + uploaded_file.name
        # with open(file_path,'wb') as f:
        #     f.write(uploaded_file.getbuffer())
        return 1
    except:
        return 0


def get_data():
    return []



st.title('SalsaAnnotation')

#three columns and their relative width
col1, col2 = st.columns([3, 3])

col1.write("This app will allow you to upload a video. You will in 10 minutes receive an email with a link to a videofile that contains your processed video.")

col1.subheader("Choreographies:")
col1.markdown("[The first choreography]: https://drive.google.com/file/d/1tX5dczXymc4EjAB0A9-5mkPx-pvV412n/view?usp=sharing  [The first choreography]")
    
col1.markdown("The Second Choreography is not out yet")
col1.markdown("At this stage we can only annotate videos that contain one of the predefined choreograpies. ")
col1.subheader("FAQ")
col1.markdown("[FAQ]: https://salsa.eero.no   [FAQ]") 
      

#TODO: consider to allow upload of video, only if questions are answered. 
coreo = st.sidebar.selectbox("Which choreography did you dance on the video?",
                                ("First", "Second"),
                                key="coreo"
                                )

video_background = st.sidebar.radio("What kind of background should the stickfigure video have?",
                                    ("Black", "Original"),
                                    key="video_background"
                                    )

#TODO: Add validation of the email address
email = st.sidebar.text_input("To which email do you want have the link sent to?",
                                key="email"
                                )

dance_role = st.sidebar.selectbox("Which role do you normally dance?",
                                    ("Follower/Female", "Leader/Male"),
                                    key="dance_role"
                                    )

salsa_style = st.sidebar.selectbox("Which style of Salsa do you dance normally or best?",
                                    ("Cuban", "LA/On1", "NY/On2",
                                    "All above", "Other"),
                                    key="salsa_style"
                                    )

uploaded_file = st.sidebar.file_uploader("Upload Video", type=["mp4","avi","mov", "wmv", "mkv"])


if uploaded_file is not None:
    col1.write(uploaded_file.name)
    col1.write(changing_video_name)
    if save_uploaded_file(uploaded_file):
        #TODO: In addition data should be saved on S3. Perhaps 
        # read a csv 
        # add a line for each new video
        # write csv  OR
        # use a pickled dataframe
        get_data().append(
            {"video_file": uploaded_file.name, 
            "coreo": coreo, 
            "video_background": video_background,
            "email": email,
            "dance_role": dance_role,
            "salsa_style": salsa_style         
            })

        st.write(pd.DataFrame(get_data()))
        st.sidebar.write(" ")
        st.sidebar.write(" ")
        st.sidebar.write("Remove the video from the list above to rerun with a new video.")

        # # display original video
        # video_file = open( os.path.join("video-test", uploaded_file.name), 'rb' )
        # video_bytes = video_file.read()
        # col1.text('Original Video')
        # col1.video(video_bytes)
    else:
        col1.write("Start by uploading a short salsa video of one person dancing.")

# show the skeleton video as example
col1.text('Skeleton Video with Black Background')
# skel_bytestream = skeleton_video_file.read()
col1.video("downloaded_from_s3.mp4")

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

