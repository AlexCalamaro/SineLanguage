'''
A Sine Language subclass to recieve messages over audio devices.

Alex Calamaro
Carleton College
'''
import os
import pyaudio
import numpy
import struct
import math
import wave
import binascii #get hex values from packed structs

rate = 44100

class Receiver:
    def __init__(self):
        self.something = 5000


    def record(self):
    	chunk = 1024
		audioFormat = pyaudio.paInt16
		channels = 1
		sampleRate = 44100
		recordDuration = 2

    	p = pyaudio.PyAudio()
		s = p.open(format = audioFormat, 
		       channels = channels,
		       rate = sampleRate,
		       input = True, 
		       frames_per_buffer = chunk)
		d = []

		for i in range(0, (sampleRate // chunk * recordDuration)): 
		    data = s.read(chunk)
		    d.append(data)
		    #s.write(data, chunk)


		s.close()


'''
TODO:

Recorder loops while listening for header tones to signify type and duration of incoming message.
Once those are asserted, it starts recording for the appropriate duration.

'''