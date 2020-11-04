import json

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import sys
import textwrap
from nltk import sent_tokenize

import utils

DEFAULT_LEFT_POS = 220
LEFT_POS_ALERT = 320
MAX_ALERTS_TO_SHOW = 5

BLACK_COLOR = (0, 0, 0)

BIG_FONT = ImageFont.truetype('fonts/Roboto-Medium.ttf', 48)
SMALL_FONT = ImageFont.truetype('fonts/Roboto-Regular.ttf', 30)
ALERT_FONT = ImageFont.truetype('fonts/Roboto-Regular.ttf', 28)

MAX_ALERT_LINE_LENGTH = 20

OUTPUT_FILE = "output.png"

def create_image(top_alerts, bottom_alerts, titles, subtitles, output_file = OUTPUT_FILE):

    print(top_alerts, bottom_alerts)

    top_alerts = process_alerts(top_alerts)
    bottom_alerts = process_alerts(bottom_alerts)

    active_alert = len(top_alerts) > 0 or len(bottom_alerts) > 0
    if active_alert and len(top_alerts) == 0:
        top_alerts.append("Service OK")
    if active_alert and len(bottom_alerts) == 0:
        bottom_alerts.append("Service OK")

    long_alert = False
    if len(top_alerts) >= 3 or len(bottom_alerts) >= 3:
        x_top = 10
        icon_left = 90
        long_alert = True
    elif len(top_alerts) > 0 or len(bottom_alerts) > 0:
        x_top = 60
        icon_left = 90
    else:
        x_top = 95
        icon_left = 50

    left_pos = LEFT_POS_ALERT if active_alert else DEFAULT_LEFT_POS
    in_file = "res/background.png"
    img = Image.open(in_file)
    config = utils.get_config_file()

    ICON_DIMENSIONS = (120, 120)
    icon1 = Image.open("res/lines/{}.png".format(config["lines"][0]["name"].lower())).resize(ICON_DIMENSIONS)
    icon2 = Image.open("res/lines/{}.png".format(config["lines"][1]["name"].lower())).resize(ICON_DIMENSIONS)

    img.paste(icon1, (icon_left, x_top), mask=icon1)
    img.paste(icon2, (icon_left, x_top + 305), mask=icon2)

    draw = ImageDraw.Draw(img)

    SUBTITLE_MARGIN = 65

    draw.text((left_pos, 30), titles[0], BLACK_COLOR, font=BIG_FONT)
    draw.text((left_pos, 30+SUBTITLE_MARGIN), subtitles[0], BLACK_COLOR, font=SMALL_FONT)

    draw.text((left_pos, 160), titles[1], BLACK_COLOR, font=BIG_FONT)
    draw.text((left_pos, 160+SUBTITLE_MARGIN), subtitles[1], BLACK_COLOR, font=SMALL_FONT)

    draw.text((left_pos, 330), titles[2], BLACK_COLOR, font=BIG_FONT)
    draw.text((left_pos, 330+SUBTITLE_MARGIN), subtitles[2], BLACK_COLOR, font=SMALL_FONT)

    draw.text((left_pos, 460), titles[3], BLACK_COLOR, font=BIG_FONT)
    draw.text((left_pos, 460+SUBTITLE_MARGIN), subtitles[3], BLACK_COLOR, font=SMALL_FONT)

    line_height = 55 if max(len(top_alerts), len(bottom_alerts)) > 3 else 80

    start_y = 300 if long_alert else 420
    for alert_num, l_alert in enumerate(top_alerts[:MAX_ALERTS_TO_SHOW]):
        l_alert_str = utils.ellipsis_string(l_alert, MAX_ALERT_LINE_LENGTH)
        w, h = ALERT_FONT.getsize(l_alert_str)
        draw.text(((300 - w) / 2, (start_y + line_height * alert_num - h) / 2), l_alert_str, font=ALERT_FONT, fill="black")

    start_y = 920 if long_alert else 1050
    for alert_num, g_alert in enumerate(bottom_alerts[:MAX_ALERTS_TO_SHOW]):
        g_alert_str = utils.ellipsis_string(g_alert, MAX_ALERT_LINE_LENGTH)
        w, h = ALERT_FONT.getsize(g_alert_str)
        draw.text(((300 - w) / 2, (start_y + line_height * alert_num - h) / 2), g_alert_str, font=ALERT_FONT, fill="black")

    img.save(output_file)


def process_alerts(alerts):
    if "Weekday Service" in alerts:
        alerts.remove("Weekday Service")
    if len(alerts) > 2 and "Weekend Service" in alerts:
        alerts.remove("Weekend Service")
    lines = []
    for alert in alerts:
        lines.extend(process_alert(alert))
    return lines


def process_alert(alert_string):
    sentences = sent_tokenize(alert_string)
    if len(sentences) == 0:
        return ""
    wrapped = textwrap.fill(sentences[0], MAX_ALERT_LINE_LENGTH)
    return wrapped.split("\n")
