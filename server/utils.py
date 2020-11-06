import json
import time


current_time = None

def ellipsis_string(string, max_length):
    if len(string) <= max_length:
        return string
    return string[:max_length-3] + "..."


def get_minutes_until_arrival(timestamp):
    the_time = get_current_time()
    return int((timestamp - the_time) / 60)


def get_config_file():
    with open('config.json') as f:
        return json.load(f)


def get_current_time():
    if current_time is None:
        return time.time()
    return current_time
