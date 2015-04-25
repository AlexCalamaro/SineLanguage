#############################
# Encoder.py
# 
#
#############################
import pyaudio
import struct
import math
import wave

RATE = 44100

class Encoder:
    def __init__(self):
        #print self.outputAux.get_default_output_device_info()
        self.notelength = 1
        self.toneConstant = 250
    
    "Gets the message from the user"
    def getMessage(self):
        message = raw_input("Type your message (using lower case letters) and press enter. To quit, type q: ")
        
        return message
    
    def isMessage(self, message):
        if message != 'q':
            return True
            
    "Converts input message to list of ASCII characters"
    def convertToASCII(self, mString):
        chars = []
        for ch in mString:
            chars.append(ord(ch))
        return chars

    "Converts ASCII values to a list of frequencies for output"
    def getOutFreq(self, chars):
        frequencies = []
        for ch in chars:
            if ch==32:
                freq = 27*self.toneConstant
            else:
                freq = (ch-26)*self.toneConstant
                
            frequencies.append(freq)
        return frequencies
    
    "Generate .wav file using message data"
    def writeWave(self, frequencies):
        wfile = wave.open('message.wav', 'w')
        
        wfile.setparams((1, 2, RATE, 0, 'NONE', 'not compressed'))
        wData = ""
        
        for i in frequencies:
            for j in range(0, RATE*(self.notelength)):
                wData += struct.pack('h', 500.0*(math.sin(i)))
                #wData += struct.pack('h', 500.0*(math.sin(j*i/(RATE))))

        
        wfile.writeframes(wData)
        wfile.close()
    
    "Play .wav file"
    def playWave(self):
        #define stream chunk
        chunk = 1024
        
        #open wav file
        wFile = wave.open('C:\Users\Liz\workspace\SineLanguage\message.wav', 'rb')
        
        #instantiate pyaudio
        p = pyaudio.PyAudio()

        #open stream
        stream = p.open(format = pyaudio.get_format_from_width(wFile.getsampwidth()), channels = wFile.getnchannels(), rate = wFile.getframerate(), output = True)
        
        #read data
        data = wFile.readframes(chunk)
        
        #play stream
        while data != '':
            stream.write(data)
            data = wFile.readframes(chunk)
        
        #stop stream
        stream.stop_stream()
        stream.close()
        
        #close PyAudio
        p.terminate()
        wFile.close()
    
    def main(self):
        message = " "
        while m.isMessage(message):
            message = m.getMessage()
            amessage = m.convertToASCII(message)
            fmessage = m.getOutFreq(amessage)
            m.writeWave(fmessage)
            m.playWave()
        
m = Encoder()
m.main()

    
    