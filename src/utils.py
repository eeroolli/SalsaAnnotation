import re

def keep_only_words(messy_string):
    # keep only words, dash and white space
    clean_string = re.sub(r'[^\w\s-:]', '', messy_string)
    return clean_string


def make_list_from_string(string):
    new_list = keep_only_words(string).split()
    return new_list

    dict()

# Does not work. the function does not get the read config file from the file call the function.
# def get_list_from_config(section, item):
#     import re
#     from configparser import ConfigParser, ExtendedInterpolation
#     cfg = ConfigParser(interpolation=ExtendedInterpolation())
#     # this requires that cfg.read('the config file') has been previously run
#     messy_string = cfg.get(section, item)
#     # keep only words and white space
#     clean_string = re.sub(r'[^\w\s]', '', messy_string)
#     new_list = clean_string.split()
#     return new_list
