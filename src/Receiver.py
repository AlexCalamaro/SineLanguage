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

        self.recordDuration = 0.25
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
            print "The freq is %f Hz." % (thefreq)
        else:
            thefreq = which*self.sampleRate/self.chunk
            print "The freq is %f Hz." % (thefreq)

        self.frequencyData.append(thefreq)
        #not clearing raw_data might cause repeating detected frequencies?

        self.parseFrequencyData()

    # Clean up raw data and extract individual notes
    def parseFrequencyData(self):
        acceptableSamples = []
        noRepeatSamples = []

        # Normalize data within error parameter. Ignore other samples
        for sample in self.frequencyData:
            sample = sample - self.toneFloor
            if sample > self.borderTone - self.freqErr:
                sampleError = sample%self.toneConstant

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

        # Calculate hex characters from tones
        for sample in noRepeatSamples:
            sample = int(sample)

            if (sample == self.borderTone):
                self.cleanedOutput.append('#')

            else:
                sample = sample - self.toneFloor
                index = sample/100
                print index
                try:
                    self.cleanedOutput.append(self.hexChars[index])
                except Exception, e:
                    print "Out-of-range frequencies detected"


        # Remove repeats in final data (stupid design but w/e)
        if len(self.cleanedOutput) > 1:
            for i in range (len(self.cleanedOutput)-1):
                if self.cleanedOutput[i] == self.cleanedOutput[i+1]:
                    self.cleanedOutput[i+1] = '$'
            while (self.cleanedOutput.count('$') > 0):
                self.cleanedOutput.remove('$')


        #print "Cleaned Samples: ", self.cleanedOutput

    # Handle protocol--determine which parts of message signify message type, payload, etc...
    def evaluate(self):
        return



    def getCallback(self):

        def callback(in_data, frame_count, time_info, status):
            print "In callback \r\n"
            self.rawData.append(in_data)
            self.decodeFreq()
            return (in_data, pyaudio.paContinue)

        return callback

    def record(self):

        self.s = self.p.open(format = self.audioFormat,
                channels = self.channels,
                rate = self.sampleRate,
                input = True,
                frames_per_buffer = self.chunk,
                stream_callback = self.getCallback())

        self.s.start_stream()
        return self

    def stopRecording(self):
        self.s.stop_stream()
        return self

    def clean(self):
        self.s.close()
        self.p.terminate()

    def execute(self):
        self.record()
        while(True):
            time.sleep(0.1)





'''
TODO:

Recorder loops while listening for header tones to signify type and duration of incoming message.
Once those are asserted, it starts recording for the appropriate duration.

'''