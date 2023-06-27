import fnmatch
import os
from datetime import date

import config


def getLog(numLines):
    file_name = ''
    res = []
    path = config.LOG_PATH
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, str(date.today()) + '_log.log'):
                file_name = os.path.join(root, name)
    with open(file_name, 'r') as f:
        for i in range(numLines):
            res.append(f.readline())



