#!/usr/bin/env python
from dweet import Dweet
import spidev
import time
from libsoc import gpio
from gpio_96boards import GPIO

GPIO_CS = GPIO.gpio_id('GPIO_CS')
RELE = GPIO.gpio_id('GPIO_A')
LED = GPIO.gpio_id('GPIO_C')
BOTAO = GPIO.gpio_id('GPIO_E')
TILT = GPIO.gpio_id('GPIO_G')

pins = ((GPIO_CS, 'out'), (RELE, 'out'), (TILT, 'in') , (BOTAO, 'in'), (LED, 'out'),)

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 10000
spi.mode = 0b00
spi.bits_per_word = 8

dweet = Dweet()

def readtemp(gpio):

	gpio.digital_write(GPIO_CS, GPIO.HIGH)
	time.sleep(0.0002)
	gpio.digital_write(GPIO_CS, GPIO.LOW)
	r = spi.xfer2([0x01, 0x80, 0x00])
	gpio.digital_write(GPIO_CS, GPIO.HIGH)
	adcout = (r[1] << 8) & 0b1100000000
	adcout = adcout | (r[2] & 0xff)		

	adc_temp = (adcout *5.0/1023-0.5)*100
	
	return adc_temp

def readLumi(gpio):

	gpio.digital_write(GPIO_CS, GPIO.HIGH)
	time.sleep(0.0002)
	gpio.digital_write(GPIO_CS, GPIO.LOW)
	r = spi.xfer2([0x01, 0xA0, 0x00])
	gpio.digital_write(GPIO_CS, GPIO.HIGH)

	adcout = (r[1] << 8) & 0b1100000000
	adcout = adcout | (r[2] & 0xff)

	return  adcout

	
def liga():

	gpio.digital_write(LED, GPIO.HIGH)
	gpio.digital_write(RELE, GPIO.HIGH)

	
def desliga():

	gpio.digital_write(LED, GPIO.LOW)
	gpio.digital_write(RELE, GPIO.LOW)


#def Botao_cloud():

	
def detectaTilt(gpio):
	status = gpio.digital_read(TILT)
	tilt_detected = 0
	sleep_count = 0
	while sleep_count < 1000:
		if gpio.digital_read(TILT) != status:
			tilt_detected += 1
			status = gpio.digital_read(TILT)
			if tilt_detected > 5:
				print("Problem Detected")
				tilt_detected = 0
				break
		sleep_count += 1
		time.sleep(0.002)


def Aut_Liga():

	liga()
	alarme = 1
	dweet.dweet_by_name(name="bm_temp", data={"alarme":alarme, "temp":vtemp, "lumi":vlumi})
	print ("botao: %d" %cloud)
	print "Sistema Automatico! \n"		
	print "Ar Condicionado Ligado"		
	print ("Temperatura: %2.1f" %vtemp)
	print ("Luminosidade: %2.1f \n" %vlumi)
	

def Aut_Des():

	desliga()	
	alarme = 0
	dweet.dweet_by_name(name="bm_temp", data={"alarme":alarme, "temp":vtemp, "lumi":vlumi})	
	print ("botao: %d" %cloud)	
	print "Sistema Automatico! \n"				
	print "Ar Condicionado Desligado"		
	print ("Temperatura: %2.1f" %vtemp)
	print ("Luminosidade: %2.1f \n" %vlumi)
	

def Manual():

	print "Sistema Manual"
	print ("Temperatura: %2.1f" %vtemp)
	print ("Luminosidade: %2.1f \n " %vlumi)



while True:
	with GPIO(pins) as gpio:
		Botao_cloud()
		vtemp = readtemp(gpio)
		vlumi = readLumi(gpio)
		resposta = dweet.latest_dweet(name="bm_temp")
		print resposta['with'][0]['content']['botao']
		botao_valor = gpio.digital_read(BOTAO)
		if botao_valor == 0: 
			if vtemp > 18:
				Aut_Liga()
				detectaTilt(gpio)
			else:
				Aut_Des()
				detectaTilt(gpio)
		else:
			Manual()
			detectaTilt(gpio)
	time.sleep(15)
        
    

