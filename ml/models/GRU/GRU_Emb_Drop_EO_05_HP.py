# There are lots of changes in tensorflow 1.15 to 2. lots of syntax is different, and I do not 
# see an implementation of GRU, so even if it is possible to run directML and use non-cuda GPU
# it seems to be a futile operation.
# EO This runs on conda: salsaTF i wsl.  CPU only. 
# EO This runs on conda: aikit-tf i wsl.  CPU only. 


from unicodedata import name
import tensorflow as tf 
tf.test.is_built_with_gpu_support()

#TODO: implement EarlyStopping
from tensorflow.keras.callbacks import CSVLogger, EarlyStopping 
from tensorflow import keras
from tensorflow.keras import layers

from tensorboard.plugins.hparams import api as hp

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

if not os.path.exists(model_path + 'logs/hparam_tuning/'):
    print("making a temp directory in ", model_path, 'logs/hparam_tuning/')
    os.makedirs(model_path + 'logs/hparam_tuning/')




def delete_files(pattern):
    file_to_delete = glob.glob(pattern)
    # Iterate over the list of filepaths & remove each file.
    for filePath in file_to_delete:
        try:
            os.remove(filePath)
        except:
            print("Error while deleting file : ", filePath)

delete_files('./logs/' + '*')  # used by tensorboard


# Define hyperparameters
BATCH_SIZE = 128
EPOCHS = 200
MAX_SEQ_LENGTH = 60   # number of frames per figure
NUM_FEATURES = 75     # number of join coordinates
DROPOUT_1 = 0.4       # Drop out rate after first GRU
DROPOUT_2 = 0.2    # Drop out rate after second GRU
DROPOUT_3 = 0.1    # Drop out rate after second GRU

HP_BATCH_SIZE = hp.HParam('batchsize', hp.Discrete([64, 128]))
HP_NUM_UNITS = hp.HParam('num_units', hp.Discrete([32]))
HP_DROPOUT_1 = hp.HParam('dropout_1', hp.RealInterval(0.3, 0.6))
HP_DROPOUT_2 = hp.HParam('dropout_2', hp.RealInterval(0.2, 0.4))
HP_DROPOUT_3 = hp.HParam('dropout_3', hp.RealInterval(0.05, 0.1))
HP_OPTIMIZER = hp.HParam('optimizer', hp.Discrete(['adam', 'relu']))

METRIC_ACCURACY = 'accuracy'

with tf.summary.create_file_writer('logs/hparam_tuning').as_default():
  hp.hparams_config(
      hparams=[HP_NUM_UNITS, HP_DROPOUT_1, HP_DROPOUT_2, HP_DROPOUT_3, HP_OPTIMIZER],
    metrics=[hp.Metric(METRIC_ACCURACY, display_name='Accuracy')],
  )

##TODO: define Sim_ID as external parameter
Sim_ID = "HParam_test_" + str(BATCH_SIZE) + "-GRU64-drop" + str(DROPOUT_1) + "-GRU32-drop" + str(DROPOUT_2) + "-GRU32-drop" + str(DROPOUT_3) +"-Dense16"
delete_files(model_path + 'temp/' + Sim_ID + '*')  # delete previous run with same parameters


logging.basicConfig(filename = model_path + 'temp/' + Sim_ID + '.log', level='INFO')

# Load the data   
PATH_DATA_TRAIN = root_path + "Data_train_validate/Data_train_orig_01_aug_x_xy.csv"
PATH_DATA_VAL = root_path + "Data_train_validate/Data_val_norm_1.csv"
data_train = pd.read_csv(PATH_DATA_TRAIN)
data_val = pd.read_csv(PATH_DATA_VAL)

print(data_train.shape)
print("n of labels in training data \n", data_train["label"].value_counts())
print("n of frames in training data ", data_train["label"].count())

print("n of labels in validation data \n", data_val["label"].value_counts())
print("n of frames in validation data ", data_val["label"].count())
print("\n ######################################################## \n")

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
    code = 9
    if label == "basic":     # preparing to use uncut version, with 9 for "other" or "unknown"
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
    X = tf.convert_to_tensor(X)
    y = [enc_label(x) for x in y]
    y = np.array(y).astype("float32")
    y = tf.convert_to_tensor(y)
    return X, y, info



# Training and validation sets
X_train, y_train, info_train = transf_data(data_train)
X_val, y_val, info_val = transf_data(data_val)



print("X_train: ", X_train.dtype)
print("y_train: ", y_train.dtype)
# print("info_train: ", info_train.shape)


