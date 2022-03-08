# import streamlit as st
import pandas as pd
# from Inference import *

# there is a incompability with new versions of s3fs and boto3. s3fs<=0.4
# https://towardsdatascience.com/reading-and-writing-files-from-to-amazon-s3-with-pandas-ccaf90bfe86c
# python -m pip install boto3 pandas "s3fs<=0.4"
# boto3 call s3fs so it does not need to be imported separately.

import boto3

# parameters
# S3_folder = "salsaannotation/video/"
# AWS_S3_BUCKET = "salsaannotation"
# AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")


# testing if boto3 works
for bucket in boto3.resource('s3').buckets.all():    
    print(bucket.name)
    
# bucket = s3.Bucket(AWS_S3_BUCKET)
s3 = boto3.client('s3')
s3.download_file(
    Bucket="salsaannotation", 
    Key="video/Ana_skeleton_with_music.mp4",
    Filename="downloaded_from_s3.mp4" 
    )
s3.upload_file(
    Filename="visualization/1P-Ana_skeleton_subtitled.mp4",
    Bucket="salsaannotation",
    Key = "video/testing_upload_to_s3_with_boto3.mp4",
    )



# TODO: github does not allow for opening files this big. The video needs to stored in the S3 Bucket.
# skeleton_video_file = open("https://salsaannotation.s3.eu-central-1.amazonaws.com/video/Ana_skeleton_with_music.mp4", "rb")
# TODO: I have not managed to save a video to S3 from the sharelit cloud.  Perhaps sharelit needs to run on EC2?
# TODO: Try using Boto3 which is the python interface to AWS.  (I think I have done that previosly)


# Allow upload video
# def save_uploaded_file(uploaded_file):
#     try:
#         file_path = S3_folder + "/" + uploaded_file.name
#         with open(file_path,'wb') as f:
#             f.write(uploaded_file.getbuffer())
#         return 1
#     except:
#         return 0


# def get_data():
#     return []

