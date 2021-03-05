import os
import numpy
import json
from inky import InkyPHAT
from PIL import Image, ImageDraw, ImageFont
from font_fredoka_one import FredokaOne
from datetime import datetime

PATH = os.path.dirname(os.path.abspath(__file__))

try:
    ttf = ImageFont.truetype(os.getenv("DANK_MONO_ITALIC"), size=36)
except ValueError:
    ttf = ImageFont.truetype(FredokaOne)


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


def get_pomodoro_time(start_time):
    # set pomodoro cycle length
    pomodoro = 25 * 60  # typical length in seconds
    small_break = 5 * 60
    long_break = 25 * 60
    cycle_length = (pomodoro + small_break) * 3 + pomodoro + long_break
    curr_time = int(datetime.utcnow().timestamp()) % 86400
    time_since_start = curr_time - start_time
    completed_cycles = int(time_since_start // cycle_length)
    pt_in_cycle = time_since_start - completed_cycles * cycle_length
    num_tomato = int(pt_in_cycle // (pomodoro + small_break))
    if int(pt_in_cycle % (pomodoro + small_break) >= pomodoro) and \
       (num_tomato < 3):
        print(num_tomato, "break time!")
        return (num_tomato, "break time!")
    elif (pt_in_cycle > (4 * pomodoro + 3 * small_break)):
        print(num_tomato, "long break time")
        return (num_tomato, "looooong break time!")
    else:
        print(num_tomato, "still working")
        return (num_tomato, "still working")


def get_tomato_image(image_num):
    """
    Use PIL library to open tomato image and transpose for inky display
    """
    rel_path = os.path.join(PATH, "../assets/tomato_" +
                            str(image_num) + ".png")
    img = Image.open(rel_path).resize((376, 92))
    return img


def get_text_image(break_text):
    lines = format_line(ttf, break_text, 376)
    _, line_height = ttf.getsize(lines[0])
    centered_y = (92 / 2) - ((line_height * len(lines)) / 2)
    height_counter = centered_y
    img = Image.new("RGB", (376, 92), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    for i in range(0, len(lines)):
        msg = lines[i]
        w, h = ttf.getsize(msg)
        x = (376 / 2) - (w / 2)
        y = height_counter
        draw.text((x, y), msg, (0, 0, 0), ttf)
        height_counter += h
    return img

def get_pomodoro(image_num, status):
    if status == 'still working':
        return get_tomato_image(image_num)
    else:
        return get_text_image(status)
