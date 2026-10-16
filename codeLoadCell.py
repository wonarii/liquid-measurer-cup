import time

import board
import digitalio

from adafruit_hx711.analog_in import AnalogIn
from adafruit_hx711.hx711 import HX711

data = digitalio.DigitalInOut(board.SDA)
data.direction = digitalio.Direction.INPUT
clock = digitalio.DigitalInOut(board.SCL)
clock.direction = digitalio.Direction.OUTPUT

hx711 = HX711(data, clock)
channel_a = AnalogIn(hx711, HX711.CHAN_A_GAIN_128)
# channel_b = AnalogIn(hx711, HX711.CHAN_B_GAIN_32)

while True:
    print(f"Reading: {channel_a.value}")
    time.sleep(1)