
def manual_click_frame(VIDEO_FILE , 
                       OUTPUT_CSV_FILE, 
                       video_id,
                       number_of_clicks_per_choreo=11,
                       wait_ms = 40):
    import cv2
    import time
    import pandas as pd
    
    # Functions to get the state of the mouse
    def print_frame(event, x, y, flags, *userdata):
        if event == cv2.EVENT_LBUTTONDOWN:
            time_list.append(cap.get(cv2.CAP_PROP_POS_MSEC))
            frame_list.append(cap.get(cv2.CAP_PROP_POS_FRAMES))

    print(f"\n  ********************* \n  {video_id} \n  *********************")
    print("  Now you need to manually click on the image of the dancer to")
    print("  mark where the choreography STARTS, every 1st beat (count 123-567-),")
    print(f"  and where each repetition of a choreography ENDS. {number_of_clicks_per_choreo} clicks ")
    print(f"  for a choreography, turn, new {number_of_clicks_per_choreo} clicks and so fort.")
    time.sleep(4)
    print("  Grab your mouse and get ready.")
    print("  press q to quit. \n")
    time.sleep(1)


    # Extracting the frames of a video to feed MediaPipe
    cap = cv2.VideoCapture(VIDEO_FILE)
    time_list = []
    frame_list = []

    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow('frame', gray)
            cv2.setMouseCallback("frame", print_frame)

            if cv2.waitKey(wait_ms) & 0xFF == ord('q'):
                break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()

    time_list = [round(x, 2) for x in time_list]
    data_annot = pd.DataFrame(
        {"Time_ms": time_list,
        "Frame": frame_list}
    )

    # Check if the number of clicks is correct for the choreography.
    #TODO: this should be a function of the choregraphy used and not a fixed number.

    # sometimes we use videos with only one repetition of the choreography - like vier from left.
    # therefore the correct number is not always multiplied by 4.
    if len(data_annot) % number_of_clicks_per_choreo == 0:
        print("The number of clicks seems correct.")
        data_annot.to_csv(OUTPUT_CSV_FILE, index=False)   #overwrites existing csv file.
        return True
    else:
        print(f"  You did {len(data_annot)} clicks. The number should be divisible by {number_of_clicks_per_choreo}")
        print(f"  your results are NOT saved. Please rerun the script for this file.") 
        return False



def check_path(x):
  if os.path.isdir(x):
    print("Using", x )
    return True
  else:
    print("Problem: There was no ", x)  # No error keeps running
    return False

def stop_if_no_path(x):
  if os.path.isdir(x):
    print("Using", x )
  else:
    raise Exception("Problem: There was no ", x)  # Throws an error and stops

def keep_only_words(messy_string):
    import re
    # keep only words, dash and white space
    clean_string = re.sub(r'\[|\]', '', messy_string)
    clean_string = re.sub(r'\W', ' ', clean_string)
    clean_string = re.sub(r'\s+', ' ', clean_string)
    clean_string = re.sub(r'^\s|\s$', '', clean_string)
    return clean_string

def make_list_from_string(string):
    new_list = keep_only_words(string).split(sep=" ")
    return new_list


import streamlit as st
@st.cache()
def get_choreography(name_of_choreography):
    from configparser import ConfigParser, ExtendedInterpolation
    from utils import keep_only_words, make_list_from_string
    cfg = ConfigParser(interpolation=ExtendedInterpolation())
    cfg.read('src/config.ini')
    # picks it up from config.ini
    # names of figures can contain - so a particular replacement is needed.
    import re
    ch = cfg.get('annotation', name_of_choreography)
    ch = re.sub(r'\[|\]|\"|\'', '', ch)
    ch = re.sub(r'^\s|\s$', '', ch).split(sep=",")
    # print(ch)
    chore = []
    for item in ch:
        chore = chore + [item, item]
    return chore
    