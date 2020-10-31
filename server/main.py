import os
import nltk
import alerts
import drawing
from datetime import datetime
import json

import format_for_kindle
import gcloud
import mta
from utils import get_minutes_until_arrival
from flask import send_file
from flask import Flask

#from server import test_drawing

app = Flask(__name__)
nltk.download('punkt')


def make_also_text(timestamps):
    if len(timestamps) == 0:
        return "No upcoming trains"
    if len(timestamps) == 1:
        return ""

    times = []
    for timestamp in timestamps[1:5]:
        time_obj = datetime.fromtimestamp(timestamp)
        times.append(time_obj.strftime("%-I:%M"))
    return "Also " + ", ".join(times)


def get_header_text(direction_name, upcoming_timestamps):
    if len(upcoming_timestamps) == 0:
        return direction_name
    return "{} - {} {}".format(
        direction_name,
        get_minutes_until_arrival(upcoming_timestamps[0]),
        "min" if get_minutes_until_arrival(upcoming_timestamps[0]) == 1 else "mins"
    )


def generate_image():
    output = mta.fetch_mta()

    with open('config.json') as f:
        config = json.load(f)

    upcoming_arrival_times = []
    for line in config["lines"]:
        upcoming_arrival_times.append(sorted(output[line["stop_id"]+"N"]))
        upcoming_arrival_times.append(sorted(output[line["stop_id"]+"S"]))

    subtitles = []
    for item in upcoming_arrival_times:
        subtitles.append(make_also_text(item))

    titles = []
    for index, line in enumerate(config["lines"]):
        titles.append(get_header_text(line["uptown_name"], upcoming_arrival_times[index*2]))
        titles.append(get_header_text(line["uptown_name"], upcoming_arrival_times[index*2 + 1]))

    drawing.create_image(
        alerts.get_alerts_for_line(config["lines"][0]["name"], include_weekend_service=True),
        alerts.get_alerts_for_line(config["lines"][1]["name"], include_weekend_service=True),
        titles,
        subtitles
    )

    format_for_kindle.format_for_kindle()


@app.route('/')
def hello_world():
    generate_image()
    gcloud.upload_blob("output2.png", "image.png")
    return send_file("output2.png", cache_timeout=1)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
