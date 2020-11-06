import os
import re
import requests
from google.transit import gtfs_realtime_pb2
import time
import utils

MTA_API_KEY = os.environ["MTA_API_KEY"]

# Include alerts that haven't started yet
UPCOMING_ALERT_SECONDS = 60 * 60


def get_alerts_for_line(line, include_weekend_service=False):
    output = []

    r = requests.get("https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fsubway-alerts", headers = {"x-api-key": MTA_API_KEY})

    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(r.content)

    for entity in feed.entity:
        important_alert = False
        if entity.HasField("alert"):
            alert = entity.alert

            if not is_alert_active(alert):
                continue

            for informed in alert.informed_entity:
                if informed.trip.route_id.upper() == line.upper() or informed.route_id.upper() == line.upper():
                    important_alert = True
                    break
            if important_alert:
                text = str(alert.header_text.translation).replace('text: ', "").replace('language: "EN"', "").replace('language: "en"', "").replace("\n", "")[2: -2]
                if (include_weekend_service or (text.lower() != "weekend service") and (text.lower() != "weekday service")):
                    try:
                        upper_case = max(re.findall('[A-Z ]+[ \]]', text), key=len)
                    except:
                        upper_case = ""
                    if upper_case.endswith("]"):
                        upper_case = upper_case[:-1]
                    if len(upper_case.strip()) > 4:
                        output.append(upper_case.title().strip())
                    else:
                        output.append(text.strip())
    return output


def is_alert_active(alert):
    try:
        if alert.active_period.end < utils.get_current_time():
            return False
    except:
        pass
    try:
        if alert.active_period.start > utils.get_current_time() + UPCOMING_ALERT_SECONDS:
            return False
    except:
        pass
    return True



#print("DONE")