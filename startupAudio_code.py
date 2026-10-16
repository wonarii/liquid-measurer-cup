import time
import array
import math
import audiocore
import board
import audiobusio

sample_rate = 8000
tone_volume = .02  # Increase or decrease this to adjust the volume of the tone.
frequency = 200  # Set this to the Hz of the tone you want to generate.
length = sample_rate // frequency  # One freqency period
sine_wave = array.array("H", [0] * length)
for i in range(length):
    sine_wave[i] = int((math.sin(math.pi * 2 * frequency * i / sample_rate) *
                        tone_volume + 1) * (2 ** 15 - 1))

audio = audiobusio.I2SOut(board.A3, board.A2, board.A1)
sine_wave_sample = audiocore.RawSample(sine_wave, sample_rate=sample_rate)


#on startup
#little wakeup song
startupSequence = True

#3 notes
frequency1 = 400
frequency2 = 500
frequency3 = 600

sine_wave1 = array.array("H", [0] * length)
for i in range(length):
    sine_wave1[i] = int((math.sin(math.pi * 2 * frequency1 * i / sample_rate) *
                        tone_volume + 1) * (2 ** 15 - 1))
sine_wave_sample1 = audiocore.RawSample(sine_wave1, sample_rate=sample_rate)

sine_wave2 = array.array("H", [0] * length)
for i in range(length):
    sine_wave2[i] = int((math.sin(math.pi * 2 * frequency2 * i / sample_rate) *
                        tone_volume + 1) * (2 ** 15 - 1))
sine_wave_sample2 = audiocore.RawSample(sine_wave2, sample_rate=sample_rate)

sine_wave3 = array.array("H", [0] * length)
for i in range(length):
    sine_wave3[i] = int((math.sin(math.pi * 2 * frequency3 * i / sample_rate) *
                        tone_volume + 1) * (2 ** 15 - 1))
sine_wave_sample3 = audiocore.RawSample(sine_wave3, sample_rate=sample_rate)




while True:
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
	
    if startupSequence == False:
	audio.play(sine_wave_sample, loop=True)
	print("playing audio")
	time.sleep(1)
	audio.stop()
	time.sleep(1)
