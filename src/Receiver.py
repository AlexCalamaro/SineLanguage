'''
A Sine Language subclass to send messages over audio devices.

Alex Calamaro and Liz Shank
Carleton College
'''
import os
import pyaudio 
import struct
import binascii #get hex values from packed structs

rate = 44100

class Receiver:
    def __init__(self):
        self.something = 5000