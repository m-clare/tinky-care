import signal
import RPi.GPIO as GPIO
import os
from tinkycare import run_tinky_care
from clear import clear_inky
from pathlib import Path
import contextlib
import json

PATH = os.path.dirname(os.path.abspath(__file__))
BUTTONS = [5, 6, 16, 24]

LABELS = ['A', 'B', 'C', 'D']

GPIO.setmode(GPIO.BCM)

GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def handle_button(pin):
    label = LABELS[BUTTONS.index(pin)]
    status_file = Path(PATH + '/assets/status.json')
    if label == 'A':
        with open(status_file, 'r') as file:
            data = json.load(file)
            data['reset'] = True
            data['pomodoro_mode'] = True
        with open(status_file, 'w') as file:
            json.dump(data, file)
        run_tinky_care()
    if label == 'D':
        clear_inky()
    if label == 'C':
        # cancel pomodoro mode
        with open(status_file, 'r') as file:
            data = json.load(file)
            data['pomodoro_mode'] = False
        with open(status_file, 'w') as file:
            json.dump(data, file)
        run_tinky_care()
    return


for pin in BUTTONS:
    GPIO.add_event_detect(pin, GPIO.FALLING, handle_button, bouncetime=250)

signal.pause()
