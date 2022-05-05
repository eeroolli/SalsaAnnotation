import json
import sys
import os
import pandas as pd
from configparser import ConfigParser, ExtendedInterpolation
from utils import get_choreography
cfg = ConfigParser(interpolation=ExtendedInterpolation())
cfg.read('config.ini')
cfg.read('src/config.ini')

PATH_DATA = cfg.get('click_frame', 'output_dir')
DATA = os.path.join(PATH_DATA, cfg.get('output_data', 'click_data'))

data_t = pd.read_csv(DATA)
frame_number = data_t["Frame"].tolist()

# coreo = ["basic", "right-turn", "side", "cuban-basic", "suzie-q"]
coreo = get_choreography()

#TODO: calculate ind coreo from len(data_t) / len(coreo). better to use data than manually fed value
right_number_of_clicks_in_choreo = len(coreo)+1
if len(data_t) % right_number_of_clicks_in_choreo == 0:
    print(f"The number of clicks, {right_number_of_clicks_in_choreo} seems correct.")
else: 
    print("The number of clicks, {right_number_of_clicks_in_choreo} does not match the choreography.")

#TODO: this check should happen when the clicks are made. not here.
# if ind_coreo == 4:
#     coreo = coreo * 4
#     assert (data_t.shape[0] == len(coreo) * 2 + 4 or data_t.shape[0] == len(coreo) * 2 + 1), "Clicks should be 44 or 41. but found {}".format(data_t.shape[0])
# elif ind_coreo == 1:
#     assert data_t.shape[0] == len(coreo) * 2 + 1, "Clicks should be 11. but found {}".format(data_t.shape[0])
# elif ind_coreo == 2:
#     coreo = coreo * 2
#     assert data_t.shape[0] == len(coreo) * 2 + 1, "Clicks should be 22. but found {}".format(data_t.shape[0])

# Forming tuples (start, end)
tuples_f = [(x, frame_number[frame_number.index(x) + 1]) for x in frame_number if frame_number.index(x) < len(frame_number) - 1]

unique_items_in_choreo = ((coreo))
print(f'Length of Choreo {unique_items_in_choreo}')
print(f'Length Tuples {len(tuples_f)}')

breakpoint

lab_dic = dict.fromkeys(coreo)

for i in lab_dic.keys():
    lab_dic[i] = []
for j in range(ind_coreo):
    for ind, i in enumerate(lab_dic.keys()):
        lab_dic[i].append(tuples_f[2 * ind + j * 10])
        lab_dic[i].append(tuples_f[2 * ind + 1 + j * 10])

def save_dict(output_op):
     Anot_file = output_op + "/Annotation.json"
     a_file = open(Anot_file, "w")
     a_file = json.dump(lab_dic, a_file)

save_dict(PATH_DATA)



