# from logging import root
import streamlit as st
import pandas as pd
# import pickle
# import boto3
import os
# from os.path import splitext
import sys
# from datetime import datetime
# import validators
import matplotlib.pyplot as plt
import seaborn as sns
# from PIL import Image
from configparser import ConfigParser, ExtendedInterpolation

from src.Inference2 import enc_label, check_pred, transf_data, load_saved_weights
from src.utils import keep_only_words, make_list_from_string, get_choreography
# Streamlit requires that streamlit run collect_and_process_videos is run from the Repo root!
from src.VideoProcessing  import  check_path, stop_if_no_path 
# check also load_video_run_openpose(), which still has some bugs.
from src.VideoProcessing  import load_video_run_openpose
from src.VideoProcessing import resize_video, delete_outputs, rename_json  


cfg = ConfigParser(interpolation=ExtendedInterpolation())
cfg.read('src/config.ini')
# st.write(f"config.ini has these sections:, {cfg.sections()} \n")

running_app_on_streamlit = cfg.getboolean('installation', 'running_app_on_streamlit')
# this script works only with Streamlit
assert running_app_on_streamlit == True

if running_app_on_streamlit==True:
    cfg.read('deployment/config_streamlit.ini')
  
parent_path = cfg.get('installation', 'parent_path')
root_path = cfg.get('installation', 'root_path')
script_path = cfg.get('installation', 'script_path')

# st.write(f"Using {root_path}    as root_path")
# st.write(f"Using {script_path}  as script_path")
# st.write(f"sys.path is now:  {sys.path}")
# st.write(''' Streamlit cloud wants the file to be 
#          in the repo root and all other references 
#          should be relative.
#          ''')

if not script_path in sys.path:  # otherwise will add anew with every run of script.
    sys.path.append(script_path)
    st.write("Added script_path to search path.")
    st.write(f"sys.path is now:  {sys.path}")

MAX_SEQ_LENGTH = cfg.getint('training', 'MAX_SEQ_LENGTH')
NUM_FEATURES   = cfg.getint('training', 'MAX_SEQ_LENGTH')
feat_cols = make_list_from_string(cfg.get('training', 'FEATURE_COLS'))
skeleton_video_file = None

sns.set_theme(style="darkgrid")
sns.set()

choreography = get_choreography(name_of_choreography="coreo")

#########################################
st.title('Salsa Annotation')

st.write('''For this demo uses Machine Learning to identify salsa figures. 
         We use an preprosessed video file, 
         where the beginning of each figure is marked, without labels.  
         The predictions are made while you are wathcing, using our trained model.
         The purpose is to see where the predictions are correct and where they are wrong.''')

st.write('''Because the dancers are dancing a fixed choreography, we can compare
         the predictions with what they were supposed to dance (the Facit).   
         ''')

#three columns and their relative width
col1, col2, col3 = st.columns([2,1,4])

with st.sidebar:
    with st.form("video-info", clear_on_submit=False):      
        person = st.radio("Whose video do you want to use for seeing the predictions?",
                                        ("Ana", "Vasil"),
                                        key="person"
                                        )
        submitted = st.form_submit_button(label="Submit answers", 
                            help="Prediction starts after you submit."
                            )
        

    

if submitted is not None:
    if person == "Ana":
        file_name = "1P-Ana.mp4"
    if person == "Vasil":
        file_name = "1p_Vasil_1_11122021_Choreo1.mp4"
        
    video_path = os.path.join("deployment", "static", file_name)
    video_file = open(video_path,'rb' )
    video_bytes = video_file.read()
    col1.text('Preprocessed Video')
    col1.video(video_bytes)
    
        # show also the skeleton
        # skeleton_video_file = open(os.path.join("deployment", 
        #                                         "static", 
        #                                         "openpose-Gustavo.mp4"), 
        #                            'rb')
        # skel_bytes = skeleton_video_file.read()
        # col2.text('Skeleton Video ')
        # col2.video(skel_bytes)
       
    # Running the prediction
    col3.text('Our predictions :')
    
    @st.cache()
    def get_csv_data(person):
        data_file_name= 'Data_norm_' + person + ".csv"
        PATH_DATA_VAL = os.path.join("deployment", "static", data_file_name)
        data_val = pd.read_csv(PATH_DATA_VAL)
        return data_val
    
    data_val = get_csv_data(person=person)
    X_val, y_val, info_val = transf_data(data_val)
    n_of_figures = X_val.shape[0]
    # plt.figure()

    while n_of_figures > len(choreography):
        choreography = choreography + choreography

    col3.write(f"There are predictions for {n_of_figures} figures: ")
    correct = 0
    
    for i in range(n_of_figures): 
        prediction, label = check_pred(X_val[i])
        # ax[i] = sns.barplot(y = 'name',x='values', data = prediction,order = prediction.sort_values('values',ascending=False).name)
        # ax[i].set(xlabel='Confidence %')
        # col3.write(f"Figure {i}: {label} ")
        # col3.write(f"{prediction['name']} {round(prediction['values'], 2)} ")
        fig, ax = plt.subplots()
        ax.set(ylim=(0,100))
        ax.bar(prediction['name'], prediction['values'])
        plt.title(f"Figure {i}    Prediction: {label}     Facit: {choreography[i]} ")
        plt.xlabel('Confidence in %')
        col3.pyplot(fig=fig, clear_figure=True) 
        if (keep_only_words(label)==keep_only_words(str(choreography[i]))):
            correct += 1
    accuracy_score = round(correct/n_of_figures*100 , ndigits=1)
    col3.write(f"Accuracy for this video is {accuracy_score}%")    
    # os.remove('video-test/' + uploaded_file.name)
    st.close
else:
    col2.write("Start by choosing a video.")

 