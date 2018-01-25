#import libraries
from enum import Enum
from .ADS1x15 import ADS1015
import SDL_Pi_HDC1000
import time
import RPi.GPIO as GPIO
import serial

# setting raspberry pi pinmode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
##-----setting pin------
statusPin = 13
power_key = 12
relay1 = 21
relay2 = 26
luxChannel = 0
opto1 = 20
opto2 = 19
    
port = "/dev/ttyS0"

GPIO.setup(statusPin, GPIO.IN)
GPIO.setup(power_key, GPIO.OUT)
hdc = SDL_Pi_HDC1000.SDL_Pi_HDC1000()

class switchStatus(Enum):
    OFF = False
    ON = True



class opto(Enum):
    opto1 = 20
    opto2 = 19

#defining 

def lux():
    rawLux = adc(luxChannel)    
    lux = rawLux*100/1580
    return lux
def temperature():
    return hdc.readTemperature()

def humidity():    
    return hdc.readHumidity()

def relay(relayNumber,status):
    assert ( (relayNumber == 1) or (relayNumber == 2) ), "Only use 1 or 2 for relayNumber"
    assert ( (status == 0) or (status == 1) ), "Only use 0 or 1 for status"
    if relayNumber == 1:
	pin = relay1
    if relayNumber == 2:
	pin = relay2
    GPIO.setup(pin, GPIO.OUT)
    return GPIO.output(pin, status)


def status():
    def turnModuleOn():
        GPIO.output(power_key, 1)
        time.sleep(2)
        GPIO.output(power_key, 0)
        time.sleep(2)

    def checkStatus():
        status = GPIO.input(statusPin)
        if status == 0:
            print "Module turned OFF"
        else:
            print "Module turned ON"
        time.sleep(0.1)
        return status

    status = checkStatus()

    if status == 0:
        turnModuleOn()

'''
def connectivity(string):
    ser = serial.Serial(port, baudrate=115200, timeout=0.5)
    ser.write(string+'\r')
    #ser.write('AT\r')
    ser.readline()
    return ser.readline()
    time.sleep(1)
'''

def adc(channelNumber):
    assert  0 <= channelNumber <= 3 , "Only use 0,1,2,3(channel Number) for adc(channelNumber) function"
    adc = ADS1015(address=0x49, busnum=1)
    adcValues = [0] * 4
    adcValues[channelNumber] = adc.read_adc(channelNumber, gain=1)
    return adcValues[channelNumber]

def optoRead(optoNumber):
    assert ( (optoNumber == 1) or (optoNumber == 2) ), "Only use 1 or 2 for pinNumber"
    if optoNumber == 1:
        pin = opto1
    if optoNumber == 2:
	pin = opto2
    GPIO.setup(pin, GPIO.IN)
    return GPIO.input(pin)
