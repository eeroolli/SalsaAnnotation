# from functools import cache
import streamlit as st
import pandas as pd
# from Inference import *
import boto3
import os
# import matplotlib.pyplot as plt
# import seaborn as sns
# sns.set_theme(style="darkgrid")
# sns.set()
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

st.title('SalsaAnnotation')

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
    #TODO: give user a way to clear the form. 
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
# object below is a stream. To get the name use uploaded_file.name 
if submitted:
    uploaded_files = col1.file_uploader("Upload Video", type=["mp4","avi","mov", "wmv", "mkv"],
                                   accept_multiple_files=True)
    counter = 0
    for uploaded_file in uploaded_files:
        counter = counter + 1
        now = datetime.now().strftime("%Y%m%d%H%M")
        changing_video_name = clean(f"video/{nickname}_{coreo}_{video_background}_{salsa_style}_{now}_{counter}_{uploaded_file.name}")
        changing_video_name = os.path.join("video/", changing_video_name)  
        
        # first saving the object as file in streamlit
        uploaded_file_path = os.path.join("temp",uploaded_file.name)
        with open(uploaded_file_path,"wb") as f:
            f.write(uploaded_file.getbuffer())
        col1.write("If you have several videos of one person upload them all at once.")
        col1.write("If you have vidoes of several persons, upload them one by one")
        col1.write("click on the X after your video and fill in the form again")    
        
        col1.write(f"You have just uploaded {uploaded_file.name}.")
        col1.video(uploaded_file)  
        
        if save_file_to_S3(uploaded_file_path, save_as=changing_video_name):
            col1.write("Successfully saved to S3")
        
else:
    col1.write("Start by answering a few questions in the sidebar.")
    col1.write("You can upload up to four different videos of the same choreography, but only one person at a time.")


            
        
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

