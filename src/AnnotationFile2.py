import json
import sys
import os
import pandas as pd
from configparser import ConfigParser, ExtendedInterpolation
from utils import get_choreography
cfg = ConfigParser(interpolation=ExtendedInterpolation())
cfg.read('config.ini')
cfg.read('src/config.ini')

CLICK_DATA_PATH = cfg.get('click_frame', 'output_dir')
CLICK_DATA_FILE = os.path.join(CLICK_DATA_PATH, cfg.get('output_data', 'click_data'))

data_t = pd.read_csv(CLICK_DATA_FILE)
frame_number = data_t["Frame"].tolist()

# coreo = ["basic", "right-turn", "side", "cuban-basic", "suzie-q"]
coreo = get_choreography("coreo")

#TODO: calculate ind coreo from len(data_t) / len(coreo). better to use data than manually fed value
right_number_of_clicks_in_choreo = len(coreo)+1

if len(data_t) % right_number_of_clicks_in_choreo == 0:  # it does matter how many times the choreo is repeated.
    print(f"The number of clicks, {right_number_of_clicks_in_choreo} seems correct.")
    coreo_repetitions = len(data_t) // right_number_of_clicks_in_choreo 
    print(f"The choreo is repeated {coreo_repetitions} times in this video.")
else: 
    print(f"Annotation of {CLICK_DATA_PATH} failed.")
    sys.exit(f"The number of clicks, {right_number_of_clicks_in_choreo} does not match the choreography.")

# Forming tuples (start, end)
tuples_f = [(x, frame_number[frame_number.index(x) + 1]) for x in frame_number if frame_number.index(x) < len(frame_number) - 1]

unique_items_in_choreo = ((coreo))
print(f'Length of Choreo {unique_items_in_choreo}')
print(f'Length Tuples {len(tuples_f)}')


labels_dict = dict.fromkeys(coreo)

#TODO: What is happening here?
for i in labels_dict.keys():
    labels_dict[i] = []
for j in range(coreo_repetitions):
    for ind, i in enumerate(labels_dict.keys()):
        labels_dict[i].append(tuples_f[2 * ind + j * 10])
        labels_dict[i].append(tuples_f[2 * ind + 1 + j * 10])

def save_dict(output_op):
     Anot_file = output_op + "/Annotation.json"
     a_file = open(Anot_file, "w")
     a_file = json.dump(labels_dict, a_file)

save_dict(CLICK_DATA_PATH)



