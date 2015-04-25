'''
A Sine Language subclass to send messages over audio devices.

Alex Calamaro
Carleton College
'''
import os
import pyaudio 
import struct
import math
import wave
import binascii #get hex values from packed structs

class Sender:
    def __init__(self):
        #print self.outputAux.get_default_output_device_info() #Prints the default output device
        self.notelength = 1
        self.toneConstant = 250
        self.toneFloor = 500
        self.hexChars = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
        self.sampleRate = 44100
        
    def send(self, messageType, message):
        freqArr = self.getFreqs(message)


        
        # Create new .wav file
        wFile = wave.open('message.wav', 'w')
        
        # Set it up
        wFile.setparams((1, 2, self.sampleRate, 0, 'NONE', 'not compressed'))
        wData = ""
        
        # Add data
        for i in freqArr:
            for j in range(0, self.sampleRate*(self.notelength)):
                wData += struct.pack('h', 500.0*(math.sin(i)))
                #wData += struct.pack('h', 500.0*(math.sin(j*i/(RATE))))

        # Close and reopen in read mode
        wFile.writeframes(wData)
        wFile.close()
        wFile = wave.open('message.wav','rb')
        print wFile.getsampwidth()

        # Define stream chunk
        chunk = 1024
        p = pyaudio.PyAudio()

        # Open stream
        stream = p.open(format = pyaudio.get_format_from_width(wFile.getsampwidth()), channels = wFile.getnchannels(), rate = wFile.getframerate(), output = True)
        data = wFile.readframes(chunk)
        
        #play stream
        while data != '':
            stream.write(data)
            data = wFile.readframes(chunk)
        
        #stop stream
        stream.stop_stream()
        stream.close()
        
        #close PyAudio and clean up
        p.terminate()
        wFile.close()
        os.remove('message.wav')

            
    #Should take in an input array of hexadecimal and output an array of frequencies
    def getFreqs(self,inputArr):
        freqArr = []
        for char in inputArr:
            freqArr.append(self.toneFloor + (self.hexChars.index(char))*self.toneConstant)
        
        print "Frequencies: ", freqArr
        return freqArr
        