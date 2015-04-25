'''
A Sine Language subclass to send messages over audio devices.

Alex Calamaro and Liz Shank
Carleton College
'''
import os
import pyaudio 
import struct
import binascii #get hex values from packed structs

class Sender:
    def __init__(self):
        #print self.outputAux.get_default_output_device_info() #Prints the default output device
        self.notelength = 1
        self.toneConstant = 250
        self.freqArr = []
        
    def send(self, messageType, message):
        if (messageType == "text"):
            # Generate a text tone
            print message
            
        if (messageType == "data"):
            # Generate a data tone
            return
        
        #Send data
            
        
    def getFreqs(self,inputArr): #Should take in an input array of hexadecimal and output an array of frequencies
        return
        