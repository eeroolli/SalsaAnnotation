import streamlit as st

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
    print(ch)
    chore = []
    for item in ch:
        chore = chore + [item, item]
    return chore
    