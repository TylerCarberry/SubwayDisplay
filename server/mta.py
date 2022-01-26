import json
import os
from typing import Dict

import requests
from google.transit import gtfs_realtime_pb2

from model.arrival_times import ArrivalTimes
from utils import get_minutes_until_arrival

MTA_API_KEY = os.environ["MTA_API_KEY"]
MTA_BASE_URL = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-{}"

MAXIMUM_MINUTES_AWAY = 90


def fetch_mta() -> Dict[str, ArrivalTimes]:
    with open('config.json') as f:
        config = json.load(f)

    first_stop_id = config['lines'][0]['stop_id']
    second_stop_id = config['lines'][1]['stop_id']

    lines = [
        ArrivalTimes(first_stop_id[0], first_stop_id[1:], "N"),
        ArrivalTimes(first_stop_id[0], first_stop_id[1:], "S"),
        ArrivalTimes(second_stop_id[0], second_stop_id[1:], "N"),
        ArrivalTimes(second_stop_id[0], second_stop_id[1:], "S"),
    ]

    result = {item.get_stop_id(): item for item in lines}
    line_letters = set([line.line_letter.lower() for line in lines])

    for line in line_letters:
        r = requests.get(MTA_BASE_URL.format(line), headers={"x-api-key": MTA_API_KEY})
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(r.content)

        for entity in feed.entity:
            if entity.HasField('trip_update'):
                for stop in entity.trip_update.stop_time_update:
                    if stop.stop_id in result.keys():
                        mins_away = get_minutes_until_arrival(stop.arrival.time)
                        if 0 < mins_away < MAXIMUM_MINUTES_AWAY:
                            result[stop.stop_id].arrival_times.append(stop.arrival.time)

    return result
