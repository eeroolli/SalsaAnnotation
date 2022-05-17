
# This file contains functions used for videoprocessing

def check_path(x):
  if os.path.isdir(x):
    print("Using", x )
  else:
    print("Problem: There was no ", x)  # No error keeps running


def stop_if_no_path(x):
  if os.path.isdir(x):
    print("Using", x )
  else:
    raise Exception("Problem: There was no ", x)  # Throws an error and stops



def resize_video(new_height, video_in, clip_name, src_folder):
    video_name, video_ext = splitext(clip_name)
    print("\n ################################ \n")
    print("#     Resizing the video:     ")
    print("clip_name: ", clip_name)
    print("video_name: ", video_name, " extention: ", video_ext)
    
    if os.path.isfile(video_in):
      print("Found the input video_in")
    else:
      print("The input video does not exist.")
      # raise Exception("No input video file")

    print("new hight will be: ", new_height)
    resize_output_dir = os.path.join(root_path, src_folder ,"h" + str(new_height))
    video_out = resize_output_dir + "/" + video_name + "_h" + str(new_height) + video_ext
    print("the output video will be: ", video_out)

    if not os.path.isdir(resize_output_dir):
      os.mkdir(resize_output_dir)
      print("Created a folder for resized video output:", src_folder, "/h",str(new_height) )
    else:
      print("Folder for resized video output:", src_folder, "/h",str(new_height) )
    
    if os.path.isfile(video_out):
      print("The video has been resized previously")
    else:
      print("The video is being resized, which takes often several minutes.")
      !ffmpeg -i $video_in -vf scale=-2:$new_height $video_out    # the -2 ensures that width is a even number as required
    return video_out

def get_video_fps(video):
  # Check for the speed of the video
  frames_per_s = default_fps            # if everything fails there is a default value
  if not os.path.isfile(video):
    print("There video is missing: \n ", video)
  else:
    print("OpenPose will now analyse \n", video)

  print(os.getcwd())
  text = !ffprobe -v 0 -of csv=p=0 -select_streams v:0 -show_entries stream=r_frame_rate $video 
  print(text)
  #frames, seconds = text.split("/")
  frames, seconds = text[0].split("/")
  frames_per_s = int(frames) / int(seconds)
  return frames_per_s

def load_video_run_openpose(video):
  #requires that video_id and connected variables are set.   
  print("\n ################################ \n")
  print("#     Run OpenPose:     ")
 
  frames_per_s = get_video_fps(video) 
  
  print("Number of frames per second: ", frames_per_s)
  print("\n")
  if frames_per_s > 20:
    multiplikator_for_images_per_second = frames_per_s / save_frames_per_second
  else:
    multiplikator_for_images_per_second = default_fps / save_frames_per_second
  
  # cut the parts of video that we cannot use
  # !ffmpeg -y -loglevel info -i "input_original/youtube.mp4" -ss $start_mmss -t $duration "input_original/video.mp4"
  
  # detect poses
  print(f"Video for Openpose {video}") 
  op_video = output_op_dir + "/openpose.avi"
  op_json = output_op_dir + "/json"

  if not os.path.exists(op_json): 
    !mkdir $op_json
  
  if skeleton_on_black_background==True: 
    !cd openpose && ./build/examples/openpose/openpose.bin --video $video --write_json $op_json --number_people_max 1  --display 0 --disable_blending  --write_video $op_video
  elif skeleton_on_black_background==False: 
    !cd openpose && ./build/examples/openpose/openpose.bin --video $video --write_json $op_json --number_people_max 1  --display 0  --write_video $op_video
  else:
    raise Exception("You need to set the variable skeleton_on_black_background") 

  
  # convert the result into MP4
  print(" ")
  print("============================== ")
  print("Converting the stickfigure video to mp4 ")
  print(" ")

  op_video_mp4 = output_op_dir + "/openpose.mp4"

  if os.path.isfile(op_video): 
    !ffmpeg -y -loglevel info -i $op_video $op_video_mp4 #convert avi til mp4
    os.remove(op_video)  # remove avi
  else:
    print("Something went wrong, as there was no output video from Openpose.")
    print("the output_op_dir contains:")
    print(os.listdir(output_op_dir))

  print(" ")
  print("Creating single frame images ")
  print("============================== ")
  print(" ")


def delete_outputs(video_id, root_path, output_dir):
    # delete output_files from Openpose if they were already created
    print("\n ################################ \n")
    print("Deleting old output files from the ", output_dir, video_id, " folder")
    # create a list of files to delete
    delete_files = glob.glob(os.path.join(root_path, output_dir, video_id, "json", "*.json"))
    delete_files.extend(glob.glob(os.path.join(root_path, output_dir, video_id, "*.mp4")))
    delete_files.extend(glob.glob(os.path.join(root_path, output_dir, video_id, "*.MOV")))
    # delete_files.extend(glob.glob(os.path.join(root_path, "output_op", clip_name, "*.avi")))
    # print("avi: ", delete_files[-1:])
    [os.remove(x) for x in delete_files]

    print("\n Now the output folder contains only these files:")
    print(glob.glob(os.path.join(root_path, output_dir, video_id, "json", "*.json")))


def rename_json(video_id, root_path, output_dir):
    print("\n ################################ \n")
    print("#     Rename JSON files:     ")
    ## Better names for JSON
    # find all json files and change the name
    # os.chdir(original_working_dir)
    print(os.getcwd())
    paths_json = glob.glob(os.path.join(root_path, output_dir, video_id, "json", "*.json"))
    paths_json = sorted(paths_json, reverse=True)

    print("there are ", len(paths_json), " json files to rename")
    if len(paths_json)>0:
      for old_file in paths_json:
          frame_number = old_file[-21:-15]  # counting backwards is safest, because folder names change
          # print(f"Frame {frame_number}")
          # print(f"Old name {old_file}")
          new_file_name = os.path.join(root_path, output_dir, video_id, "json") + "/frame-" + frame_number + ".json"
          # print(f"New name {new_file_name}")
          os.rename(old_file, new_file_name)

      print(" ")
      print("All json are now renamed.")
    else:
      print("nothing to be done.")  
    print("============================== ")

    # delete old names
    # [os.remove(x) for x in paths_json]
    print(" ")
    
def play_video_in_colab(video_show):
  #video_show should be a full path.
  # this only plays compressed files!
  from IPython.display import HTML
  from base64 import b64encode
  if os.path.isfile(video_show):
      print("The videofile to be shown does exist.")
      print("Note that this player is not able to play large uncompressed videos.")
  else:
      print("The videofile to be shown does NOT exist.")

  mp4 = open(video_show,'rb').read()
  data_url = "data:video/mp4;base64," + b64encode(mp4).decode()
  HTML("""
  <video width=300 controls>
        <source src="%s" type="video/mp4">
  </video>
  """ % data_url)

