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
resetValue = 512500
#how i calculate the mass
slope = 350

# AUDIO

# Screaming
frequency = 200
frequencyOffset = 100
frequencyScaler = 1.5
sample_rate = 8000
tone_volume = .05  # Increase or decrease this to adjust the volume of the tone.
length = sample_rate // frequency  # One freqency period
sine_wave = array.array("H", [0] * length)
for i in range(length):
    sine_wave[i] = int((math.sin(math.pi * 2 * frequency * i / sample_rate) *
                        tone_volume + 1) * (2 ** 15 - 1))


audio = audiobusio.I2SOut(board.A3, board.A2, board.A1)


#on startup
#little wakeup song
startupSequence = True

#3 notes
frequency1 = 400
frequency2 = 500
frequency3 = 600

length1 = sample_rate // frequency1  
length2 = sample_rate // frequency2 
length3 = sample_rate // frequency3 

sine_wave1 = array.array("H", [0] * length1)
for i in range(length1):
    sine_wave1[i] = int((math.sin(math.pi * 2 * frequency1 * i / sample_rate) *
                        tone_volume + 1) * (2 ** 15 - 1))
sine_wave_sample1 = audiocore.RawSample(sine_wave1, sample_rate=sample_rate)

sine_wave2 = array.array("H", [0] * length2)
for i in range(length2):
    sine_wave2[i] = int((math.sin(math.pi * 2 * frequency2 * i / sample_rate) *
                        tone_volume + 1) * (2 ** 15 - 1))
sine_wave_sample2 = audiocore.RawSample(sine_wave2, sample_rate=sample_rate)

sine_wave3 = array.array("H", [0] * length3)
for i in range(length3):
    sine_wave3[i] = int((math.sin(math.pi * 2 * frequency3 * i / sample_rate) *
                        tone_volume + 1) * (2 ** 15 - 1))
sine_wave_sample3 = audiocore.RawSample(sine_wave3, sample_rate=sample_rate)






#--------------------------CODE-----------------------------------------------------

while True:

#----- STARTUP SONG -------
    print(startupSequence)
    if startupSequence == True:
        print("playing song")
        audio.play(sine_wave_sample1, loop=True)
	time.sleep(0.1)
	audio.stop()
	audio.play(sine_wave_sample2, loop=True)
	time.sleep(0.1)
	audio.stop()
	audio.play(sine_wave_sample3, loop=True)
	time.sleep(0.3)
	#audio.stop()
	startupSequence = False
	print("end song")

#------ MEASURED SCREAMING --------
    if startupSequence == False:
	
	# read value on scale
    	print(f"Reading: {channel_a.value}")
    	#calculating gram/mL value
    	mass = (channel_a.value - resetValue)/slope
    	print(f"Value: {mass}mL")

	#change frequency to match value
	frequency = mass * frequencyScaler + frequencyOffset
	print(frequency)
	length = int(sample_rate // frequency)
	sine_wave = array.array("H", [0] * length)
        for i in range(length):
    		sine_wave[i] = int((math.sin(math.pi * 2 * frequency * i / sample_rate) *
                        tone_volume + 1) * (2 ** 15 - 1))

	sine_wave_sample = audiocore.RawSample(sine_wave, sample_rate=sample_rate)


	#play sound
	
	audio.play(sine_wave_sample, loop=True)
	print("playing audio")
	time.sleep(1)
	#vv can remove this for a constant, annoying sound!vv
	audio.stop()

    	#amount of time it waits before reading again
    	time.sleep(0.5)






    