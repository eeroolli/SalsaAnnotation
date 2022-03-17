import re

def keep_only_words(messy_string):
    # keep only words, dash and white space
    clean_string = re.sub(r'[^\w\s-:]', '', messy_string)
    return clean_string


def make_list_from_string(string):
    new_list = keep_only_words(string).split()
    return new_list

