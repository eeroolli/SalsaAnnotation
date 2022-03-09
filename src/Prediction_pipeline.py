import argparse
import os
from configparser import ConfigParser, ExtendedInterpolation
cfg = ConfigParser(interpolation=ExtendedInterpolation())
cfg.read('config.ini')
import global_
import pandas as pd
import subprocess

def parse_args():
    parser = argparse.ArgumentParser(description='Prediction script')
    parser.add_argument(
        '--video', required=True,
        help='Video_ID', type=str)
    parser.add_argument(
        '--coreo', required=True,
        help='Indice', type=str)
    parser.add_argument('--sample', choices=('True', 'False'))

    return parser.parse_args()


args = parse_args()
global_.video_id = args.video
global_.ind_coreo = args.coreo
global_.PATH_OUTPUT = cfg.get('folders', 'output_predict')
global_.PATH_OUTPUT_OP = cfg.get('folders', 'output_predict_OP')
global_.PATH_OUTPUT = global_.PATH_OUTPUT + "_" + global_.video_id
global_.sample = args.sample

if global_.sample == "True":
    global_.PATH_OUTPUT_OP = "../Sample-skeletonVideos/" + global_.video_id
else:
    global_.PATH_OUTPUT_OP = global_.PATH_OUTPUT_OP + "_" + global_.video_id



if __name__ == '__main__':
    # TODO here, scripts of Eero for resizing and creating the folder structure
    # TODO: if sample, not necessary to run the resize part

    if not os.path.isdir(global_.PATH_OUTPUT):
        os.makedirs(global_.PATH_OUTPUT)
    else:
        print("Folder already exists ...")

    global_.video_size = "h920" # this number shoulb be return from the function resize

    # Manual annotation
    import Click_Frame        # Manual assignment of star-end of a figure

    # Transformation of assignment to json format
    # TODO: better with import?
    # run_annot = "python AnnotationFile_t.py "\
    #             + global_.PATH_OUTPUT \
    #             + " " \
    #             + global_.ind_coreo
    # print(run_annot)
    # os.system(run_annot)

    subprocess.run(["python","AnnotationFile_t.py",global_.PATH_OUTPUT, global_.ind_coreo])

    # import OpenPose_run     # Running Openpose, renaming json files
    # TODO: if sample, not needed to run Openpose
    # TODO: Openpose out-put (json and mp4) in Open_Pose outpout or sample folder

    # Create data frame from json files and Annotation.json
    # TODO: replace by subprocess
    Anot_file = global_.PATH_OUTPUT + "/Annotation.json"
    run_parsing = "python Parsing-Openpose-Annotation.py " \
                  + global_.video_id \
                  + " " \
                  + global_.PATH_OUTPUT_OP \
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