# print parameters to file
logging.info(f"Training data: {PATH_DATA_TRAIN}")
logging.info(f"Validation data: {PATH_DATA_VAL}")
logging.info(f"Parameters of the model BATCH_SIZE {BATCH_SIZE}")
logging.info(f"Parameters of the model EPOCHS {EPOCHS}")
logging.info(f"Parameters of the model MAX_SEQ_LENGTH {MAX_SEQ_LENGTH}")
logging.info(f"Parameters of the model NUM_FEATURES {NUM_FEATURES}")
logging.info(f"Parameters of the model DROPOUT_1 {DROPOUT_1}")
logging.info(f"Parameters of the model DROPOUT_2 {DROPOUT_2}")
logging.info(f"Parameters of the model DROPOUT_3 {DROPOUT_2}")

def train_test_model(hparams):
    # Build the model (This section can be modified to a diferent model)
    model = keras.Sequential()
    model.add(layers.InputLayer(input_shape=(MAX_SEQ_LENGTH, NUM_FEATURES)))
    model.add(layers.GRU(64, return_sequences=True, name="1_GRU"))
    model.add(layers.Dropout(HP_DROPOUT_1, name="1_dropout"))
    model.add(layers.GRU(64, return_sequences=True, name="2_GRU"))
    model.add(layers.Dropout(HP_DROPOUT_2, name="2_dropout"))
    model.add(layers.GRU(hparams[HP_NUM_UNITS], return_sequences=True, name="3_GRU"))
    model.add(layers.Dropout(HP_DROPOUT_3, name="3_dropout"))
    model.add(layers.GRU(32, name="4_GRU"))
    model.add(layers.Dense(16, activation="relu", name="4_Dense"))
    model.add(layers.Dense(6, activation="softmax", name="5_Dense"))
    model.summary(print_fn=logging.info)
    
    # Compile the model
    model.compile(
        optimizer=hparams[HP_OPTIMIZER],
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )
    model.fit(X_train,
              y_train,
              epochs=1)  # Run with 1 epoch to speed things up for demo purposes
    _, accuracy = model.evaluate(X_val, y_val)
    return accuracy

  

def run(run_dir, hparams):
  with tf.summary.create_file_writer(run_dir).as_default():
    hp.hparams(hparams)  # record the values used in this trial
    accuracy = train_test_model(hparams)
    tf.summary.scalar(METRIC_ACCURACY, accuracy, step=1)
    

# Check the trainning accuracy

# csv_logfile_name = os.path.join(model_path, "temp" , Sim_ID + "_log.csv")
# csv_log = CSVLogger(csv_logfile_name)

# def History():      
#     history = model.fit(
#         X_train,
#         y_train,
#         epochs=EPOCHS,
#         batch_size=BATCH_SIZE,
#         validation_data=(X_val, y_val),
#         callbacks=[csv_log, #the old system
#                 tf.keras.callbacks.TensorBoard(logdir),  # log metrics
#                 hp.KerasCallback(logdir, hparams),  # log hparams
#             ],
#         )
#     return history

# # Checking accuracies
# def render_history(history):
#     plt.figure()
#     plt.plot(history["loss"], label="loss")
#     plt.plot(history["val_loss"], label="val_loss")
#     plt.legend()
#     plt.title("Losses")
#     plt.savefig(os.path.join( model_path, "temp",  Sim_ID + "-Loss.jpg"))

#     plt.figure()
#     plt.plot(history["accuracy"], label="accuracy")
#     plt.plot(history["val_accuracy"], label="val_accuracy")
#     plt.legend()
#     plt.title("Accuracies")
#     plt.savefig(os.path.join(model_path, "temp",  Sim_ID + "-Acc.jpg"))

### FROM https://www.tensorflow.org/tensorboard/hyperparameter_tuning_with_hparams
session_num = 0

for num_units in HP_NUM_UNITS.domain.values:
  for dropout_rate_1 in (HP_DROPOUT_1.domain.min_value, HP_DROPOUT_1.domain.max_value):
      for dropout_rate_2 in (HP_DROPOUT_2.domain.min_value, HP_DROPOUT_2.domain.max_value):
        for dropout_rate_3 in (HP_DROPOUT_3.domain.min_value, HP_DROPOUT_3.domain.max_value):
            for optimizer in HP_OPTIMIZER.domain.values:
                hparams = {
                    HP_NUM_UNITS: num_units,
                    HP_DROPOUT_1: dropout_rate_1,
                    HP_DROPOUT_2: dropout_rate_2,
                    HP_DROPOUT_3: dropout_rate_3,
                    HP_OPTIMIZER: optimizer,
                }
                run_name = "run-%d" % session_num
                print('--- Starting trial: %s' % run_name)
                print({h.name: hparams[h] for h in hparams})
                run('logs/hparam_tuning/' + run_name, hparams)
                session_num += 1
                
                # render_history(history.history)

                # _, accuracy = model.evaluate(X_val, y_val)
                # print(f"Accuracy is {round(accuracy * 100, 2)}%")
                # logging.info(f"Accuracy is {round(accuracy * 100, 2)}%")


