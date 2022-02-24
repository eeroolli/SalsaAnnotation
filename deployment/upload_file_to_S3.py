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
st.markdown("This app will allow you to upload a video and it sends you back an email with a link to a videofile that contains your processed video.  ")
st.markdown("      ")
st.subheader("Choreographies:")
st.markdown("[The first choreography]: https://drive.google.com/file/d/1tX5dczXymc4EjAB0A9-5mkPx-pvV412n/view?usp=sharing  [The first choreography] ")       
   
st.markdown("The Second Choreography is not out yet")
st.markdown("At this stage we can only annotate videos that contain one of the predefined choreograpies. ")
# st.markdown("* Role: Do you dance Leader/Male or Follower/Female role?")
# st.markdown("* Style: What style of Salsa do you dance?")
# st.markdown("")

col1, col2, col3 = st.columns([3,3,2])


#TODO: first answer questions and then allow upload of video. 

# Allow upload video
def save_uploaded_file(uploaded_file):
    try:
        with open(os.path.join('video-test',uploaded_file.name),'wb') as f:
            f.write(uploaded_file.getbuffer())
        return 1
    except:
        return 0

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
        st.sidebar.text("Your video is uploaded.")
    except:
        st.write("No skeleton video, yet")
else:
    try:
        uploaded_file = st.sidebar.file_uploader("Upload Video")

        coreo = st.sidebar.selectbox("Which choreography did you dance on the video?", 
                            ("First", "Second"),
                            key="coreo"
                            )



        video_background = st.sidebar.radio("What kind of background should the stickfigure video have?", 
                            ("Black", "Original"),
                            key="video_background"
                            )

        #TODO: Add validation to the email address
        email = st.sidebar.text_input("To which email do you want have the link sent to?", 
                            key="email"
                            )

        dance_role = st.sidebar.selectbox("Which role do you normally dance?",
                            ("Follower/Female", "Leader/Male"),
                            key="dance_role"
                            )

        salsa_style = st.sidebar.selectbox("Which style of Salsa do you dance normally or best?", 
                            ("Cuban", "LA/On1", "NY/On2", "All above", "Other" ),
                            key="salsa_style"
                    )


        # st.sidebar.button(label='Save')
    except:
        st.write("Something is wrong")


##############################################
# Answer questions
# https://discuss.streamlit.io/t/save-user-input-into-a-dataframe-and-access-later/2527/3

@st.cache(allow_output_mutation=True)
def get_data():
    return []

if st.button("Save my info"):
    get_data().append(
        {"video_file": uploaded_file.name, 
         "coreo": coreo, 
         "video_background": video_background,
         "email": email,
         "dance_role": dance_role,
         "salsa_style": salsa_style         
         })

st.write(pd.DataFrame(get_data()))

