import os
from time import sleep
from PIL import Image, ImageOps
import utils


FILE_IMAGE_WITH_BORDER = "image-with-border.png"


def format_for_kindle():
    img = Image.open('output.png')
    img = img.rotate(get_angle_config(), Image.NEAREST, expand=1, fillcolor='white')
    img_with_border = ImageOps.expand(img, border=(0, 0, 1200, 0), fill='white')
    img_with_border.resize((600, 800)).save(FILE_IMAGE_WITH_BORDER)
    os.popen("convert {} -depth 4 output2.png".format(FILE_IMAGE_WITH_BORDER))
    sleep(2)


def get_angle_config():
    return utils.get_config_file()['kindle']['angle']
