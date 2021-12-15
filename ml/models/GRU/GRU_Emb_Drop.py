# Try to import Time distributed layer
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import models, layers
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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

# Define hyperparameters
BATCH_SIZE = 8
EPOCHS = 150
MAX_SEQ_LENGTH = 40   # number of frames per figure
NUM_FEATURES = 75     # number of join coordinates
no_sample = 20        # number of examples

# Import the data
PATH_DATA_TRAIN = "Data_train_validate/Data_train_norm.csv"
PATH_DATA_VAL = "Data_train_validate/Data_val_norm.csv"
data_train = pd.read_csv(PATH_DATA_TRAIN)
data_val = pd.read_csv(PATH_DATA_VAL)


# Function to select a number of frames per figure and right in the correct format for the mdoel

def transf_data(data):
    # Data preprocessing, get the input X and the label y
    ind_start = data[data['status'] == "S"].index.tolist()
    ind_end = data[data['status'] == "E"].index.tolist()

    # Take intervals between consecutive "S", they define one figure
    X = []
    y = []

    for i in range(len(ind_start) - 1):
        X.append(data.iloc[ind_start[i]: ind_end[i], 4:-3])  # the last 25 (visibility ) + 2
        y.append(data.loc[ind_start[i], 'label'])

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

    return X, y

# Train set
X_train, y_train = transf_data(data_train)
X_val, y_val = transf_data(data_val)

# Build the model
model = models.Sequential()
model.add(layers.InputLayer(input_shape=(MAX_SEQ_LENGTH, NUM_FEATURES)))
model.add(layers.GRU(128, return_sequences=True))
model.add(layers.Dropout(0.8))
model.add(layers.GRU(64))
model.add(layers.Dense(5, activation="softmax"))
model.summary()

# Compile the model
model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

# Check the trainning accuracy
history = model.fit(
    X_train,
    y_train,
    epochs=EPOCHS,
    batch_size=BATCH_SIZE,
    validation_data=(X_val, y_val)
)

# Checking accuracies
def render_history(history):
    plt.plot(history["loss"], label="loss")
    plt.plot(history["val_loss"], label="val_loss")
    plt.legend()
    plt.title("Losses")
    plt.show()
    plt.close()

    plt.plot(history["accuracy"], label="accuracy")
    plt.plot(history["val_accuracy"], label="val_accuracy")
    plt.legend()
    plt.title("Accuracies")
    plt.show()
    plt.close()

render_history(history.history)

# Prediction example
pred = model.predict( np.expand_dims(X_train[0], axis=0) )
print(f"Pred {pred}: Real Label {y_train[0]}")