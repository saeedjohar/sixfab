import time
import serial
from enum import Enum
import RPi.GPIO as GPIO
from .ADS1x15 import ADS1015
import SDL_Pi_HDC1000
from mpu6050 import mpu6050

import os
import glob
import time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

OFF = False
ON = True

USER_LED_PIN		= 20
RELAY1_PIN			= 21
RELAY2_PIN			= 26
OPTO1_PIN			= 16
OPTO2_PIN			= 18
GPRS_STATUS_PIN 	= 13
GPRS_POWER_KEY_PIN 	= 12
LUX_CHANNEL			= 0

def lux():

	adc=ADS1015(address=0x49, busnum=1)
	rawLux = adc.read_adc(LUX_CHANNEL, gain=1)
	lux = (rawLux * 100) / 1580

	return lux


def setRelay(relayNumber, status):

	assert ( (relayNumber == 1) or (relayNumber == 2) ), "Only use 1 or 2 for relayNumber"

	assert ( (status == 0) or (status == 1) ), "Only use 0 or 1 for status"

	if relayNumber == 1:
		pin = RELAY1_PIN

	if relayNumber == 2:
		pin = RELAY2_PIN

	GPIO.setup(pin, GPIO.OUT)

	return GPIO.output(pin, status)


def readOpto(optoNumber):

	assert ( (optoNumber == 1) or (optoNumber == 2) ), "Only use 1 or 2 for pinNumber"


	if optoNumber == 1:
		pin = OPTO1_PIN

	if optoNumber == 2:
		pin = OPTO2_PIN

	GPIO.setup(pin, GPIO.IN)

	return GPIO.input(pin)


def readAdc(channelNumber):

	assert  0 <= channelNumber <= 3 , "Only use 0,1,2,3(channel Number) for readAdc(channelNumber) function"

	adc=ADS1015(address=0x49, busnum=1)
	adcValues = [0] * 4
	adcValues[channelNumber] = adc.read_adc(channelNumber, gain=1)

	return adcValues[channelNumber]

def temp():

	hdc1000 = SDL_Pi_HDC1000.SDL_Pi_HDC1000()
	hdc1000.setTemperatureResolution(SDL_Pi_HDC1000.HDC1000_CONFIG_TEMPERATURE_RESOLUTION_14BIT)

	return  hdc1000.readTemperature()

def humidity():

	hdc1000 = SDL_Pi_HDC1000.SDL_Pi_HDC1000()
	hdc1000.setHumidityResolution(SDL_Pi_HDC1000.HDC1000_CONFIG_HUMIDITY_RESOLUTION_14BIT)

	return hdc1000.readHumidity()

def getAccel():

	sensor = mpu6050(0x68)

	return sensor.get_accel_data()

def getGyro():

	sensor = mpu6050(0x68)

	return sensor.get_gyro_data()


def read_ds18b20_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_ds18b20():
    lines = read_ds18b20_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_ds18b20_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

def toggleLed():

	GPIO.setup(USER_LED_PIN, GPIO.OUT)
	GPIO.output(USER_LED_PIN, not GPIO.input(USER_LED_PIN))
