import sys
sys.path.append('src')
import config
import pandas as pd
from Inference import *

from configparser import ConfigParser, ExtendedInterpolation
cfg = ConfigParser(interpolation=ExtendedInterpolation())
cfg.read('config.ini')

output_dir = cfg.get('folders', 'output_dir')

# TODO in this line include the scripts of Eero for resizing and creating the folder structure
# include run_video_processing.py here

arg = "output" # TODO use input arguments, use classes when possible
config.VIDEO_ID = arg
# TODO: define the body parts of open pose in a single file

import Click_Frame # Manual annotation
import OpenPose_run

# Process data file: Normalization, missing values, remove jettering
import Data_preparation

# Running the model
PATH_DATA_VAL = output_dir +  "/Data_norm.csv"
data_val = pd.read_csv(PATH_DATA_VAL)

X_val, y_val, info_val = transf_data(data_val)

for i in range(X_val.shape[0]):
    prediction, label = check_pred(X_val[i])  #, label
    print(f"Prediction {prediction}")
    print(f"Label {label}")

print("Done ...")



