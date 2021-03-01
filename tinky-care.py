import os
from PIL import Image, ImageDraw, ImageFont
from inky.inky_uc8159 import Inky
from datetime import datetime as dt

# Inky display information
inky_display = Inky()

DESATURATED_PALETTE = (0, 0, 0,
                       255, 255, 255,
                       0, 255, 0,
                       0, 0, 255,
                       255, 0, 0,
                       255, 255, 0,
                       255, 140, 0,
                       255, 255, 255) + (0, 0, 0) * 248

SATURATED_PALETTE = (57, 48, 57,
                     255, 255, 255,
                     58, 91, 70,
                     61, 59, 94,
                     156, 72, 75,
                     208, 190, 71,
                     177, 106, 73,
                     255, 255, 255) + (0, 0, 0) * 248

MID_PALETTE = tuple(sum(x) // 2 for x in zip(DESATURATED_PALETTE,
                                             SATURATED_PALETTE))


def set_blank_background(width, height):
    canvas = Image.new("RGB", (width, height))
    pixels = canvas.load()
    for x in range(canvas.size[0]):
        for y in range(canvase_size[1]):
            pixles[x, y] = (255, 255, 255)
    return canvas


def assemble_canvas(inky):
    canvas = Image.new("RGB", (inky.WIDTH, inky.HEIGHT), (255, 255, 255))
    org = Image.open('./assets/org.png')
    canvas.paste(org, (0, 0))
    tweet = Image.open('./assets/tweet.png')
    canvas.paste(tweet, (org.width, 0))
    return canvas


def update_canvas_component(bot=None):
    if bot == org:
        pass
    if bot == tweet:
        pass


img = assemble_canvas(inky_display)
# Inky color display conversion
pal_img = Image.new("P", (1, 1))
pal_img.putpalette(MID_PALETTE)
img = img.convert("RGB").quantize(palette=pal_img)
img.show()
inky_display.rotation = 180
inky_display.set_image(img)
inky_display.show()
