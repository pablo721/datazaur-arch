import datetime
import os


def compare_timestamps(refresh_rate=600, file=None):
    return file in os.listdir() and datetime.datetime.now().timestamp() - os.path.getmtime(file) < refresh_rate


def compare_dates(file):
    return file in os.listdir() and datetime.datetime.fromtimestamp(os.path.getmtime(file)).day == datetime.datetime.now().day


