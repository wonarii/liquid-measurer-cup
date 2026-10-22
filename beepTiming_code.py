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
slope = 1500 #used to be 350

# AUDIO

#Audio synth
audio = audiobusio.I2SOut(bit_clock=board.A3, word_select=board.A2, data=board.A1)


mixer = audiomixer.Mixer(sample_rate=44100, buffer_size=2048)

synth = synthio.Synthesizer(sample_rate=44100)
audio.play(mixer)
mixer.voice[0].play(synth)
mixer.voice[0].level = 0.1

#For the screaming
note = 80 #jerome's preferred sound
minTimeBeeps = 0.2 #when nothing on scale
timeBetweenBeeps = 0.2
maxTimeBeeps = 0.05 #when goal reached
slopeTimeBeeps = (maxTimeBeeps - minTimeBeeps)/100

#on startup
#little wakeup song
startupSequence = True

#3 notes
note1 = 58
note2 = 63
note3 = 65

#amount to be added to the cup
targetmL = 100

#how many times we measure to calibrate
nbMeasure = 12

#Reset Button
resetButton = digitalio.DigitalInOut(board.A0)
resetButton.direction = digitalio.Direction.INPUT
resetButton.pull = digitalio.Pull.UP

#--------------------------CODE-----------------------------------------------------

####################-------FUNCTIONS------########################################

#-----------RESET BUTTON FUNCTION----------

def reset():
    print("reset")
#reset the target amount
    targetmL = 0

#calibrate load cell

#get a bunch of measures and add them up
    sumMeasures = 0
    for i in range(nbMeasure):
        sumMeasures = channel_a.value + sumMeasures
        time.sleep(0.1)
    #calculate the average and assign it to resetValue
    resetValue = int(sumMeasures/nbMeasure)
    print("value reset to:")
    print(resetValue)
    time.sleep(2)
    
    return 

#----- STARTUP SONG FUNCTION-------
def startupSong():    
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
    return


#-------MAIN LOOP----------------


while True:
    #startupSequence = False

    print(startupSequence)
    if startupSequence == True:
        startupSong()
        startupSequence = False
        print("end song")

    if startupSequence == False:
        if not resetButton.value:   # pressed = False (pulled to GND)
	    reset()

#------ MEASURED SCREAMING --------
    if startupSequence == False:
	
	# read value on scale
    	print(f"Reading: {channel_a.value}")
    	#calculating gram/mL value
        if channel_a.value > (resetValue - 100):
    	    mass = (channel_a.value - resetValue)/slope
    	print(f"Value: {mass}mL")

	#change beep speed to match value
        #lots of safeguards here because I was getting random negative values sometimes that would crash the code
        if targetmL > 0:
	    newTimeBetweenBeeps = (100*mass/targetmL)*slopeTimeBeeps + minTimeBeeps
            if newTimeBetweenBeeps > 0:
                timeBetweenBeeps = newTimeBetweenBeeps
	    print(timeBetweenBeeps)
	#play sound
	
        synth.press(note)  # midi note 65 = F4
        time.sleep(0.1)
        synth.release(note)  # release the note we pressed
        time.sleep(timeBetweenBeeps)
	





    