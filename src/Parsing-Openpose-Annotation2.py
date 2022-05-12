from re import M
import pandas as pd
from pandas import concat
import numpy as np
import json
import os
from os.path import exists, join, basename, splitext
import glob
import datetime
import sys
from VideoProcessing import get_video_fps


# Input arguments
# video_id = sys.argv[1]
# output_op = sys.argv[2]
# output_analysis = sys.argv[3]
# Anot_file = sys.argv[4]

video_id = "1p_ThomasW_girl_right"
output_op = "output_op_1p/1p_ThomasW_girl_right"
output_analysis = "output_op_1p/1p_ThomasW_girl_right"
Anot_file = "output_op_1p/1p_ThomasW_girl_right/Annotation.json"


clip_name = video_id

# this is needed for get_video_fps()
video = os.path.join(output_op, "openpose.mp4")

# Data frame format for Openpose
pose_df = pd.DataFrame( columns = [
            "clip_name" ,
            "frame_nr",
            "person_id",
             "nose_x",
             "nose_y",
             "neck_x",
             "neck_y",
             "rshoulder_x",
             "rshoulder_y",
             "relbow_x",
             "relbow_y",
             "rwrist_x",
             "rwrist_y",
             "lshoulder_x",
             "lshoulder_y",
             "lelbow_x",
             "lelbow_y",
             "lwrist_x",
             "lwrist_y",
             "midhip_x",
             "midhip_y",
             "rhip_x",
             "rhip_y",
             "rknee_x",
             "rknee_y",
             "rankle_x",
             "rankle_y",
             "lhip_x",
             "lhip_y",
             "lknee_x",
             "lknee_y",
             "lankle_x",
             "lankle_y",
             "reye_x",
             "reye_y",
             "leye_x",
             "leye_y",
             "rear_x",
             "rear_y",
             "lear_x",
             "lear_y",
             "lbigtoe_x",
             "lbigtoe_y",
             "lsmalltoe_x",
              "lsmalltoe_y",
              "lheal_x",
             "lheal_y",
             "rbigtoe_x",
             "rbigtoe_y",
             "rsmalltoe_x",
             "rsmalltoe_y",
             "rheal_x",
             "rheal_y",
             "nose_v",
             "neck_v",
             "rshoulder_v",
             "relbow_v",
             "rwrist_v",
             "lshoulder_v",
             "lelbow_v",
             "lwrist_v",
             "midhip_v",
             "rhip_v",
             "rknee_v",
             "rankle_v",
             "lhip_v",
             "lknee_v",
             "lankle_v",
             "reye_v",
             "leye_v",
             "rear_v",
             "lear_v",
             "lbigtoe_v",
             "lsmalltoe_v",
             "lheal_v",
             "rbigtoe_v",
             "rsmalltoe_v",
             "rheal_v"
             ]
)

# Function to remove frames out of the coreography
def cut_frame(df_to_cut):
  # Remove all empty frames at the beginning and at the end
  index = df_to_cut.index
  conditionS = df_to_cut["status"] == "S"
  start_i = index[conditionS][0]
  conditionE = df_to_cut["status"] == "E"
  end_i = index[conditionE][len(index[conditionE])-1]
  df_to_cut = df_to_cut.loc[start_i:end_i, :]

  return df_to_cut

