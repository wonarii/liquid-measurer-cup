# -------- Imports --------
import board
import time
import math
import gc
import json
import neopixel
import socketpool
import wifi
import audiocore
import audiobusio
import array
import synthio

# -------- Garbage Collection and Debug -------
gc.collect()
print(dir(board))

# -------- Hardware Setup --------

# Audio (I2S) Setup
sample_rate = 8000
audio = audiobusio.I2SOut(
    bit_clock=board.A0,
    word_select=board.A1,
    data=board.A3
)

# Melody Setup
volume = 0.035
volumeModifier = 1
durationMultiplier = 1

env = synthio.Envelope(
    sustain_level=0.02,
)

synth = synthio.Synthesizer(sample_rate=44100, envelope=env)
audio.play(synth)

melody = [
    (72, 0.5, volume),
    (72, 0.5, volume),
    (72, 0.5, volume),
    (0, 0.5, 0),
    (72, 0.25, volume),
    (71, 0.25, volume),
    (69, 0.25, volume),
    (71, 0.25, volume),
    (72, 0.25, volume),
    (74, 0.5, volume),
    (76, 0.5, volume),
    (76, 0.5, volume),
    (76, 0.5, volume),
    (0, 0.5, 0),
    (76, 0.25, volume),
    (74, 0.25, volume),
    (72, 0.25, volume),
    (74, 0.25, volume),
    (76, 0.25, volume),
    (77, 0.5, volume),
    (79, 1, volume),
    (72, 1, volume),
]

currentNote = 0
melodyLength = len(melody)

# Neopixel LEDS
NUM_LEDS = 8
np = neopixel.NeoPixel(board.A2, NUM_LEDS, brightness=0.1)

# -------- Distance + Timing Settings --------
MAX_DISTANCE = 2
MIN_INTERVAL = 200
MAX_INTERVAL = 2000
last_beep_time = time.monotonic()

# -------- Helper Functions --------

def clamp_distance(distance):
    if distance == float('inf'):
        return MAX_DISTANCE
    return max(0, min(distance, MAX_DISTANCE))


def interval_from_distance(distance):
    distance = clamp_distance(distance)
    ratio = distance / MAX_DISTANCE
    return int(MIN_INTERVAL + (ratio * (MAX_INTERVAL - MIN_INTERVAL)))


def leds_from_distance(distance):
    distance = clamp_distance(distance)
    ratio = 1 - (distance / MAX_DISTANCE)
    led_count = math.ceil(ratio * NUM_LEDS)

    np.fill((0, 0, 0))

    den = max(1, led_count - 1)

    for i in range(led_count):
        t = i / den

        r = int(255 - (127 * t))
        g = int(255 * (1 - t))
        b = int(128 * t)

        np[i] = (r, g, b)

    np.show()


# -------- Audio --------

def playNote():
    global currentNote

    midi_note, duration, base_vol = melody[currentNote]

    vol = base_vol * volumeModifier
    duration *= durationMultiplier

    note = synthio.Note(
        frequency=synthio.midi_to_hz(midi_note),
        amplitude=vol
    )

    synth.press(note)
    time.sleep(duration)
    synth.release(note)

    time.sleep(0.05)
    currentNote = (currentNote + 1) % melodyLength


def update_audio(distance):
    global volumeModifier, durationMultiplier

    dist = clamp_distance(distance)

    if dist == 0:
        volumeModifier = 1
        durationMultiplier = 1
    else:
        volumeModifier = max(0.01, min(1 / dist, 1))
        durationMultiplier = max(0.75, min(dist, 1.25))

    playNote()


# -------- Access Point --------
AP_SSID = "hello"
AP_PASSWORD = "password"
PORT = 12345

print("Starting access point...")
wifi.radio.start_ap(ssid=AP_SSID, password=AP_PASSWORD)
print("AP IP:", wifi.radio.ipv4_address_ap)

try:
    pool = socketpool.SocketPool(wifi.radio)
    sock = pool.socket(pool.AF_INET, pool.SOCK_DGRAM)
    sock.bind((str(wifi.radio.ipv4_address_ap), PORT))

    while True:
        buffer = bytearray(1024)

        try:
            length, client_addr = sock.recvfrom_into(buffer)
        except OSError as e:
            print("Receive error:", e)
            continue

        data = buffer[:length]
        info = json.loads(data)

        distance = info["dist"]

        # LEDs
        leds_from_distance(distance)

        print("Distance:", distance)

        # Audio
        now = time.monotonic()
        interval = interval_from_distance(distance) / 1000

        if (now - last_beep_time) >= interval:
            update_audio(distance)
            last_beep_time = now

        time.sleep(0.1)

finally:
    try:
        sock.close()
    except:
        pass

    try:
        audio.stop()
    except:
        pass

    try:
        np.fill((0, 0, 0))
        np.show()
    except:
        pass

    print("All systems shut down.")
