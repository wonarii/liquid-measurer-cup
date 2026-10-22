#----------------------------------IMPORTS--------------------------------------------
import time

#For the load cell
import board
import digitalio

#For sounds
import array
import math
import audiocore
import board
import audiobusio

#new synth stuff
import synthio
import audiomixer
import math

from adafruit_hx711.analog_in import AnalogIn
from adafruit_hx711.hx711 import HX711

#------------------------------VARIABLES----------------------------------------------

# LOAD CELL
data = digitalio.DigitalInOut(board.SDA)
data.direction = digitalio.Direction.INPUT
clock = digitalio.DigitalInOut(board.SCL)
clock.direction = digitalio.Direction.OUTPUT

hx711 = HX711(data, clock)
channel_a = AnalogIn(hx711, HX711.CHAN_A_GAIN_128)
# channel_b = AnalogIn(hx711, HX711.CHAN_B_GAIN_32)

#the average reading when there's nothing on the scale
resetValue = 504700
#512 500 at home
#computation lab: 504700
#how i calculate the mass
slope = 350

# AUDIO

# Screaming
frequency = 500
frequencyOffset = 100
frequencyScaler = 2.5
sample_rate = 10000
tone_volume = 0.1  # Increase or decrease this to adjust the volume of the tone.
length = sample_rate // frequency  # One frequency period
sine_wave = array.array("H", [0] * length)
for i in range(length):
    sine_wave[i] = int((math.sin(math.pi * 2 * frequency * i / sample_rate) *
                        tone_volume + 1) * (2 ** 15 - 1))





#Audio synth
audio = audiobusio.I2SOut(bit_clock=board.A3, word_select=board.A2, data=board.A1)


mixer = audiomixer.Mixer(sample_rate=44100, buffer_size=2048)

synth = synthio.Synthesizer(sample_rate=44100)
audio.play(mixer)
mixer.voice[0].play(synth)
mixer.voice[0].level = 0.1



#on startup
#little wakeup song
startupSequence = True

#3 notes
note1 = 58
note2 = 63
note3 = 65





#--------------------------CODE-----------------------------------------------------

while True:
    #startupSequence = False

#----- STARTUP SONG -------
    print(startupSequence)
    if startupSequence == True:
        synth.press(note1)  # midi note 65 = F4
        time.sleep(0.3)
        synth.release(note1)  # release the note we pressed
        synth.press(note2)  # midi note 65 = F4
        time.sleep(0.1)
        synth.release(note2)  # release the note we pressed
        synth.press(note3)  # midi note 65 = F4
        time.sleep(0.5)
        synth.release(note3)  # release the note we pressed
	time.sleep(0.2)
        startupSequence = False
	print("end song")

#------ MEASURED SCREAMING --------
    if startupSequence == False:
	
	# read value on scale
    	print(f"Reading: {channel_a.value}")
    	#calculating gram/mL value
    	mass = (channel_a.value - resetValue)/slope
    	print(f"Value: {mass}mL")

	#change note to match value
	# note must be between 0-127
	#note = int(math.fabs(mass))
        note = 80 #45 is approved big speaker


	#play sound
	
        synth.press(note)  # midi note 65 = F4
        time.sleep(0.1)
        synth.release(note)  # release the note we pressed
        time.sleep(0.2)
	




    