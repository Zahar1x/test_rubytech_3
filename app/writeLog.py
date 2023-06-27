import time
from datetime import date

import config


def writeLog(line):
    path = config.LOG_PATH
    file_name = str(date.today()) + '_log.log'
    with open(path + '\\' + file_name, 'w') as f:
        f.write(line)
