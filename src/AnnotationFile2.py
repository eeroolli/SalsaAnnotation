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

# Input arguments
EXECUTION_ARGUMENTS_N = len(sys.argv)-1
print(f"The number of arguments given is {EXECUTION_ARGUMENTS_N}" )
if EXECUTION_ARGUMENTS_N==1:
  print(f"The given arguments are used to parse the annotation.")
  CLICK_DATA_PATH = sys.argv[1]
elif EXECUTION_ARGUMENTS_N != 1:
  print(f"There should be 1 argument. Using the info from config.ini file, instead.")
  CLICK_DATA_PATH = cfg.get('click_frame', 'output_dir')


ANNOTATION_FILE = os.path.join(CLICK_DATA_PATH, "Annotation.json")
data_t = pd.read_csv(CLICK_DATA_FILE)
frame_number = data_t["Frame"].tolist()

# coreo = ["basic", "right-turn", "side", "cuban-basic", "suzie-q"]
coreo = get_choreography("coreo")

#TODO: calculate ind coreo from len(data_t) / len(coreo). better to use data than manually fed value
right_number_of_clicks_in_choreo = len(coreo)+1

if len(data_t) % right_number_of_clicks_in_choreo == 0:  # it does matter how many times the choreo is repeated.
    print(f"The number of clicks, {right_number_of_clicks_in_choreo}, seems correct.")
    coreo_repetitions = len(data_t) // right_number_of_clicks_in_choreo 
    print(f"The choreo is repeated {coreo_repetitions} times in this video.")
else: 
    print(f"Annotation of {CLICK_DATA_FILE} failed.")
    sys.exit(f"The number of clicks, {right_number_of_clicks_in_choreo} does not match the choreography.")

# Forming tuples (start, end)
tuples_f = [(x, frame_number[frame_number.index(x) + 1]) for x in frame_number if frame_number.index(x) < len(frame_number) - 1]

unique_items_in_choreo = ((coreo))
print(f'The Choreo {coreo}')
print(f'Length of Tuples {len(tuples_f)}')


labels_dict = dict.fromkeys(coreo)

#TODO: What is happening here?
for i in labels_dict.keys():
    labels_dict[i] = []
    # print(labels_dict)
for j in range(coreo_repetitions):
    for ind, i in enumerate(labels_dict.keys()):
        labels_dict[i].append(tuples_f[2 * ind + j * 10])
        labels_dict[i].append(tuples_f[2 * ind + 1 + j * 10])

print(labels_dict)
def save_dict(content=labels_dict, folder=CLICK_DATA_PATH):
     ANNOTATION_FILE = folder + "/Annotation.json"
     if os.path.exists(ANNOTATION_FILE): 
        os.remove(ANNOTATION_FILE)
        print(f"{os.listdir(CLICK_DATA_PATH)}")
     a_file = open(ANNOTATION_FILE, "w")             # this always overwrites the existing file
     a_file = json.dump(content, a_file)
     if os.path.exists(ANNOTATION_FILE):
        print(f"{ANNOTATION_FILE} is saved.")

save_dict()

    




