import json
import time
import os


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


def remove_from_string(string, items):
    for item in items:
        string = string.replace(item, " ")
    return string


def remove_duplicates_preserve_order(items):
    seen = set()
    seen_add = seen.add
    return [x for x in items if not (x in seen or seen_add(x))]


def delete_file_if_exists(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)


def is_running_on_pi():
    return os.getenv('PI') is not None