# Parse all json files
def json_dframe(openpose_df):
 print("----------------------")
 print(f"Parsing {output_op}")
 json_path = os.path.join(output_op, "json")
 json_files = glob.glob(json_path + '/frame*.json')
 json_files = sorted(json_files, reverse=False)
 print(f"The number of json files is {len(json_files)}")
 count_0 = 0

 for ind, file_name in enumerate(json_files):  # frames loop
  base_file_name = splitext(file_name)
  _ , frame = base_file_name[0].split("-")  # using the actual frame number in case of cutting of videos.
  frame_nr = int(frame) 
  json_text = pd.read_json(file_name)
  n_of_people = json_text["people"].count()

  assert n_of_people <= 1, "With OpenPose 1p, n of persons should be 0 or 1"

  if (n_of_people != 1):
      # print(f'Number of people {n_of_people} Frame {frame_nr}')
      count_0 += 1

  for i in range(1):  # loops through the FIRST person in one frame
   if n_of_people != 0:
       pose_keypoints = json_text.loc[i, "people"]["pose_keypoints_2d"]
       person_id = i
       nose_x, nose_y = pose_keypoints[0:2]
       neck_x, neck_y = pose_keypoints[3:5]
       rshoulder_x, rshoulder_y = pose_keypoints[6:8]
       relbow_x, relbow_y = pose_keypoints[9:11]
       rwrist_x, rwrist_y = pose_keypoints[12:14]
       lshoulder_x, lshoulder_y = pose_keypoints[15:17]
       lelbow_x, lelbow_y = pose_keypoints[18:20]
       lwrist_x, lwrist_y = pose_keypoints[21:23]
       midhip_x, midhip_y = pose_keypoints[24:26]
       rhip_x, rhip_y = pose_keypoints[27:29]
       rknee_x, rknee_y = pose_keypoints[30:32]
       rankle_x, rankle_y = pose_keypoints[33:35]
       lhip_x, lhip_y = pose_keypoints[36:38]
       lknee_x, lknee_y = pose_keypoints[39:41]
       lankle_x, lankle_y = pose_keypoints[42:44]
       reye_x, reye_y = pose_keypoints[45:47]
       leye_x, leye_y = pose_keypoints[48:50]
       rear_x, rear_y = pose_keypoints[51:53]
       lear_x, lear_y = pose_keypoints[54:56]
       lbigtoe_x, lbigtoe_y = pose_keypoints[57:59]
       lsmalltoe_x, lsmalltoe_y = pose_keypoints[60:62]
       lheal_x, lheal_y = pose_keypoints[63:65]
       rbigtoe_x, rbigtoe_y = pose_keypoints[66:68]
       rsmalltoe_x, rsmalltoe_y = pose_keypoints[69:71]
       rheal_x, rheal_y = pose_keypoints[72:74]

       nose_v = pose_keypoints[2]
       neck_v = pose_keypoints[5]
       rshoulder_v = pose_keypoints[8]
       relbow_v = pose_keypoints[11]
       rwrist_v = pose_keypoints[14]
       lshoulder_v = pose_keypoints[17]
       lelbow_v = pose_keypoints[20]
       lwrist_v = pose_keypoints[23]
       midhip_v = pose_keypoints[26]
       rhip_v = pose_keypoints[29]
       rknee_v = pose_keypoints[32]
       rankle_v = pose_keypoints[35]
       lhip_v = pose_keypoints[38]
       lknee_v = pose_keypoints[41]
       lankle_v = pose_keypoints[44]
       reye_v = pose_keypoints[47]
       leye_v = pose_keypoints[50]
       rear_v = pose_keypoints[53]
       lear_v = pose_keypoints[56]
       lbigtoe_v = pose_keypoints[59]
       lsmalltoe_v = pose_keypoints[62]
       lheal_v = pose_keypoints[65]
       rbigtoe_v = pose_keypoints[68]
       rsmalltoe_v = pose_keypoints[71]
       rheal_v = pose_keypoints[74]

       # adding variables into a Dict.
       posedata = {"clip_name": clip_name,
                   "frame_nr": frame_nr,
                   "person_id": person_id,
                   "nose_x": nose_x,
                   "nose_y": nose_y,
                   "neck_x": neck_x,
                   "neck_y": neck_y,
                   "rshoulder_x": rshoulder_x,
                   "rshoulder_y": rshoulder_y,
                   "relbow_x": relbow_x,
                   "relbow_y": relbow_y,
                   "rwrist_x": rwrist_x,
                   "rwrist_y": rwrist_y,
                   "lshoulder_x": lshoulder_x,
                   "lshoulder_y": lshoulder_y,
                   "lelbow_x": lelbow_x,
                   "lelbow_y": lelbow_y,
                   "lwrist_x": lwrist_x,
                   "lwrist_y": lwrist_y,
                   "midhip_x": midhip_x,
                   "midhip_y": midhip_y,
                   "rhip_x": rhip_x,
                   "rhip_y": rhip_y,
                   "rknee_x": rknee_x,
                   "rknee_y": rknee_y,
                   "rankle_x": rankle_x,
                   "rankle_y": rankle_y,
                   "lhip_x": lhip_x,
                   "lhip_y": lhip_y,
                   "lknee_x": lknee_x,
                   "lknee_y": lknee_y,
                   "lankle_x": lankle_x,
                   "lankle_y": lankle_y,
                   "reye_x": reye_x,
                   "reye_y": reye_y,
                   "leye_x": leye_x,
                   "leye_y": leye_y,
                   "rear_x": rear_x,
                   "rear_y": rear_y,
                   "lear_x": lear_x,
                   "lear_y": lear_y,
                   "lbigtoe_x": lbigtoe_x,
                   "lbigtoe_y": lbigtoe_y,
                   "lsmalltoe_x": lsmalltoe_x,
                   "lsmalltoe_y": lsmalltoe_y,
                   "lheal_x": lheal_x,
                   "lheal_y": lheal_y,
                   "rbigtoe_x": rbigtoe_x,
                   "rbigtoe_y": rbigtoe_y,
                   "rsmalltoe_x": rsmalltoe_x,
                   "rsmalltoe_y": rsmalltoe_y,
                   "rheal_x": rheal_x,
                   "rheal_y": rheal_y,
                   "nose_v": nose_v,
                   "neck_v": neck_v,
                   "rshoulder_v": rshoulder_v,
                   "relbow_v": relbow_v,
                   "rwrist_v": rwrist_v,
                   "lshoulder_v": lshoulder_v,
                   "lelbow_v": lelbow_v,
                   "lwrist_v": lwrist_v,
                   "midhip_v": midhip_v,
                   "rhip_v": rhip_v,
                   "rknee_v": rknee_v,
                   "rankle_v": rankle_v,
                   "lhip_v": lhip_v,
                   "lknee_v": lknee_v,
                   "lankle_v": lankle_v,
                   "reye_v": reye_v,
                   "leye_v": leye_v,
                   "rear_v": rear_v,
                   "lear_v": lear_v,
                   "lbigtoe_v": lbigtoe_v,
                   "lsmalltoe_v": lsmalltoe_v,
                   "lheal_v": lheal_v,
                   "rbigtoe_v": rbigtoe_v,
                   "rsmalltoe_v": rsmalltoe_v,
                   "rheal_v": rheal_v
                   }
       # converting dict to a series
       pose_row = pd.DataFrame(posedata, index=[0])
       #  print(pose_row)
       # data_json = {'clip_name': [clip_name] , 'frame_nr': [frame_nr], 'json_content': [json_text]}
       openpose_df = pd.concat([openpose_df, pose_row], axis=0, ignore_index=True)

   else:
       # print(f"No detected skeleton, empty json {frame_nr}")
       posedata = {"clip_name": clip_name,
                   "frame_nr": frame_nr}
       # converting dict to a series
       pose_series = pd.Series(posedata)
       # data_json = {'clip_name': [clip_name] , 'frame_nr': [frame_nr], 'json_content': [json_text]}
       openpose_df = pd.concat([openpose_df, pose_series], axis=0, ignore_index=True)

 # these belong to the loop through each frame
 print(f"The shape of the openpose_df is {openpose_df.shape}")
 print("\n")
 print("+++++++++++++++++++++++++++++++++++++++++")
 return openpose_df, count_0

