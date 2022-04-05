# This script is used to do inference with a particular model
# It assumes that the data has been already preprocessed
# Here we do the inference from the validation data
# This is the same file as /deployment/inference modified to run on share.streamlit.io 

import pickle
import numpy as np
import pandas as pd

# Parameters of the data
MAX_SEQ_LENGTH = 40   # number of frames per figure
NUM_FEATURES = 75     # number of join coordinates

# Loading the data
PATH_DATA_VAL = "ml/models/Data_train_validate/Data_val_norm.csv"
data_val = pd.read_csv(PATH_DATA_VAL)

# loading the model
loaded_model = pickle.load(open("deployment/weights/GRU_model.pkl", 'rb'))

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

feat_cols = ['nose_x', 'nose_y',
       'neck_x', 'neck_y', 'rshoulder_x', 'rshoulder_y', 'relbow_x',
       'relbow_y', 'rwrist_x', 'rwrist_y', 'lshoulder_x', 'lshoulder_y',
       'lelbow_x', 'lelbow_y', 'lwrist_x', 'lwrist_y', 'midhip_x', 'midhip_y',
       'rhip_x', 'rhip_y', 'rknee_x', 'rknee_y', 'rankle_x', 'rankle_y',
       'lhip_x', 'lhip_y', 'lknee_x', 'lknee_y', 'lankle_x', 'lankle_y',
       'reye_x', 'reye_y', 'leye_x', 'leye_y', 'rear_x', 'rear_y', 'lear_x',
       'lear_y', 'lbigtoe_x', 'lbigtoe_y', 'lsmalltoe_x', 'lsmalltoe_y',
       'lheal_x', 'lheal_y', 'rbigtoe_x', 'rbigtoe_y', 'rsmalltoe_x',
       'rsmalltoe_y', 'rheal_x', 'rheal_y', 'nose_v', 'neck_v', 'rshoulder_v',
       'relbow_v', 'rwrist_v', 'lshoulder_v', 'lelbow_v', 'lwrist_v',
       'midhip_v', 'rhip_v', 'rknee_v', 'rankle_v', 'lhip_v', 'lknee_v',
       'lankle_v', 'reye_v', 'leye_v', 'rear_v', 'lear_v', 'lbigtoe_v',
       'lsmalltoe_v', 'lheal_v', 'rbigtoe_v', 'rsmalltoe_v', 'rheal_v']

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

    # Changing format of the data to be compatible with Tensor Flow
    X = [x.loc[ind_samp[ind], :].to_numpy() for (ind, x) in enumerate(X)]
    X = np.array(X)
    X = X.reshape(len(ind_start) - 1, MAX_SEQ_LENGTH, NUM_FEATURES).astype("float32")
    # TODO: decide of the X values need to be normalized
    y = [enc_label(x) for x in y]
    y = np.array(y).astype("float32")

    return X, y, info

# Functions to print the predictions
# Checking the predictions for the validation set
classes = {0.: "basic",
           1.: "right-turn",
           2.: "side",
           3.: "cuban-basic",
           4.: "suzie-q"
           }


def check_pred(ind):
    #pred = loaded_model.predict(np.expand_dims(X_val[ind], axis=0))[0]
    #clip_name = info_val[ind]["clip_name"]
    #nu_frame = info_val[ind]["frame_nr"]

    #print(f"Real: Label {classes[y_val[ind]]} ")
    #print(f"Source: Video {clip_name} Frame {nu_frame} \n")
    #for ind_i, i in enumerate(classes.keys()):
    #    print(f"  {classes[i]}: {pred[ind_i] * 100:5.2f}%")


    figs_labels = list( classes.values() )
    prediction = loaded_model.predict(np.expand_dims(X_val[ind], axis=0)) * 100
    prediction = pd.DataFrame(np.round(prediction, 1), columns=figs_labels).transpose()
    prediction.columns = ['values']
    prediction = prediction.reset_index()
    prediction.columns = ['name', 'values']

    return prediction

# Val set
X_val, y_val, info_val = transf_data(data_val)


