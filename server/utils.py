import json
import time


def ellipsis_string(string, max_length):
    if len(string) <= max_length:
        return string
    return string[:max_length-3] + "..."


def get_minutes_until_arrival(timestamp):
    return int((timestamp - time.time()) / 60)


def get_config_file():
    with open('config.json') as f:
        return json.load(f)
