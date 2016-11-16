import configparser
import os
from botanick.const import BASE_PATH

config = configparser.ConfigParser()

botanick_ini_file=os.path.join(BASE_PATH, 'botanick', 'config', 'botanick.ini')
config.read(botanick_ini_file)
