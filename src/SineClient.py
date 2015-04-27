'''
Data-over-sound main class

Alex Calamaro
Carleton College
'''
import os
import sys
import pyaudio 
import struct
import binascii #get hex values from packed structs
from Sender import *
from Receiver import *

#Might want a class that handles structures of hexadecimal objects. That should simplify conversion and transmission.


class SineClient:
    def __init__(self):
        #Will need some fun things here. Maybe encryption agreement?
        self.transmitter = Sender()
        self.receiver = Receiver()
        
    def console(self):
        #User control interface. Determines if the client would like to send or receive, and subsequently
        #whether the client would like to send a file or a plain text message.
        print "text - Send plain text message \r\n",\
                "data - Specify a file to send \r\n",\
                "recv - Listen for messages \r\n",\
                "util - Utilities and tools \r\n", \
                "quit - Exit Sine Language \r\n"
        userIn = raw_input("Please select an option from above \r\n")
        
        def textInput():
            s = struct.Struct('c')
            message = raw_input("Please enter a message to send. \r\n")
            output = ""
            
            while(len(message) >= 1):
                letter = message[0]
                message = message[1:]
                output += s.pack(letter)
            hex = binascii.hexlify(output)
            print 'Packed Value   :', hex, " Length : ", len(hex)
            self.transmitter.send("text", hex)

        
        def dataInput():
            return
        
        def listen():
            self.reciever.execute()
            return
        
        def utilities():
            return

        def about():
            self.clearScreen()
            print "This program is a revision of Sine Language,\r\n",\
                "a project from the 10/13 Carleton College Hackathon.\r\n", \
                "Original Authors: Liz Shank and Alex Calamaro \r\n",\
                "Inquiries to: calamara@carleton.edu \r\n" 
        
        def exitApp():
            self.clearScreen()
            sys.exit()
        
        
        options = {     "text" : textInput,
                        "data" : dataInput,
                        "recv" : listen,
                        "util" : utilities,
                        "about": about,
                        "quit" : exitApp,
        }
        
        try:
            options[userIn]()
        except KeyError:
            print "Invalid input."
            return

                
    
            
    def listener(self):
        #Make a class for this
        return
    
    def addHeader(self, message, type):
        #adds a header with one char representing the type, n chars representing length
        # and a # representing start of data
        return
    
    def binToHex(self,binInput):
        #returns hexadecimal representation of binary input.
        print binInput
        return
    
    def hexToBin(self, hexInput):
        #returns binary representation of hexadecimal input.
        return

    def clearScreen(self):
        os.system(['clear','cls'][os.name=='nt'])
    
    def main(self):
        self.clearScreen()
        print "Welcome to Sine Language! \r\n",\

        self.console()
        
run = SineClient()
run.main()
