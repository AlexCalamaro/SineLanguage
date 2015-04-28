'''
A Sine Language subclass to recieve messages over audio devices.

Alex Calamaro
Carleton College

The algorithm in decode() is cannabalized from Justin Peel at:
http://stackoverflow.com/questions/2648151/python-frequency-detection
'''
import os
import sys
import pyaudio
import numpy as np
import struct
import math
import wave
import time
import binascii #get hex values from packed structs

class Receiver:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.s = None

        self.recordDuration = 1
        self.channels = 1
        self.audioFormat = pyaudio.paInt16
        self.sampleRate = 44100
        self.chunk = 1024
        self.window = np.blackman(self.chunk)

        self.sampleWidth = self.p.get_sample_size(self.audioFormat)

        self.hexChars = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']

        self.toneConstant = 100
        self.toneFloor = 400
        self.borderTone = 300
        self.freqErr = 2

        self.rawData = []
        self.frequencyData = []
        self.cleanedOutput = []

    # Calculate frequencies from raw data
    def decodeFreq(self):
        newFreq = []
        print "In decodeFreq()"

        '''
        workBuffer = []
        for i in range(self.chunk*self.sampleWidth):
            workBuffer.append(self.rawData.pop[0])
        '''

        workBuffer = self.rawData.pop(0)

        # unpack the data and times by the hamming window
        indata = np.array(wave.struct.unpack("%dh"%(len(workBuffer)/self.sampleWidth),\
                                             workBuffer))*self.window
        # Take the fft and square each value
        fftData=abs(np.fft.rfft(indata))**2
        # find the maximum
        which = fftData[1:].argmax() + 1
        # use quadratic interpolation around the max
        thefreq = None
        if which != len(fftData)-1:
            y0,y1,y2 = np.log(fftData[which-1:which+2:])
            x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
            # find the frequency and output it
            thefreq = (which+x1)*self.sampleRate/self.chunk
            #print "The freq is %f Hz." % (thefreq)
        else:
            thefreq = which*self.sampleRate/self.chunk
            #print "The freq is %f Hz." % (thefreq)

        newFreq.append(thefreq)
        #not clearing raw_data might cause repeating detected frequencies?

        self.parseFrequencyData(newFreq)

    # Clean up raw data and extract individual notes
    def parseFrequencyData(self, newData):
        acceptableSamples = []
        noRepeatSamples = []

        # Normalize data within error parameter. Ignore other samples
        for sample in newData:
            sample = sample - self.toneFloor
            if sample > self.borderTone - self.freqErr:
                sampleError = sample%self.toneConstant
                #print "Sample error: ", sampleError, "Sample: ", sample

                # Check both sides of error. Turns out the detection algorithm is pretty good
                #   so one hz of error is plenty.
                if (sampleError < self.freqErr):
                    sample = sample-sampleError
                    acceptableSamples.append(sample)

                if (self.toneConstant-sampleError < self.freqErr):
                    sample = sample + (self.toneConstant-sampleError)
                    acceptableSamples.append(sample)

        # Remove repeats in working data
        prevNote = None
        for note in acceptableSamples:
            if (note != prevNote):
                noRepeatSamples.append(note)
            prevNote = note

        #print acceptableSamples

        # Calculate hex characters from tones
        for sample in noRepeatSamples:
            sample = int(sample)

            # Special case for borderTone since I set this up like an idiot
            if (sample == self.borderTone):
                self.cleanedOutput.append('#')

            else:
                # Should convert frequency to index-of-character representation
                sample = sample - self.toneFloor
                index = sample/100

                try:
                    self.cleanedOutput.append(self.hexChars[index])
                except Exception, e:
                    pass
                    #print "Out-of-range frequencies detected"

        # Attempt to remove duplicates since in 1 second of a freq playing
        #   that frequency is recorded a lot of times. We only want one character per tone
        #   To make this easier, a bordertone needs to be inserted between any repeated chars
        #   on the sender side.
        i = 0
        if(len(self.cleanedOutput) > 1):
            while(i < len(self.cleanedOutput)-1):
                if(self.cleanedOutput[i] == self.cleanedOutput[i+1]):
                    self.cleanedOutput.pop(i+1)

        self.evaluate()

    # Handle protocol--determine which parts of message signify message type, payload, etc...
    def evaluate(self):
        if len(self.cleanedOutput) > 5:
            self.stopRecording()
        print self.cleanedOutput


    # Callback is supposedly called repeatedly until pyaudio.paComplete is returned
    #   but right now it's exiting seemingly randomly
    def getCallback(self):

        def callback(in_data, frame_count, time_info, status):
            print "In callback \r\n"
            self.rawData.append(in_data)
            self.decodeFreq()
            return (None, pyaudio.paContinue)

        return callback

    # Set up callback-infused recorder. Maybe can put the "work" here?
    def record(self):

        self.s = self.p.open(format = self.audioFormat,
                channels = self.channels,
                rate = self.sampleRate,
                input = True,
                frames_per_buffer = self.chunk,
                stream_callback = self.getCallback())

        self.s.start_stream()
        while self.s.is_active():
            time.sleep(0.1)
        return self

    def stopRecording(self):
        self.s.stop_stream()
        return self

    # Closes streams etc.
    def clean(self):
        self.s.close()
        self.p.terminate()

    def execute(self):
        self.record()

        # When done (self.clean is getting weird errors):
        #self.clean()






'''
TODO:

Recorder loops while listening for header tones to signify type and duration of incoming message.
Once those are asserted, it starts recording for the appropriate duration.

'''