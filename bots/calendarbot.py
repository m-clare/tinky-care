from dotenv import load_dotenv
from datetime import datetime, timezone
from ics import Calendar
import requests
import os
from font_fredoka_one import FredokaOne
from PIL import Image, ImageDraw, ImageFont

calendar_base = 'https://www.recurse.com/calendar/events.ics?token='
PATH = os.path.dirname(os.path.abspath(__file__))
load_dotenv(PATH + "/../mclare.env")
token = os.getenv("ICS_TOKEN")

# Set font
try:
    ttf = ImageFont.truetype(os.getenv("DANK_MONO_ITALIC"), size=32)
except ValueError:
    ttf = ImageFont.truetype(FredokaOne, size=32)

def get_next_event():
    null_event = {'name': "No events scheduled.",
                  'location': None,
                  'start': None,
                  'end': None,
                  'active': False}
    if not token:
        return null_event 
    c = Calendar(requests.get(calendar_base + token).text)
    tl = c.timeline

    for event in tl.today(): # is there a way to only retrieve a single event?
        if event.begin > datetime.now(timezone.utc) and event.status != 'CANCELLED':
            next_event = {
                'name': event.name,
                'location': event.location,
                'start': event.begin.astimezone(tz=None).strftime('%H:%M'),
                'end': event.end.astimezone(tz=None).strftime('%H:%M'),
                'active': True,
            }
            return next_event
    return null_event


def get_event_img(width, height, toFile=True):
    font = ttf
    event = get_next_event()
    if event['active'] is True:
        event_name = event['name'][:28]
        event_range = event['start'] + ' - ' + event['end']
        event_location = event['location'].split('/')[-1]
        full_text = (event_name, event_range, event_location)
    else:
        full_text = (event['name'][:28])
    lines = []
    for line in full_text:
        lines.extend(format_line(font, line, width))
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
        img.save(PATH + '/../assets/event.png', format='png')
        return img
    else:
        return


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

if __name__ == "__main__":
    img = get_event_img(376, 104)
    img.show()
