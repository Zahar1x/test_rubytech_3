import os
import pathlib


basedir = pathlib.Path(__file__).parent.resolve()

SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'monitoring.db'}"
SQLALCHEMY_TRACK_MODIFICATIONS = False

NUM_LOG_LINES = 20
LOG_PATH = os.getcwd()
