import signal
import RPi.GPIO as GPIO
import os
from tinkycare import run_tinky_care
from clear import clear_inky

PATH = os.path.dirname(os.path.abspath(__file__))
BUTTONS = [5, 6, 16, 24]

LABELS = ['A', 'B', 'C', 'D']

GPIO.setmode(GPIO.BCM)

GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def handle_button(pin):
    label = LABELS[BUTTONS.index(pin)]
    if label == 'A':
        # reset status if it exist
        s
        if os.path.exists(PATH + '/assets/status.json'):
            os.remove(PATH + '/assets/status.json')
        run_tinky_care()
    if label == 'D':
        clear_inky()
    if label == 'C':
        # cancel pomodoro mode
        run_tinky_care(False)
    return


for pin in BUTTONS:
    GPIO.add_event_detect(pin, GPIO.FALLING, handle_button, bouncetime=250)

signal.pause()
