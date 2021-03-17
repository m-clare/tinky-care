import os
import json
from PIL import Image, ImageDraw, ImageFont
from inky.inky_uc8159 import Inky
from datetime import datetime as dt
from bots.orgbot import get_org_image
from bots.twitterbot import get_tweet_img
from bots.twitterbot import get_recent_care_tweet
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


def save_status(data, PATH):
    with open(PATH + '/assets/status.json', 'w') as fh:
        json.dump(data, fh)


def rgb_to_inky(canvas):
    pal_img = Image.new("P", (1, 1))
    pal_img.putpalette(SATURATED_PALETTE)
    img = canvas.convert("RGB").quantize(palette=pal_img)
    inky_display.rotation = 180
    inky_display.set_image(img)
    inky_display.show()


def make_canvas(data, tweet_only, PATH):
    canvas = Image.new("RGB", (inky_display.WIDTH, inky_display.HEIGHT),
                       (255, 255, 255))
    org = Image.open(PATH + '/assets/org.png')
    canvas.paste(org, (0, 0))
    if tweet_only is True:
        tweet = get_tweet_img(376, 448, toFile=False)
    else:
        pom = get_pomodoro(data['tomato'], data['cycle'])
        tweet = get_tweet_img(376, 356, toFile=False)
        canvas.paste(pom, (org.width, tweet.height))
    canvas.paste(tweet, (org.width, 0))
    return canvas


def check_display(data, PATH):
    num_tomato, status_text = get_pomodoro_time(data['start_time'])
    tweet = get_recent_care_tweet()
    pomodoro = data['pomodoro_mode']
    reset = data['reset']
    if pomodoro is False:
        # check if twitter has changed, otherwise don't update
        if tweet != data['tweet'] or reset is True:
            data['tweet'] = tweet
            data['reset'] = False
            canvas = make_canvas(data, True, PATH)
            rgb_to_inky(canvas)
            save_status(data, PATH)
        else:
            return
    elif reset is True or (status_text != data['cycle']):
        data['tomato'] = num_tomato
        data['cycle'] = status_text
        data['tweet'] = tweet
        data['reset'] = False
        canvas = make_canvas(data, False, PATH)
        rgb_to_inky(canvas)
        save_status(data, PATH)
    else:
        return


def run_tinky_care():
    now = int(dt.utcnow().timestamp()) % 86400
    # default start values for pomodoro
    default_data = {'tomato': 0, 'cycle': 'still working',
                    'start_time': now, 'pomodoro_mode': True,
                    'reset': True,
                    'tweet': ''}
    PATH = os.path.dirname(os.path.abspath(__file__))
    if os.path.exists(PATH + '/assets/status.json'):
        with open(PATH + '/assets/status.json', 'r') as fh:
            data = json.load(fh)
            check_display(data, PATH)
    else:
        check_display(default_data, PATH)


if __name__ == "__main__":
    run_tinky_care()
