import sixfab.nbiotshield as sixfab
import time
from threading import Timer
import urllib2
import datetime
import serial


relayCounter = 0
stateRelay = False

ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)


def wait():
	sixfab.toggleLed()
	time.sleep(0.3)
	
while 1:

	ser.reset_input_buffer()

	while 1:
		ser.write("ATE0\r")
		time.sleep(1)
		response = ser.readline()
		response = ser.readline()
		print 'RESPONSE:%s' % response
		
		if response.startswith('OK'):
			break
			
	print 'TAMAMLANDI 0'
	ser.reset_input_buffer()
	
	while 1:
		ser.write("AT+CFUN=1\r")
		time.sleep(1)
		response = ser.readline()		
		response = ser.readline()
		print 'RESPONSE:%s' % response
		
		if response.startswith('OK'):
			break
			
	print 'TAMAMLANDI 1'
	
	ser.reset_input_buffer()
	
	

	while 1:
		ser.write("AT+CGATT=1\r")
		time.sleep(0.5)
		
		response = ser.readline()		
		response = ser.readline()
		print 'RESPONSE:%s' % response
		
		if response.startswith('OK'):
			break
			
		
	
	print 'TAMAMLANDI 2'
	
	ser.reset_input_buffer()
	
	
	while 1:
		ser.write("AT+CGDCONT=1,\"IP\",\"IOTTEST\"\r")
		time.sleep(1)
		
		response = ser.readline()		
		response = ser.readline()
		print 'RESPONSE:%s' % response
		
		if response.startswith('OK'):
			break
			

	print 'TAMAMLANDI 3'
	
	time.sleep(3)
	
	ser.reset_input_buffer()
	
	while 1:
		ser.write("AT+CGATT?\r")
		time.sleep(1)
		
		
		while 1:
			ser.write("AT+CGATT?\r")
			time.sleep(1)
			response = ser.readline()
			response = ser.readline()
			print 'RESPONSE:%s' % response
		
			if response.startswith('+CGATT:1'):
				break
			
		break

	print 'TAMAMLANDI 4'
	
	ser.write('AT+NSOCL=0\r')
	time.sleep(1)
	
	ser.reset_input_buffer()
	
	while 1:
		ser.write("AT+NSOCR=DGRAM,17,3005,1\r")
		time.sleep(0.5)
		
		
		while 1:
			response = ser.readline()
			response = ser.readline()
			print 'RESPONSE:%s' % response
		
			if response.startswith('OK'):
				break
				
			if response.startswith('ERROR'):
				ser.write("AT+NSOCR=DGRAM,17,3005,1\r")
			
		break

	print 'TAMAMLANDI 5'
	
	break


while 1:

	relayCounter += 1

	if relayCounter>= 5:
		relayCounter = 0
		
		if stateRelay == True:
			sixfab.setRelay(1,1)
			print "Set Relay 1 : 1"
			sixfab.setRelay(2,1)
			print "Set Relay 2 : 1"
			
			stateRelay = False
		else: 
			sixfab.setRelay(1,0)
			print "Set Relay 1 : 0"
			sixfab.setRelay(2,0)
			print "Set Relay 2 : 0"
			
			stateRelay = True
		


	s_opto1 = sixfab.readOpto(1)
	print "Opto 1 State: %d" % s_opto1

	print "Opto 2 State: %d" % sixfab.readOpto(2)
	
	s_hdctemp = sixfab.temp()
	print "HDC1080 Temp is : %d" % s_hdctemp
	
	s_humidity = sixfab.humidity()
	print "HDC1080 Humidity is : %d" % s_humidity
	
	s_lux = sixfab.lux()
	print "Lux Value is : %d" % s_lux
	
	s_ds18b20temp = sixfab.read_ds18b20()[0]
	print "DS18b20 Temp Value is : %d" % s_ds18b20temp	
	
	s_adc0 = sixfab.readAdc(0)
	print "Adc0 : %d" % s_adc0
	
	s_adc1 = sixfab.readAdc(1)
	print "Adc1 : %d" % s_adc1
	
	s_adc2 = sixfab.readAdc(2)
	print "Adc2 : %d" % s_adc2
	
	s_adc3 = sixfab.readAdc(3)
	print "Adc3 : %d" % s_adc3
	
	s_acc = sixfab.readAcc()
	print ("Acc : %d %d %d" % ( s_acc["x"] , s_acc["y"] ,s_acc["z"] ))
	
	for i in range(0,200):
		wait()
		
	now = datetime.datetime.now()
	print str(now)
	
	data = '{{"_0":{0}, "_1":{1}, "_2":{2}, "_3":{3}, "_4":{4} , "_5":{5} , "_6":{6} , "_7":{7}}}'.format(s_hdctemp, s_humidity, s_lux, s_ds18b20temp, s_acc["x"], s_acc["y"], s_adc1, s_opto1) 
	
	print data
		
        print 'DATA SENDING'
        
        data ='AT+NSOST=0,104.236.216.61,2223,{0},{1}\r'.format(str(len(data)),data.encode("hex"))
        
        ser.reset_input_buffer()
		
        ser.write(data)
        
        response = ser.readline()
        response = ser.readline()
        print 'RESPONSE:%s' % response


	
