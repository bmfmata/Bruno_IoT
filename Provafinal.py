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

alarme_bebe = 0
bam_nuvem = 0
ld_nuvem = 0
reset_nuvem = 0
aux_led_liga = 0
aux_rele_liga = 0
aux_led_desliga = 0
aux_rele_desliga = 0

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


#def Leitura_nuvem():
#	global bam_nuvem, ld_nuvem, reset_nuvem
#	resposta = dweet.latest_dweet(name="bmfmata")
#	bam_nuvem = resposta['with'][0]['content']['bam_nuvem']
#	ld_nuvem = resposta['with'][0]['content']['liga_des']
#	reset_nuvem = resposta['with'][0]['content']['reset']

	
def liga():
	
	#global aux_led_liga, aux_rele_liga
	#aux_led_liga = gpio.digital_read(LED)
	#if aux_led_liga == 0: 
	gpio.digital_write(LED, GPIO.HIGH)
	#aux_rele_liga = gpio.digital_read(RELE)
	#if aux_rele_liga == 0:
	gpio.digital_write(RELE, GPIO.HIGH)

	
def desliga():

	#global aux_led_desliga, aux_rele_desliga
	#aux_led_desliga = gpio.digital_read(LED)
	#if aux_led_desliga == 1: 
	gpio.digital_write(LED, GPIO.LOW)
	#aux_rele_desliga = gpio.digital_read(RELE)
	#if aux_rele_desliga == 1:
	gpio.digital_write(RELE, GPIO.LOW)


	

#def detectaTilt(gpio):
#	global alarme_bebe
#	status = gpio.digital_read(TILT)
#	tilt_detected = 0
#	sleep_count = 0
#	while sleep_count < 1000:
#		if gpio.digital_read(TILT) != status:
#			tilt_detected += 1
#			status = gpio.digital_read(TILT)
#			if tilt_detected > 5:
#				print("Problem Detected")
#				alarme_bebe = 1
#				tilt_detected = 0
#				break
#		sleep_count += 1
#		time.sleep(0.002)
#

def Aut_Liga():

	liga()
	alarme = 1
	dweet.dweet_by_name(name="bmfmata", data={"alarme":alarme, "temp":vtemp, "lumi":vlumi, "bam_nuvem":bam_nuvem, "bebe":alarme_bebe, "reset":reset_nuvem, "liga_des":ld_nuvem,})
	print "Sistema Automatico! \n"		
	print "Ar Condicionado Ligado"		
	print ("Temperatura: %2.1f" %vtemp)
	print ("Luminosidade: %2.1f \n" %vlumi)
	

def Aut_Des():

	desliga()	
	alarme = 0
	dweet.dweet_by_name(name="bmfmata", data={"alarme":alarme, "temp":vtemp, "lumi":vlumi, "bam_nuvem":bam_nuvem, "bebe":alarme_bebe, "reset":reset_nuvem, "liga_des":ld_nuvem,})
	print "Sistema Automatico! \n"				
	print "Ar Condicionado Desligado"		
	print ("Temperatura: %2.1f" %vtemp)
	print ("Luminosidade: %2.1f \n" %vlumi)
	

def Manual():

	print "Sistema Manual"
	print ("Temperatura: %2.1f" %vtemp)
	print ("Luminosidade: %2.1f \n " %vlumi)

def Man_Liga():

	liga()
	alarme = 1
	dweet.dweet_by_name(name="bmfmata", data={"alarme":alarme, "temp":vtemp, "lumi":vlumi, "bam_nuvem":bam_nuvem, "bebe":alarme_bebe, "reset":reset_nuvem, "liga_des":ld_nuvem,})
	print "Ar Condicionado Ligado"		
	print ("Temperatura: %2.1f" %vtemp)
	print ("Luminosidade: %2.1f \n" %vlumi)

def Man_Des():

	desliga()	
	alarme = 0
	dweet.dweet_by_name(name="bmfmata", data={"alarme":alarme, "temp":vtemp, "lumi":vlumi, "bam_nuvem":bam_nuvem, "bebe":alarme_bebe, "reset":reset_nuvem, "liga_des":ld_nuvem,})
	print "Ar Condicionado Desligado"		
	print ("Temperatura: %2.1f" %vtemp)
	print ("Luminosidade: %2.1f \n" %vlumi)


while True:
	with GPIO(pins) as gpio:
		aux_led_liga = gpio.digital_read(LED)
		aux_rele_liga = gpio.digital_read(RELE)
		resposta = dweet.latest_dweet(name="bmfmata")
		bam_nuvem = resposta['with'][0]['content']['bam_nuvem']
		vtemp = readtemp(gpio)
		vlumi = readLumi(gpio)
		botao_valor = gpio.digital_read(BOTAO)
		#Leitura_nuvem()

		if botao_valor == 0:
			if vtemp > 10:
				print ("led: %d " %aux_led_liga) 
				print ("rele: %d " %aux_rele_liga)
				#if aux_led_liga and aux_rele_liga:
				Aut_Liga()
				time.sleep(10)
			else:
				Aut_Des()
				time.sleep(10)
		else:
			#detectaTilt(gpio)
			Manual()
			time.sleep(10)
			#detectaTilt(gpio)
			#if ld_nuvem == 1:
			#	Man_liga()
			#else:
			#	Man_des()
			#if reset_nuvem == 1:	
			#alarme_bebe == 0
		
		#
		#time.sleep(5)
		
        
    

