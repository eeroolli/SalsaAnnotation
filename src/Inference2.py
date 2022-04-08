# This script is used to do inference with a particular model
# It assumes that the data has been already preprocessed
# Here we do the inference from the validation data

import pickle
import numpy as np
import pandas as pd
from configparser import ConfigParser, ExtendedInterpolation

from src.utils import keep_only_words, make_list_from_string

cfg = ConfigParser(interpolation=ExtendedInterpolation())
cfg.read('src/config.ini')

running_app_on_streamlit = cfg.getboolean('installation', 'running_app_on_streamlit')

if running_app_on_streamlit==True:
    cfg.read('deployment/config_streamlit.ini')
 
root_path = cfg.get('installation', 'root_path')


# Parameters of the data
MAX_SEQ_LENGTH = cfg.getint('training', 'MAX_SEQ_LENGTH')
NUM_FEATURES   = cfg.getint('training', 'NUM_FEATURES')
feat_cols = make_list_from_string(cfg.get('training', 'FEATURE_COLS'))

# Fixing format of the label
def enc_label(label):
    code = 0
    if label == "right-turn":
        code = 1
    if label == "side":
        code = 2
    if label == "cuban-basic":
        code = 3
    if label == "suzie-q":
        code = 4
    return code


# loading the data
# Function to select a number of frames per figure and right in the correct format for the mdoel
def transf_data(data):
    # Data preprocessing, get the input X and the label y
    ind_start = data[data['status'] == "S"].index.tolist()
    ind_end = data[data['status'] == "E"].index.tolist()

    # Take intervals between consecutive "S", they define one figure
    X = []
    y = []
    info = []

    for i in range(len(ind_start) - 1):
        X.append(data.loc[ind_start[i]: ind_end[i], feat_cols])  # - 3 the last 25 (visibility ) + 2
        y.append(data.loc[ind_start[i], 'label'])
        info.append(data.loc[ind_start[i], ['clip_name', 'frame_nr']])

    # select frames from the interval
    ind_samp = []

    for i in range(len(ind_start) - 1):
        # Take frames that are evenlly distributed
        aux = np.linspace(ind_start[i]
                          , ind_end[i]
                          , MAX_SEQ_LENGTH
                          , endpoint=False).astype(int)

        # random
        # aux = np.random.randint(ind_start[i], ind_end[i], MAX_SEQ_LENGTH)
        # aux.sort()
        ind_samp.append(aux)
    print(f"MAX_SEQ_LENGTH: {MAX_SEQ_LENGTH} \nNUM_FEATURES: {NUM_FEATURES}")
    # Changing format of the data to be compatible with Tensor Flow
    X = [x.loc[ind_samp[ind], :].to_numpy() for (ind, x) in enumerate(X)]
    X = np.array(X)
    X = X.reshape(len(ind_start) - 1, MAX_SEQ_LENGTH, NUM_FEATURES).astype("float32")
    y = [enc_label(x) for x in y]
    y = np.array(y).astype("float32")

    return X, y, info

# Functions to print the predictions
# Checking the predictions for the validation set
# TODO: Move the classes to config.ini [prediction]
classes = {0.: "basic",
           1.: "right-turn",
           2.: "side",
           3.: "cuban-basic",
           4.: "suzie-q"
           }


# loading the model (moved the path to config ini)  But why is it needed here. Why does the check_pred()
# not just use the loaded_model in make_prediction_demo
# loaded_model = pickle.load(open("deployment/weights/GRU_model.pkl", 'rb'))
loaded_model = pickle.load(open(cfg.get('prediction', 'model_weights'), 'rb'))

def check_pred(Xdata):
    figs_labels = list( classes.values() )
    prediction = loaded_model.predict(np.expand_dims(Xdata, axis=0)) * 100
    classes_x = np.argmax(prediction, axis=1)
    classes_x = classes_x.reshape(1, 1)
    pred_label = classes[classes_x[0][0]]

    prediction = pd.DataFrame(np.round(prediction, 1), columns=figs_labels).transpose()
    prediction.columns = ['values']
    prediction = prediction.reset_index()
    prediction.columns = ['name', 'values']
    # prediction = prediction.sort_values("name")

    return prediction, pred_label

