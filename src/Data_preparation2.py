import os
import pandas as pd
import numpy as np
import sys
from global_ import video_id, PATH_OUTPUT
from configparser import ConfigParser, ExtendedInterpolation
cfg = ConfigParser(interpolation=ExtendedInterpolation())
cfg.read('src/config.ini')

# Input arguments
EXECUTION_ARGUMENTS_N = len(sys.argv)-1
print(f"The number of arguments given is {EXECUTION_ARGUMENTS_N}" )
if EXECUTION_ARGUMENTS_N == 2:
  print(f"The given arguments are used to parse the annotation.")
  video_id = sys.argv[1]
  output_analysis = sys.argv[2]
elif EXECUTION_ARGUMENTS_N != 2:
  print(f"There should be 2 arguments. Using the info from config.ini file, instead.")
  video_id = cfg.get("click_frame", "video_id")
  output_analysis = cfg.get("click_frame", "output_dir") 


DATA_CUT_NAME = cfg.get('output_data', 'json_cut_df')
DATA_PATH = os.path.join(output_analysis, DATA_CUT_NAME)
data = pd.read_csv(DATA_PATH)

cols = ['nose_x', 'nose_y', 'neck_x',
       'neck_y', 'rshoulder_x', 'rshoulder_y', 'relbow_x', 'relbow_y',
       'rwrist_x', 'rwrist_y', 'lshoulder_x', 'lshoulder_y', 'lelbow_x',
       'lelbow_y', 'lwrist_x', 'lwrist_y', 'midhip_x', 'midhip_y', 'rhip_x',
       'rhip_y', 'rknee_x', 'rknee_y', 'rankle_x', 'rankle_y', 'lhip_x',
       'lhip_y', 'lknee_x', 'lknee_y', 'lankle_x', 'lankle_y', 'reye_x',
       'reye_y', 'leye_x', 'leye_y', 'rear_x', 'rear_y', 'lear_x', 'lear_y',
       'lbigtoe_x', 'lbigtoe_y', 'lsmalltoe_x', 'lsmalltoe_y', 'lheal_x',
       'lheal_y', 'rbigtoe_x', 'rbigtoe_y', 'rsmalltoe_x', 'rsmalltoe_y',
       'rheal_x', 'rheal_y']

# Add column for the figure ID
# Figure ID is used to to do shuffle between the figures keeping the frames that belong to one figure together

ind_start = data[data['status'] == "S"].index.tolist()
ind_end = data[data['status'] == "E"].index.tolist()

def get_id(row_ind):
    l_bound = np.array(ind_start) <= row_ind
    h_bound = np.array(ind_end) >= row_ind

    intersect = np.where(l_bound * h_bound)
    return intersect[0][0]

data = data.assign(figure_id=lambda x: x.index)
data['figure_id'] = data['figure_id'].map(lambda row: get_id(row))

# Replace "0" by NaN in with numpy
# Use pandas to do linear interpolat0ion of NaN values

data[cols] = data[cols].replace({0.:np.nan})
data.interpolate(method='linear', columns=cols, inplace=True)

clip_names = list(data["clip_name"].unique())

# Reduce the jitter with Smoothing per video
from scipy.signal import savgol_filter
import numpy as np
np.set_printoptions(precision=2)  # For compact display.
window_length = 9
polyorder = 2

for i in clip_names:
    for j in cols:
        data.loc[ data["clip_name"] == i, j] = savgol_filter(
            data.loc[ data["clip_name"] == i, j],
            window_length,
            polyorder,
            mode='nearest')

# Normalization
def normalize(array):
    max_value = np.max(array)
    min_value = np.min(array)
    diff = max_value - min_value
    normalized = (array - min_value) / diff
    return normalized

for i in clip_names:
     data.loc[ data["clip_name"] == i, cols] = normalize(data.loc[ data["clip_name"] == i, cols])

# In case of training the model we need to shuffle by figures
# Saving particular example of data
file_name = cfg.get('output_data', 'norm_df')
DATA_NORMALIZED_PATH = os.path.join(output_analysis, file_name)
data.to_csv(DATA_NORMALIZED_PATH)





