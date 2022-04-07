
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

