from tensorflow.keras import models, layers
#TODO: implement EarlyStopping
from tensorflow.keras.callbacks import CSVLogger, EarlyStopping 

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import logging
import os
import glob 

# from tensorflow.keras import callbacks
# import csv

# VSCode requires: ml/models while PyCharm requires ../ 
root_path = "ml/models/"  
model_path = root_path + "GRU/"

if not os.path.exists(model_path + 'temp'):
    print("making a temp directory in ", model_path , 'temp')
    os.makedirs(model_path + 'temp')

# Define hyperparameters
BATCH_SIZE = 16
EPOCHS = 100
MAX_SEQ_LENGTH = 40   # number of frames per figure
NUM_FEATURES = 75     # number of join coordinates
DROPOUT_1 = 0.30       # Drop out rate after first GRU
DROPOUT_2 = 0.10      # Drop out rate after second GRU

##TODO: define Sim_ID as external parameter
Sim_ID = "GRU64-drop" + str(DROPOUT_1) + "-GRU32-drop" + str(DROPOUT_2) + "-Dense16"

file_to_delete = glob.glob(model_path + 'temp/' + Sim_ID + '*')

if not os.path.exists('temp'):
    os.makedirs('temp')

# Iterate over the list of filepaths & remove each file.
for filePath in file_to_delete:
    try:
        os.remove(filePath)
    except:
        print("Error while deleting file : ", filePath)


logging.basicConfig(filename = model_path + 'temp/' + Sim_ID + '.log', level='INFO')

# Load the data   
#PATH_DATA_TRAIN = root_path + "Data_train_validate/Data_train_orig_01_aug_x_xy.csv"
PATH_DATA_TRAIN = root_path + "Data_train_validate/Data_train_norm_1.csv"
PATH_DATA_VAL = root_path + "Data_train_validate/Data_val_norm_1.csv"

logging.basicConfig(filename='temp/' + Sim_ID + '.log', level='INFO')


print(data_train.shape)


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

assert len(feat_cols) == NUM_FEATURES

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

# Function to select a number of frames per figure and right in the correct format for the mdoel
def transf_data(data):
    # Get the input X and the label y
    ind_start = data[data['status'] == "S"].index.tolist()
    ind_end = data[data['status'] == "E"].index.tolist()

    # Take intervals between consecutive "S", they define one figure
    X = []
    y = []
    info = []

    for i in range(len(ind_start) - 1):
        X.append(data.loc[ind_start[i]: ind_end[i], feat_cols])
        y.append(data.loc[ind_start[i], 'label'])
        info.append(data.loc[ind_start[i], ['clip_name', 'frame_nr']])

    # select frames from the interval
    ind_samp = []

    for i in range(len(ind_start) - 1):
        # Take frames that are evenly distributed
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
    X = tf.Tensor.from_tensor_

    y = [enc_label(x) for x in y]
    y = np.array(y).astype("float32")

    return X, y, info

# Training and validation sets
X_train, y_train, info_train = transf_data(data_train)
X_val, y_val, info_val = transf_data(data_val)


print(X_train.shape)
print(y_train.shape)
print(X_val.shape)
print(y_val.shape)




# print parameters to file
logging.info(f"Parameters of the model BATCH_SIZE {BATCH_SIZE}")
logging.info(f"Parameters of the model EPOCHS {EPOCHS}")
logging.info(f"Parameters of the model MAX_SEQ_LENGTH {MAX_SEQ_LENGTH}")
logging.info(f"Parameters of the model NUM_FEATURES {NUM_FEATURES}")
logging.info(f"Parameters of the model DROPOUT_1 {DROPOUT_1}")
logging.info(f"Parameters of the model DROPOUT_2 {DROPOUT_2}")


# Build the model (This section can be modified to a diferent model)
model = models.Sequential()
model.add(layers.InputLayer(input_shape=(MAX_SEQ_LENGTH, NUM_FEATURES)))
model.add(layers.GRU(64, return_sequences=True))
model.add(layers.Dropout(DROPOUT_1))
model.add(layers.GRU(32))
model.add(layers.Dropout(DROPOUT_2))
model.add(layers.Dense(16, activation="relu"))
model.add(layers.Dense(5, activation="softmax"))
model.summary(print_fn=logging.info)

# Compile the model
model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

# Check the trainning accuracy


csv_logfile_name = os.path.join(model_path, "temp" , Sim_ID + "_log.csv")
csv_log = CSVLogger(csv_logfile_name)
                    

history = model.fit(
    X_train,
    y_train,
    epochs=EPOCHS,
    batch_size=BATCH_SIZE,

    validation_data=(X_val, y_val),
    callbacks=[csv_log]
)


# Checking accuracies
def render_history(history):
    plt.figure()
    plt.plot(history["loss"], label="loss")
    plt.plot(history["val_loss"], label="val_loss")
    plt.legend()
    plt.title("Losses")

    plt.savefig(os.path.join( model_path, "temp",  Sim_ID + "-Loss.jpg"))

 
    plt.figure()
    plt.plot(history["accuracy"], label="accuracy")
    plt.plot(history["val_accuracy"], label="val_accuracy")
    plt.legend()
    plt.title("Accuracies")
    plt.savefig(os.path.join(model_path, "temp",  Sim_ID + "-Acc.jpg"))


render_history(history.history)

_, accuracy = model.evaluate( X_val, y_val)
print(f"Accuracy is {round(accuracy * 100, 2)}%")
logging.info(f"Accuracy is {round(accuracy * 100, 2)}%")