# Function to transform time
def convert_time(date_time):
 format = '%M:%S'  # The format
 datetime_str = datetime.datetime.strptime(date_time, format)

 return datetime_str


def add_annot_2(df):
 # create the new columns in the data frame using time codes
 df = df.assign(label='', start='', duration='')
 frames_per_s = get_video_fps(video)
 # for every element of the json file, get: frame, duration, label
 for i in data.keys():
  for ind_j, j in enumerate(data[i]):
      print(f'j {j}')
      print(f'ind_j {ind_j}')
      start_t = convert_time(j[0])
      end_t = convert_time(j[1])
      duration = (end_t - start_t).seconds * frames_per_s  # duration in frames
      frame_ind = start_t.second * frames_per_s  # start in frames
      df.loc[frame_ind, "label"] = i
      df.loc[frame_ind, "start"] = "S"
      df.loc[frame_ind, "duration"] = duration

 return df

def add_annot_1(openpose_df, manual_annotation):
     # here the json data of the annotation  is already in "frame" format
     # create the new columns in the data frame
     df = openpose_df.assign(label='', status='')
     # for every element of the json file, get: frame, duration, label
     for i in manual_annotation.keys():
         print(i)
         for ind_j, j in enumerate(manual_annotation[i]):
             print(f'j= {j}')
             print(f'ind_j= {ind_j}')
             frame_ind = j[0] + 1  # start in frames, +1 to avoid collisions
             df.loc[frame_ind: j[1], "label"] = i
             df.loc[frame_ind, "status"] = "S"
             df.loc[j[1], "status"] = "E"

     return df

########################
# Calling the functions
#######################

pose_df, value_0 = json_dframe(pose_df)
print(pose_df.columns)
openpose_output = os.path.join(output_op, "openpose_parsed.csv")
pose_df.to_csv(openpose_output)

with open(Anot_file) as f:
  manual_annotation = json.load(f)

# TODO: get the names of the file from config init
new_df = add_annot_1(pose_df, manual_annotation=manual_annotation)
csv_file = os.path.join(output_analysis) + "/Data.csv"
new_df.to_csv(csv_file , index=False)

new_df_cut = cut_frame(new_df)
csv_file_cut = os.path.join(output_analysis) + "/Data_concat_cut.csv"
new_df_cut.to_csv(csv_file_cut , index=False)

csv_file_0 = os.path.join(output_analysis) + "/Person0.csv"
f = open(csv_file_0, "w")
f.write(str(value_0))
f.close()
