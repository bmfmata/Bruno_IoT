#!/usr/bin/env python
from dweet import Dweet
import spidev
import time
from libsoc import gpio
from gpio_96boards import GPIO

GPIO_CS = GPIO.gpio_id('GPIO_CS')
LED = GPIO.gpio_id('GPIO_A')
RELE = GPIO.gpio_id('GPIO_C')
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
		liga()
		botao_valor = gpio.digital_read(BOTAO)		
		vtemp = readtemp(gpio)
		vlumi = readLumi(gpio)
		alarme = 1
		time.sleep(0.5)	
		led_valor = gpio.digital_read(LED)
		rele_valor = gpio.digital_read(RELE)
		print ("Alarme: %d" %alarme)
		print ("Led %d" %led_valor)	
		print ("rele: %d" %rele_valor)
		print ("botao: %d" %botao_valor)		
		print ("Temperatura: %2.1f" %vtemp)
		print ("Luminosidade: %2.1f" %vlumi)
		dweet.dweet_by_name(name="bm_temp", data={"temp":vtemp})
		dweet.dweet_by_name(name="bm_temp", data={"temp":vlumi})
		resposta = dweet.latest_dweet(name="bm_temp")
		time.sleep(2)




        
    

