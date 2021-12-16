import streamlit as st
import pandas as pd
from Inference import *
import os
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="darkgrid")
sns.set()
from PIL import Image

# Defining the enviroment
st.title('SalsaClassifier')

# Allow upload video
def save_uploaded_file(uploaded_file):
    try:
        with open(os.path.join('video-test',uploaded_file.name),'wb') as f:
            f.write(uploaded_file.getbuffer())
        return 1
    except:
        return 0

uploaded_file = st.file_uploader("Upload Video")

if uploaded_file is not None:
    if save_uploaded_file(uploaded_file):

        # display original video
        video_file = open( os.path.join("video-test", uploaded_file.name), 'rb' )
        video_bytes = video_file.read()
        st.video(video_bytes)

        # show also the skeleton
        skel = open(os.path.join("static", "openpose-Gustavo.mp4"), 'rb')
        skel_bytes = skel.read()
        st.video(skel_bytes)

        # Running the prediction
        st.text('Our predictions :')


        fig, ax = plt.subplots(1, 3)
        for i in range(3):
            prediction = check_pred(i)
            ax[i] = sns.barplot(y = 'name',x='values', data = prediction,order = prediction.sort_values('values',ascending=False).name)
            ax[i].set(xlabel='Confidence %')

        st.pyplot(fig)
        os.remove('video-test/' + uploaded_file.name)