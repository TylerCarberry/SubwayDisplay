import json
import os
import requests
from google.transit import gtfs_realtime_pb2
from utils import get_minutes_until_arrival

MTA_API_KEY = os.environ["MTA_API_KEY"]
MTA_BASE_URL = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-{}"

MAXIMUM_MINUTES_AWAY = 90


def fetch_mta():
    with open('config.json') as f:
        config = json.load(f)

    lines, stops = [], []
    for line in config["lines"]:
        lines.append(line["name"].lower())
        stops.append(line["stop_id"] + "N")
        stops.append(line["stop_id"] + "S")

    output = {}
    for item in stops:
        output[item] = []

    for line in lines:
        r = requests.get(MTA_BASE_URL.format(line), headers={"x-api-key": MTA_API_KEY})

        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(r.content)
        for entity in feed.entity:
            if entity.HasField('trip_update'):
                for stop in entity.trip_update.stop_time_update:
                    if stop.stop_id in stops:
                        mins_away = get_minutes_until_arrival(stop.arrival.time)
                        if 0 < mins_away < MAXIMUM_MINUTES_AWAY:
                            output[stop.stop_id].append(stop.arrival.time)
    return output
