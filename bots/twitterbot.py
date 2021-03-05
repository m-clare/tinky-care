import os
import re
import emoji
import twitter
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont

PATH = os.path.dirname(os.path.abspath(__file__))
load_dotenv(PATH + '/../mclare.env')

# Set font
try:
    ttf = ImageFont.truetype(os.getenv("DANK_MONO_ITALIC"), size=36)
except ValueError:
    print("Default font not found in assets!")


def strip_emoji(text):
    new_text = re.sub(emoji.get_emoji_regexp(), r"", text)
    return new_text


def format_line(font, msg, width):
    lines = []
    w, h = font.getsize(msg)
    if w <= width:
        lines.append(msg)
    else:
        toks = msg.split()
        cur_line = ''
        for tok in toks:
            cur_w, _ = font.getsize(cur_line + tok + ' ')
            if cur_w <= width:
                cur_line = cur_line + tok + ' '
            else:
                lines.append(cur_line)
                cur_line = tok + ' '
        lines.append(cur_line)
    return lines


def get_tweet_image(width, height, toFile=True):
    font = ttf
    text = get_recent_care_tweet()
    padding = 2*10
    lines = format_line(font, text, width-padding)
    _, line_height = font.getsize(lines[0])
    centered_y = (height / 2) - ((line_height * len(lines)) / 2)
    height_counter = centered_y
    img = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    for i in range(0, len(lines)):
        msg = lines[i]
        w, h = font.getsize(msg)
        x = (width / 2) - (w / 2)
        y = height_counter
        draw.text((x, y), msg, (0, 0, 0), font)
        height_counter += h
    if toFile:
        img.save(PATH + '/../assets/tweet.png', format='png')
    else:
        return img


def get_recent_care_tweet():
    TTC_BOT = os.getenv("TTC_BOT")
    TTC_CONSUMER_KEY = os.getenv("TTC_CONSUMER_KEY")
    TTC_CONSUMER_SECRET = os.getenv("TTC_CONSUMER_SECRET")

    twit = twitter.Api(consumer_key=TTC_CONSUMER_KEY,
                       consumer_secret=TTC_CONSUMER_SECRET,
                       application_only_auth=True)

    recent_tweet = twit.GetUserTimeline(screen_name=TTC_BOT)[0].text.strip()
    recent_tweet = strip_emoji(recent_tweet)
    return recent_tweet


if __name__ == "__main__":
    get_tweet_image(400, 400)
