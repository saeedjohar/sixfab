import sixfab.nbiotshield as sixfab
import time
from threading import Timer
import urllib2
import datetime

myAPI = "2OY298JEVZOJZ9EN"


relayCounter = 0
stateRelay = False

def wait():
	sixfab.toggleLed()
	time.sleep(0.3)

baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI
print baseURL
	
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
	
	for i in range(0,20):
		wait()
	
		
	now = datetime.datetime.now()
	print str(now)
	
	for x in range(0, 3):
		try:
			f = urllib2.urlopen(baseURL + "&field1=%d&field2=%d&field3=%d&field4=%d&field5=%d&field6=%d&field7=%d&field8=%d" % (s_hdctemp, s_humidity, s_lux, s_ds18b20temp, s_accelX, s_gyroX, s_adc1, s_opto1))
			print f.read()
			f.close()
			print "send ok"
			break
		except:
			print "problem while sending"
	
