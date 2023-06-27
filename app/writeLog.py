import time
from datetime import date

import config


def writeLog(date_time, file_name, line):
    path = config.LOG_PATH
    file_name = str(date.today()) + '_log.log'
    with open(path + '\\' + file_name, 'a') as f:
        f.write(str(date_time) + ':' + file_name + line + '\n')
