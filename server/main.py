import os
import time
from datetime import datetime
from typing import Dict

import nltk
from flask import Flask
from flask import send_file

import alerts
import drawing
import format_for_kindle
import logs
import mta
import utils
from model.arrival_times import ArrivalTimes
from model.direction import Direction
from model.line import Line

#from server import test_drawing

app = Flask(__name__)
nltk.download('punkt')


def generate_image():
    arrival_times: Dict[str, ArrivalTimes] = mta.fetch_mta()

    config = utils.get_config_file()

    top_train = build_line_from_config(config["lines"][0], arrival_times)
    bottom_train = build_line_from_config(config["lines"][1], arrival_times)

    drawing.create_image(top_train, bottom_train)
    format_for_kindle.format_for_kindle()


def build_line_from_config(line_config: Dict, arrival_times):
    return Line(
        line_config["name"],
        Direction(line_config["uptown_name"], arrival_times[line_config["stop_id"] + "N"].arrival_times),
        Direction(line_config["downtown_name"], arrival_times[line_config["stop_id"] + "S"].arrival_times),
        alerts.get_alerts_for_line(line_config["name"])
    )


@app.route('/')
def run_gcloud():
    current_time = time.time()
    for photo_num in range(9, -1, -1):
        print(photo_num)
        make_image_for_timestamp(current_time + photo_num * 30)
        #gcloud.upload_blob("output2.png", "image{}.png".format(photo_num))
    logs.post_to_discord(datetime.now().strftime("%B %d %Y - %H:%M:%S"), "", "output.png")
    return send_file("output2.png", cache_timeout=1)


def run_locally():
    current_time = time.time()
    for photo_num in range(9, -1, -1):
        print(photo_num)
        make_image_for_timestamp(current_time + photo_num * 30)
        file_name = "image{}.png".format(photo_num)
        utils.delete_file_if_exists(file_name)
        os.rename("output2.png", file_name)
    logs.post_to_discord(datetime.now().strftime("%B %d %Y - %H:%M:%S"), "", "output.png")


def make_image_for_timestamp(timestamp):
    utils.current_time = timestamp
    generate_image()


if __name__ == "__main__":
    if utils.is_running_on_pi():
        print("Running on raspberry pi, generating images")
        run_locally()
    else:
        print("Running in the cloud, launching flask app")
        app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
