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
        self.notelength = 0.5
        self.toneConstant = 100
        self.toneFloor = 600
        self.borderTone = 500
        self.hexChars = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
        self.sampleRate = 44100
        self.volume = 4000
        
    def send(self, messageType, message):
        freqArr = self.getFreqs(message)


        
        # Create new .wav file
        wFile = wave.open('message.wav', 'w')
        
        # Set it up
        wFile.setparams((1, 2, self.sampleRate, 0, 'NONE', 'not compressed'))
        wData = ""
        
        # Add data
        for note in freqArr:
            for sample in range(0, int(self.sampleRate*(self.notelength))):
                
                wData += struct.pack('h', self.volume*(math.sin(2*sample*note*math.pi/(self.sampleRate))))

        # Close and reopen in read mode
        wFile.writeframes(wData)
        wFile.close()
        wFile = wave.open('message.wav','rb')

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
        prevVal = 0

        #Indicates start/end of message
        freqArr.append(self.borderTone)

        for char in inputArr:
            frequency = self.toneFloor + (self.hexChars.index(char))*self.toneConstant

            # In case of repeated values, the reciever needs to be able to tell
            # that the same note is played twice, so we add a border tone
            if(frequency == prevVal):
                freqArr.append(self.borderTone)

            freqArr.append(frequency)
            prevVal = frequency
        
        freqArr.append(self.borderTone)
        print "Frequencies: ", freqArr
        return freqArr
        