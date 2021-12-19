import streamlit as st
import pandas as pd
from Inference import *
import os
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="darkgrid")
sns.set()
from PIL import Image

# In terminal$ streamlit run Model_deployment.py
# will open the webpage with the running prediction.
# This python script defines the webpage.


st.title('SalsaClassifier')

skeleton_video_file = None
   #three columns and their relative width

col1, col2, col3 = st.columns([2,3,3])

# Allow upload video
def save_uploaded_file(uploaded_file):
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
        skeleton_video_file = open(os.path.join("static", "openpose-Gustavo.mp4"), 'rb')
        skel_bytes = skeleton_video_file.read()
        col2.text('Skeleton Video ')
        col2.video(skel_bytes)
        st.sidebar.write(" ")
        st.sidebar.write(" ")
        st.sidebar.write("Remove the video from the list above to rerun with a new video.")

        # Running the prediction
        col3.text('Our predictions :')

        fig, ax = plt.subplots(1, 3)
        for i in range(3):
            prediction = check_pred(i)
            ax[i] = sns.barplot(y = 'name',x='values', data = prediction,order = prediction.sort_values('values',ascending=False).name)
            ax[i].set(xlabel='Confidence %')

        col3.pyplot(fig)
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

