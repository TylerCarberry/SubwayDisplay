import os
import drawing

TOP_NORTH_NAME = "Uptown"
TOP_SOUTH_NAME = "Downtown"
BOTTOM_NORTH_NAME = "Queens"
BOTTOM_SOUTH_NAME = "Brooklyn"

SUBTITLE_NO_TRAINS = "No upcoming trains"
SUBTITLE_SHORT = "Also 1:23"
SUBTITLE_LONG = "Also 10:10, 11:11, 11:23, 11:55"

CLOSED_CLEANING_ALERT = 'The subway is closed each night between 1 AM and 5 AM while we clean our trains and stations.    We are running extra bus service overnight, including new interborough routes.      Plan your bus trip on our homepage  . Be sure to set the time for your overnight trip, and select &quotbus&quot and &quotexpress bus&quot under Travel Preferences.'

try:
    os.mkdir("test/output")
except:
    pass

drawing.create_image(
    [CLOSED_CLEANING_ALERT],
    [CLOSED_CLEANING_ALERT],
    [TOP_NORTH_NAME, TOP_SOUTH_NAME, BOTTOM_NORTH_NAME, BOTTOM_SOUTH_NAME],
    [SUBTITLE_NO_TRAINS, SUBTITLE_NO_TRAINS, SUBTITLE_NO_TRAINS, SUBTITLE_NO_TRAINS],
    "test/output/covid_overnight.png"
)

drawing.create_image(
    [CLOSED_CLEANING_ALERT],
    [CLOSED_CLEANING_ALERT],
    [TOP_NORTH_NAME + " - 4 min", TOP_SOUTH_NAME, BOTTOM_NORTH_NAME, BOTTOM_SOUTH_NAME + " - 1 min"],
    [SUBTITLE_SHORT, SUBTITLE_NO_TRAINS, SUBTITLE_NO_TRAINS, SUBTITLE_SHORT],
    "test/output/covid_preclosing.png"
)

drawing.create_image(
    [],
    [],
    [TOP_NORTH_NAME + " - 4 min", TOP_SOUTH_NAME + " - 7 min", BOTTOM_NORTH_NAME + " - 12 min", BOTTOM_SOUTH_NAME + " - 1 min"],
    [SUBTITLE_LONG, SUBTITLE_LONG, SUBTITLE_LONG, SUBTITLE_LONG],
    "test/output/no_alerts.png"
)

drawing.create_image(
    [],
    ["Weekend Schedule"],
    [TOP_NORTH_NAME + " - 4 min", TOP_SOUTH_NAME + " - 7 min", BOTTOM_NORTH_NAME + " - 12 min", BOTTOM_SOUTH_NAME + " - 1 min"],
    [SUBTITLE_LONG, SUBTITLE_LONG, SUBTITLE_LONG, SUBTITLE_LONG],
    "test/output/weekend_schedule.png"
)

drawing.create_image(
    ["Weekend Schedule", "Delays"],
    [],
    [TOP_NORTH_NAME + " - 4 min", TOP_SOUTH_NAME + " - 7 min", BOTTOM_NORTH_NAME + " - 12 min", BOTTOM_SOUTH_NAME + " - 1 min"],
    [SUBTITLE_LONG, SUBTITLE_LONG, SUBTITLE_LONG, SUBTITLE_LONG],
    "test/output/double_alerts.png"
)

drawing.create_image(
    ["Weekend Schedule", "Broken Elevator", "Delays"],
    ["Weekend Schedule", "Broken Elevator", "Delays"],
    [TOP_NORTH_NAME + " - 4 min", TOP_SOUTH_NAME + " - 7 min", BOTTOM_NORTH_NAME + " - 12 min", BOTTOM_SOUTH_NAME + " - 1 min"],
    [SUBTITLE_LONG, SUBTITLE_LONG, SUBTITLE_LONG, SUBTITLE_LONG],
    "test/output/triple_alerts.png"
)