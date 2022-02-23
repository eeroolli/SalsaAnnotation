import streamlit as st
import pandas as pd
# from Inference import *
import os
# import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="darkgrid")
sns.set()
from PIL import Image

# In terminal$ streamlit run upload_file_to_S3.py
# will open the webpage with the possibility to upload a file.
# This python script defines the webpage.

S3_folder = "https://salsaannotation.s3.eu-central-1.amazonaws.com/video/"

st.title('SalsaAnnotation')

skeleton_video_file = None
   #three columns and their relative width
st.markdown("                                                                                                 ")
st.markdown("This app will allow you to upload a video and it sends you back an email with ")
st.markdown("a link to a videofile that contains your processed video.  ")
st.markdown("      ")
st.markdown("Options:")
st.markdown("* Annotation:  Do you want your video to include our guesses of the names of figures?")
st.markdown("* Background:  Should the skeleton video have black or normal background?")
st.markdown("Information about you and the video:")
st.markdown("* Choreography:  We can only annotate videos that contain one of the predefined choreograpies. ")
st.markdown("* Role: Do you dance Leader/Male or Follower/Female role?")
st.markdown("* Style: What style of Salsa do you dance?")
st.markdown("")

col1, col2, col3 = st.columns([2,3,3])
# Allo upload video
def sae_uploaded_file(uploaded_file):
    try:
        with open(os.path.join('video-test',uploaded_file.name),'wb') as f:
            f.write(uploaded_file.getbuffer())
        return 1
    except:
        return 0

uploaded_file = st.sidebar.file_uploader("Upload Video")

if uploaded_file is not None:
    if save_uploaded_file(uploaded_file):

        # display original video
        video_file = open( os.path.join("video-test", uploaded_file.name), 'rb' )
        video_bytes = video_file.read()
        col1.text('Original Video')
        col1.video(video_bytes)

        # show also the skeleton
        # skeleton_video_file = open(os.path.join("static", "openpose-Gustavo.mp4"), 'rb')
        # skel_bytes = skeleton_video_file.read()
        col2.text('Skeleton Video ')
        col2.video(skel_bytes)
        st.sidebar.write(" ")
        st.sidebar.write(" ")
        st.sidebar.write("Remove the video from the list above to rerun with a new video.")

        # Running the prediction
        col3.text('Our predictions :')

        # fig, ax = plt.subplots(1, 3)
        # for i in range(3):
        #     prediction = check_pred(i)
        #     ax[i] = sns.barplot(y = 'name',x='values', data = prediction,order = prediction.sort_values('values',ascending=False).name)
        #     ax[i].set(xlabel='Confidence %')

        # col3.pyplot(fig)
        os.remove('video-test/' + uploaded_file.name)
    else:
        col2.write("Start by uploading a short salsa video of one person dancing.")


if skeleton_video_file is not None:
    try:
        st.sidebar.download_button(label='Download your skeleton video',
                                  data=skeleton_video_file ,
                                  file_name='my_skeleton_video.mp4')

        st.sidebar.button(label='Download a text file with names of figures',
                             #     data=None,
                             #     mime="text/plain",
                             #     file_name='my_figures.txt'
                         )
    except:
        st.write("No skeleton video, yet")
else:
    try:
        st.sidebar.button(label='Your skeleton video is soon ready')
    except:
        st.write("Something is wrong")


##############################################

@st.cache(allow_output_mutation=True)
def get_data():
    return []

coreo = st.selectbox("Which choreography did you dance on the video?", index = 0, 
                     options("First")
                     key("coreo")
                     )

video_background = st.radio("What kind of background should the stickfigure video have?", 
                       options("Black", "Original"),
                       key("background")
                       )

#TODO: Add validation to the email address
email = st.text_input("To which email do you want have the link sent to?", 
                      key("email")
                      )

dance_role = st.selectbox("Which role do you normally dance?",
                    options("Follower/Female", "Leader/Male"),
                    key("dance_role")
                    )

salsa_style = st.selectbox("Which style of Salsa do you dance?", 
                    options("Cuban", "LA/On1", "NY/On2", "Other" )
                    key("salsa_style"))


if st.button("Add row"):
    get_data().append({"UserID": user_id, "foo": foo, "bar": bar})

st.write(pd.DataFrame(get_data()))

