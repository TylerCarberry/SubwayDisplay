import time


def ellipsis_string(string, max_length):
    if len(string) <= max_length:
        return string
    return string[:max_length-3] + "..."


def get_minutes_until_arrival(timestamp):
    return int((timestamp - time.time()) / 60)
