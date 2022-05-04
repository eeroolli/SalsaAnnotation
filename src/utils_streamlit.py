

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
    