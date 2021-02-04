import textwrap

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from nltk import sent_tokenize

import utils


MAX_ALERTS_TO_SHOW = 5
MAX_ALERT_LINE_LENGTH = 20

BLACK_COLOR = (0, 0, 0)

BIG_FONT = ImageFont.truetype('fonts/Roboto-Medium.ttf', 48)
SMALL_FONT = ImageFont.truetype('fonts/Roboto-Regular.ttf', 30)
ALERT_FONT = ImageFont.truetype('fonts/Roboto-Regular.ttf', 28)

BACKGROUND_FILE = "res/background.png"
OUTPUT_FILE = "output.png"


def create_image(top_alerts, bottom_alerts, titles, subtitles, output_file=OUTPUT_FILE):
    print(top_alerts, bottom_alerts)
    config = utils.get_config_file()

    top_alerts = process_alerts(top_alerts)
    bottom_alerts = process_alerts(bottom_alerts)

    is_active_alert = len(top_alerts) > 0 or len(bottom_alerts) > 0
    is_long_alert = max(len(top_alerts), len(bottom_alerts)) >= 3

    icon_dimensions = (120, 120) if is_active_alert else (140, 140)
    icon_x_position = 90 if is_active_alert else 60
    top_icon_y_position = 10 if len(top_alerts) >= 3 else 60 if len(top_alerts) > 0 else 95
    bottom_icon_y_position = 10 if len(bottom_alerts) >= 3 else 60 if len(bottom_alerts) > 0 else 95
    text_x_position = 320 if is_active_alert else 250

    img = Image.open(BACKGROUND_FILE)

    top_line_icon = Image.open("res/lines/{}.png".format(config["lines"][0]["name"].lower())).resize(icon_dimensions)
    bottom_line_icon = Image.open("res/lines/{}.png".format(config["lines"][1]["name"].lower())).resize(icon_dimensions)

    img.paste(top_line_icon, (icon_x_position, top_icon_y_position), mask=top_line_icon)
    img.paste(bottom_line_icon, (icon_x_position, bottom_icon_y_position + 305), mask=bottom_line_icon)

    draw = ImageDraw.Draw(img)

    SUBTITLE_MARGIN = 65

    draw.text((text_x_position, 30), titles[0], BLACK_COLOR, font=BIG_FONT)
    draw.text((text_x_position, 30+SUBTITLE_MARGIN), subtitles[0], BLACK_COLOR, font=SMALL_FONT)

    draw.text((text_x_position, 160), titles[1], BLACK_COLOR, font=BIG_FONT)
    draw.text((text_x_position, 160+SUBTITLE_MARGIN), subtitles[1], BLACK_COLOR, font=SMALL_FONT)

    draw.text((text_x_position, 330), titles[2], BLACK_COLOR, font=BIG_FONT)
    draw.text((text_x_position, 330+SUBTITLE_MARGIN), subtitles[2], BLACK_COLOR, font=SMALL_FONT)

    draw.text((text_x_position, 460), titles[3], BLACK_COLOR, font=BIG_FONT)
    draw.text((text_x_position, 460+SUBTITLE_MARGIN), subtitles[3], BLACK_COLOR, font=SMALL_FONT)

    alert_line_height = 55 if max(len(top_alerts), len(bottom_alerts)) > 3 else 80

    start_y = 300 if is_long_alert else 420
    for alert_num, l_alert in enumerate(top_alerts[:MAX_ALERTS_TO_SHOW]):
        l_alert_str = utils.ellipsis_string(l_alert, MAX_ALERT_LINE_LENGTH)
        w, h = ALERT_FONT.getsize(l_alert_str)
        draw.text(((300 - w) / 2, (start_y + alert_line_height * alert_num - h) / 2), l_alert_str, font=ALERT_FONT, fill="black")

    start_y = 920 if is_long_alert else 1050
    for alert_num, g_alert in enumerate(bottom_alerts[:MAX_ALERTS_TO_SHOW]):
        g_alert_str = utils.ellipsis_string(g_alert, MAX_ALERT_LINE_LENGTH)
        w, h = ALERT_FONT.getsize(g_alert_str)
        draw.text(((300 - w) / 2, (start_y + alert_line_height * alert_num - h) / 2), g_alert_str, font=ALERT_FONT, fill="black")

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
