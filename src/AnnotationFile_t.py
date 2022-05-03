import json
import sys
import os
import pandas as pd
from configparser import ConfigParser, ExtendedInterpolation

cfg = ConfigParser(interpolation=ExtendedInterpolation())
cfg.read('config.ini')

PATH_DATA = sys.argv[1]
DATA = os.path.join(PATH_DATA, cfg.get('output_data', 'click_data'))
ind_coreo = int(sys.argv[2])

data_t = pd.read_csv(DATA)
frame_number = data_t["Frame"].tolist()

#TODO: this should use utils.get_choreography()
coreo = ["basic", "right-turn", "side", "cuban-basic", "suzie-q"]

#TODO: this check should happen when the clicks are made. not here.
#TODO: calculate ind coreo from len(data_t) / len(coreo). better to use data than manually fed value
if ind_coreo == 4:
    coreo = coreo * 4
    assert (data_t.shape[0] == len(coreo) * 2 + 4 or data_t.shape[0] == len(coreo) * 2 + 1), "Clicks should be 44 or 41. but found {}".format(data_t.shape[0])
elif ind_coreo == 1:
    assert data_t.shape[0] == len(coreo) * 2 + 1, "Clicks should be 11. but found {}".format(data_t.shape[0])
elif ind_coreo == 2:
    coreo = coreo * 2
    assert data_t.shape[0] == len(coreo) * 2 + 1, "Clicks should be 22. but found {}".format(data_t.shape[0])

# Forming tuples (start, end)
tuples_f = [(x, frame_number[frame_number.index(x) + 1]) for x in frame_number if frame_number.index(x) < len(frame_number) - 1]

print(f'Length Coreo {len(coreo)}')
print(f'Length Tuples {len(tuples_f)}')

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



