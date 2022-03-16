# BOTO3 works. 
# from functools import cache
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

# github does not allow for opening files this big. The video needs to stored in the S3 Bucket.
# skeleton_video_file = open("https://salsaannotation.s3.eu-central-1.amazonaws.com/video/Ana_skeleton_with_music.mp4", "rb")
# I have managed to save a video to S3 from the sharelit cloud.  
# DONE Try using Boto3 which is the python interface to AWS.  (I think I have done that previosly)


# this deals with the upload and download of files from S3
s3 = boto3.client('s3')

 
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

# This works also from Streamlit. 
# s3.upload_file(
#     Filename="visualization/1P-Ana_skeleton_subtitled.mp4",
#     Bucket="salsaannotation",
#     Key = "video/testing_upload_to_s3.mp4",
#     )



# def read_video(filename):
#     with fs.open(filename, "rb") as f:
#         return f.read()
    
# skel_bytestream = read_video("downloaded_from_s3.mp4")


# Allow upload video
#@st.cache(allow_output_mutation=True, ttl=600)
def save_uploaded_file(filename):
    
    col1.write(filename)
    save_as = f"/video/uploaded_from_streamlit_cloud.mp4"
    col1.write(save_as)
    
    try:
        s3.upload_file(
            Filename= filename,
            Bucket="salsaannotation",
            Key = save_as,
            ) 
        # file_path = S3_folder + "/" + uploaded_file.name
        # with open(file_path,'wb') as f:
        #     f.write(uploaded_file.getbuffer())
        return 1
    except:
        return 0

# Remove every thing that can be a problem in a file name.
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

st.title('SalsaAnnotation')

#three columns and their relative width
col1, col2 = st.columns([3, 3])

col1.write("This app will allow you to upload a video. You will in 10 minutes receive an email with a link to a videofile that contains your processed video.")

col2.subheader("Choreographies:")
col2.markdown("The Video explaining how to do the First Choreography:")
col2.markdown("https://drive.google.com/file/d/1tX5dczXymc4EjAB0A9-5mkPx-pvV412n/view?usp=sharing")
    
col2.markdown("The Second Choreography is not out yet")
col2.markdown("At this stage we can only use videos that contain one of the predefined choreograpies. ")
col2.subheader("FAQ")
col2.markdown("https://salsa.eero.no   ") 

with st.sidebar:
    with st.form("user-info"):      
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
        submitted = st.form_submit_button(label="Submit answers", 
                            help="Submit info before uploading the video"
                            )


# dance_role = st.sidebar.selectbox("Which role do you normally dance?",
#                                     ("Follower/Female", "Leader/Male"),
#                                     key="dance_role"
#                                     )


#TODO: consider to allow upload of video, only if questions are answered. 
# limiting the available types is a good for security
uploaded_file = col1.file_uploader("Upload Video", type=["mp4","avi","mov", "wmv", "mkv"])


if uploaded_file is not None:
    uploaded_file_name = uploaded_file.name # testing if .name is a slowing everything down            
    col1.write(f"You have just successfully uploaded {uploaded_file.name}.")
    #{dance_role}_{salsa_style}_
    changing_video_name = clean(f"{nickname}_{coreo}_{video_background}_{salsa_style}_{uploaded_file.name}")
    col1.write(changing_video_name)
    save_uploaded_file(uploaded_file_name)
    
    working_dir = os.getcwd()
    col1.write(f"The working directory is {working_dir}")
    
    col1.subheader("This is the file you uploaded.")
    col1.video(uploaded_file)
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
    st.sidebar.write(" ")
    st.sidebar.write(" ")
    st.sidebar.write("click on the X after your video to upload a new video.")

        # # display original video
        # video_file = open( os.path.join("video-test", uploaded_file.name), 'rb' )
        # video_bytes = video_file.read()
        # col2.text('Original Video')
        # col2.video(video_bytes)
else:
    col1.write("Start by answering a few questions and then upload your salsa video of one person dancing a choreography.")



# show the skeleton video as example
col2.text('Example of a Skeleton Video with Black Background')
# skel_bytestream = skeleton_video_file.read()
col2.video("ana_skeleton_with_music.mp4")

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

