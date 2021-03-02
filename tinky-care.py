import os
from PIL import Image, ImageDraw, ImageFont
from inky.inky_uc8159 import Inky
from datetime import datetime as dt
from bots.orgbot import get_org_image
from bots.twitterbot import get_tweet_image

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


def assemble_canvas(inky, pom):
    canvas = Image.new("RGB", (inky.WIDTH, inky.HEIGHT), (255, 255, 255))
    org = Image.open('./assets/org.png')
    canvas.paste(org, (0, 0))
    tweet = Image.open('./assets/tweet.png')
    canvas.paste(tweet, (org.width, 0))

    return canvas


def check_display(inky, tomato, cycle, start_time):
    num_tomato, text = get_pomodoro_time(start_time)
    if num_tomato == tomato and text == cycle:
        return
    else:
        get_tweet_image(450, 338)
        if text == "still working":
            pom = get_tomato_image(inky, num_tomato)
        else:
            pom = get_text_image(inky, text)
        out_dict = {'num_tomato': num_tomato,
                    'status_cycle': text,
                    'start_time': start_time}
        with open(PATH + '../assets/update/status.json', 'w') as fh:
            json.dump(out_dict, fh)
        img = assemble_canvas(inky_display)
        # Inky color display conversion
        pal_img = Image.new("P", (1, 1))
        pal_img.putpalette(SATURATED_PALETTE)
        img = img.convert("RGB").quantize(palette=pal_img)
        img.show()
        inky_display.rotation = 180
        inky_display.set_image(img)
        inky_display.show()


# default start values for pomodoro
tomato = 0
cycle = 'still working'
start_time = int(datetime.utcnow().timestamp()) % 86400

if os.path.exists(PATH + '../assets/update/status.json'):
    with open(PATH + '../assets/update/status.json', 'r') as fh:
        status = json.load(fh)
        tomato = status["num_tomato"]
        cycle = status["status_cycle"]
        start_time = status['start_time']
else:
    status = {'num_tomato': tomato,
              'status_cycle': cycle,
              'start_time': start_time}
    # reset display
    img = get_tomato_image(inky_display, 0)
    inky_display.set_image(img)
    inky_display.show()
    with open(PATH + '/status.json', 'w') as fh:
        json.dump(status, fh)

check_display(inky_display, tomato, cycle, start_time)



