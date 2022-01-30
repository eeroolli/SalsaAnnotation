# It assumes OpenPose was built before
import os
import glob
import config
import pandas as pd
from global_ import PATH_OUTPUT

from configparser import ConfigParser, ExtendedInterpolation
cfg = ConfigParser(interpolation=ExtendedInterpolation())
cfg.read('config.ini')

ind_coreo = "1"  #TODO it needs to be defined as external parameter

# Functions
def rename_json():
  # Better names for JSON
  paths_json = glob.glob(os.path.join(PATH_OUTPUT, "json", "*.json"))
  paths_json = sorted(paths_json, reverse=True)
  print("there are ", len(paths_json), " json files to rename")

  for old_file in paths_json:
    frame_number = old_file[-21:-15]  # counting backwards is safest, because folder names change
    new_file_name = os.path.join(PATH_OUTPUT, "json") + "/frame-" + frame_number + ".json"
    os.rename(old_file, new_file_name)

  print(" ")
  print("json are renamed")
  print("============================== ")
  print(" ")

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

def run_openpose():
  # TODO check if open pose was built before, check folder where needs to be built
  run_openpose = "./build/examples/openpose/openpose.bin"\
                 " --number_people_max 1"\
                 " --video ../run-example/1p_Gustavo_Front_h920.mp4"\
                 " --write_json ../run-example/json/"\
                 " --display 0"\ 
                 " --write_video ../run-example/output.avi"

  run_transf = "ffmpeg -y -loglevel info"\
               " -i ../run-example/output.avi"\
               " ../run-example/output.mp4"

  os.system(run_openpose)
  os.system(run_transf)

run_openpose()
rename_json()




# Make a Data Frame from the current video, how to modify for several videos?
#TODO declare all the names of the data files in the config file
PATH_DATA = os.path.join(PATH_OUTPUT, "Data.csv")
df_all = pd.read_csv(PATH_DATA)
cut_df = df_all.copy()
cut_df = cut_frame(cut_df)
csv_file_cut = os.path.join(PATH_OUTPUT, "Data_concat_cut.csv")
cut_df.to_csv(csv_file_cut , index=False)
