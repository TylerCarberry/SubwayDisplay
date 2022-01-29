import os
import time

import drawing
import nltk

from model.direction import Direction
from model.line import Line

TOP_NORTH_NAME = "Uptown"
TOP_SOUTH_NAME = "Downtown"
BOTTOM_NORTH_NAME = "Queens"
BOTTOM_SOUTH_NAME = "Brooklyn"

nltk.download('punkt')

try:
    os.mkdir("test")
except:
    pass

try:
    os.mkdir("test/output")
except:
    pass


now = int(time.time())

def no_upcoming():
    top = Line("A", Direction(TOP_NORTH_NAME, []), Direction(TOP_SOUTH_NAME, []), [])
    bottom = Line("C", Direction(BOTTOM_NORTH_NAME, []), Direction(BOTTOM_SOUTH_NAME, []), [])

    drawing.create_image(
        top,
        bottom,
        "test/output/no_upcoming.png"
    )


def many_upcoming():
    top = Line("A", Direction(TOP_NORTH_NAME, [now + 90, now + 120, now + 180, now + 280]), Direction(TOP_SOUTH_NAME, [now + 90, now + 120, now + 180]), [])
    bottom = Line("C", Direction(BOTTOM_NORTH_NAME, [now + 90, now + 120, now + 180, now + 280]), Direction(BOTTOM_SOUTH_NAME, [now + 90, now + 120, now + 180]), [])

    drawing.create_image(
        top,
        bottom,
        "test/output/many_upcoming.png"
    )


def many_upcoming_alerts():
    top = Line("A", Direction(TOP_NORTH_NAME, [now + 90, now + 120, now + 180, now + 280]), Direction(TOP_SOUTH_NAME, [now + 90, now + 120, now + 180]), ["Broken Elevator", "Station Improvements"])
    bottom = Line("C", Direction(BOTTOM_NORTH_NAME, [now + 90, now + 120, now + 180, now + 280]), Direction(BOTTOM_SOUTH_NAME, [now + 90, now + 120, now + 180]), [])

    drawing.create_image(
        top,
        bottom,
        "test/output/many_upcoming_alerts.png"
    )


def no_upcoming_alerts():
    top = Line("A", Direction(TOP_NORTH_NAME, []), Direction(TOP_SOUTH_NAME, []), ["Broken Elevator", "Station Improvements"])
    bottom = Line("C", Direction(BOTTOM_NORTH_NAME, []), Direction(BOTTOM_SOUTH_NAME, []), ["Delays", "Weekend Service"])

    drawing.create_image(
        top,
        bottom,
        "test/output/no_upcoming_alerts.png"
    )


no_upcoming()
many_upcoming()
no_upcoming_alerts()
many_upcoming_alerts()