import argparse
import os
from configparser import ConfigParser, ExtendedInterpolation
cfg = ConfigParser(interpolation=ExtendedInterpolation())
cfg.read('config.ini')
import global_
import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser(description='Prediction script')
    parser.add_argument(
        '--video', required=True,
        help='Video_ID', type=str)

    return parser.parse_args()

args = parse_args()
global_.video_id = args.video
global_.PATH_OUTPUT = cfg.get('folders', 'output_predict_dir')
global_.PATH_OUTPUT = global_.PATH_OUTPUT + "_" + global_.video_id

if __name__ == '__main__':
    # TODO here, scripts of Eero for resizing and creating the folder structure
    # Create json file etc
    # It assumes that after this step the resize fideo with format
    if not os.path.isdir(global_.PATH_OUTPUT):
        os.makedirs(global_.PATH_OUTPUT)
    else:
        print("Folder already exists ...")

    # TODO: define the body parts of open pose in a single file

    # import Click_Frame        # Manual assignment of star-end of a figure

    # Transformation of assignment to json format
    run_annot = "python AnnotationFile_t.py "\
                + global_.PATH_OUTPUT
    os.system(run_annot)

    # import OpenPose_run     # Running Openpose, renaming json files

    # Create data frame from json files and Annotation.json
    Anot_file = global_.PATH_OUTPUT + "/Annotation.json"
    run_parsing = "python Parsing-Openpose-Annotation.py " \
                  + global_.video_id \
                  + " " \
                  + global_.PATH_OUTPUT \
                  + " " \
                  + Anot_file
    os.system(run_parsing)

    import Data_preparation   # Normalization, missing values, remove jettering

    # Running the model
    file_name = cfg.get('output_data', 'norm_df')
    PATH_DATA_VAL = os.path.join(global_.PATH_OUTPUT, file_name)
    data_val = pd.read_csv(PATH_DATA_VAL)

    from Inference import *
    X_val, y_val, info_val = transf_data(data_val)

    for i in range(X_val.shape[0]):
        #TODO, define a better format for the output
        prediction, label = check_pred(X_val[i])
        print(f"Prediction {prediction}")
        print(f"Label {label}")

    print("Done ...")



