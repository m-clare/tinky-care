import os
import json
from PIL import Image, ImageDraw, ImageFont
from inky.inky_uc8159 import Inky
from datetime import datetime as dt
from bots.orgbot import get_org_image
from bots.twitterbot import get_tweet_image
from bots.pomodorobot import get_pomodoro_time
from bots.pomodorobot import get_pomodoro

# Inky display information
inky_display = Inky()  # Global because only one inky to pass around...

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


def load_status():
    with open(PATH + '/assets/update/status.json', 'r') as fh:
        status = json.load(fh)
        tomato = status["num_tomato"]
        cycle = status["status_cycle"]
        start_time = status['start_time']
    return tomato, cycle, start_time


def save_status(num_tomato, status_text, start_time):
    out_dict = {'num_tomato': num_tomato,
                'status_cycle': status_text,
                'start_time': start_time}
    with open(PATH + '/assets/update/status.json', 'w') as fh:
        json.dump(out_dict, fh)


def refresh_image(tomato, cycle):
    canvas = make_canvas(tomato, cycle)
    rgb_to_inky(canvas)


def rgb_to_inky(canvas):
    pal_img = Image.new("P", (1, 1))
    pal_img.putpalette(SATURATED_PALETTE)
    img = canvas.convert("RGB").quantize(palette=pal_img)
    inky_display.rotation = 180
    inky_display.set_image(img)
    inky_display.show()


def make_canvas(num_tomato, status_text):
    canvas = Image.new("RGB", (inky_display.WIDTH, inky_display.HEIGHT), (255, 255, 255))
    org = Image.open(PATH + '/assets/update/org.png')
    tweet = get_tweet_image(376, 356, toFile=False)
    pom = get_pomodoro(num_tomato, status_text)
    canvas.paste(org, (0, 0))
    canvas.paste(tweet, (org.width, 0))
    canvas.paste(pom, (org.width, tweet.height))
    return canvas


def check_display(tomato, cycle, start_time):
    num_tomato, status_text = get_pomodoro_time(start_time)
    if num_tomato == tomato and status_text == cycle:
        return
    else:
        # Assemble new image for update
        refresh_image(num_tomato, status_text)
        save_status(num_tomato, status_text, start_time)


def run_tinky_care():
    PATH = os.path.dirname(os.path.abspath(__file__))
    # default start values for pomodoro
    tomato = 0
    cycle = 'still working'
    start_time = int(dt.utcnow().timestamp()) % 86400
    try:
        tomato, cycle, start_time = load_status()
        check_display(tomato, cycle, start_time)
    except:
        refresh_image(tomato, cycle)
        save_status(tomato, cycle, start_time)


if __name__ == "__main__":
    run_tinky_care()





