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

pins = ((GPIO_CS, 'out'), (RELE, 'out'), (BOTAO, 'in'), (LED, 'out'),)

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



while True:
	with GPIO(pins) as gpio:
		botao_valor = gpio.digital_read(BOTAO)
		vtemp = readtemp(gpio)
		vlumi = readLumi(gpio)
		#resposta = dweet.latest_dweet(name="bm_temp")
		#cloud = resposta['with'][0]['content']['botao']
		if botao_valor == 0:
			if vtemp > 23:
				liga()
				alarme = 1
				dweet.dweet_by_name(name="bm_temp", data={"alarme":alarme, "temp":vtemp, "lumi":vlumi})
				print "Sistema Automatico! \n"		
				print "Ar Condicionado Ligado"		
				print ("Temperatura: %2.1f" %vtemp)
				print ("Luminosidade: %2.1f \n" %vlumi)
				time.sleep(5)
			else:
				desliga()	
				alarme = 0
				dweet.dweet_by_name(name="bm_temp", data={"alarme":alarme, "temp":vtemp, "lumi":vlumi})	
				#print ("botao: %d" %cloud)	
				print "Sistema Automatico! \n"				
				print "Ar Condicionado Desligado"		
				print ("Temperatura: %2.1f" %vtemp)
				print ("Luminosidade: %2.1f \n" %vlumi)
				time.sleep(5)         		
		else:
			print "Sistema Manual"
			print ("Temperatura: %2.1f" %vtemp)
			print ("Luminosidade: %2.1f \n " %vlumi)
			time.sleep(5)

		time.sleep(1)	

        
    

