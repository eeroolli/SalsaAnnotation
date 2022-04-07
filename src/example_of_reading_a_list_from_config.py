from utils import keep_only_words, make_list_from_string 
from configparser import ConfigParser, ExtendedInterpolation
cfg = ConfigParser(interpolation=ExtendedInterpolation())


cfg.read('src/config.ini')

# This allows for a very sloppy notation in config ini.  It will accept almost anything and give
# it back as a list as long as there is some kind of separator between values.
coreo = make_list_from_string(cfg.get("annotation", "coreo"))

print(coreo)

op_columns = make_list_from_string(cfg.get("training", "FEATURE_COLS"))

print(op_columns)
