'''
A Sine Language subclass to recieve messages over audio devices.

Alex Calamaro
Carleton College
'''
import os
import pyaudio 
import struct
import math
import binascii #get hex values from packed structs

rate = 44100

class Receiver:
    def __init__(self):
        self.something = 5000