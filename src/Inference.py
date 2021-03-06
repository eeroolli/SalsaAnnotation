# This script is used to do inference with a particular model
# It assumes that the data has been already preprocessed
# Here we do the inference from the validation data

import pickle
import numpy as np
import pandas as pd

# Parameters of the data
MAX_SEQ_LENGTH = 60   # number of frames per figure
NUM_FEATURES = 75     # number of join coordinates

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

# TODO 
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

    return prediction, pred_label

# loading the model
# TODO: move the model def to config.ini [prediction]
loaded_model = pickle.load(open("../deployment/weights/GRU_64.pkl", 'rb'))
