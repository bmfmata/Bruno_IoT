#!/usr/bin/env python
from dweet import Dweet
import spidev
import time
from libsoc import gpio
from gpio_96boards import GPIO

GPIO_CS = GPIO.gpio_id('GPIO_CS')
RELE = GPIO.gpio_id('GPIO_G')
LED = GPIO.gpio_id('GPIO_C')
BOTAO = GPIO.gpio_id('GPIO_E')


pins = ((GPIO_CS, 'out'), (RELE, 'out'), (BOTAO, 'in'), (LED, 'out'),)

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
estado_am = 0
x = 0
y = 0


def readtemp(gpio):

	gpio.digital_write(GPIO_CS, GPIO.HIGH)
	time.sleep(0.0002)
	gpio.digital_write(GPIO_CS, GPIO.LOW)
	r = spi.xfer2([0x01, 0xA0, 0x00])
	gpio.digital_write(GPIO_CS, GPIO.HIGH)
	adcout = (r[1] << 8) & 0b1100000000
	adcout = adcout | (r[2] & 0xff)		

	#adc_temp = (adcout *5.0/1023-0.5)*100
	
	return adcount

def readLumi(gpio):

	gpio.digital_write(GPIO_CS, GPIO.HIGH)
	time.sleep(0.0002)
	gpio.digital_write(GPIO_CS, GPIO.LOW)
	r = spi.xfer2([0x01, 0x80, 0x00])
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
	
	gpio.digital_write(LED, GPIO.HIGH)
	gpio.digital_write(RELE, GPIO.HIGH)

	
def desliga():


	gpio.digital_write(LED, GPIO.LOW)
	gpio.digital_write(RELE, GPIO.LOW)


def readDigital(gpio):
	digital = [0,0]
	digital[0] = gpio.digital_read(RELE)
	digital[1] = gpio.digital_read(LED)

	return digital

def writeDigital(gpio, digital):
	write = digital
	gpio.digital_write(RELE, write[0])
	gpio.digital_write(LED, write[1])

	return digital


def Aut_Liga():

	liga()
	alarme = 1
	dweet.dweet_by_name(name="bmfmata", data={"alarme":alarme, "temp":vtemp, "lumi":vlumi, "bam_nuvem":bam_nuvem, "bebe":alarme_bebe, "reset":reset_nuvem, "estado": estado_am, "liga_des":ld_nuvem,})
	print "Sistema Automatico! \n"		
	print "Ar Condicionado Ligado"		
	print ("Temperatura: %2.1f" %vtemp)
	print ("Luminosidade: %2.1f \n" %vlumi)
	

def Aut_Des():

	desliga()	
	alarme = 0
	dweet.dweet_by_name(name="bmfmata", data={"alarme":alarme, "temp":vtemp, "lumi":vlumi, "bam_nuvem":bam_nuvem, "bebe":alarme_bebe, "reset":reset_nuvem, "estado": estado_am, "liga_des":ld_nuvem,})
	print "Sistema Automatico! \n"				
	print "Ar Condicionado Desligado"		
	print ("Temperatura: %2.1f" %vtemp)
	print ("Luminosidade: %2.1f \n" %vlumi)
	

def Man_Liga():

	liga()
	alarme = 1
	dweet.dweet_by_name(name="bmfmata", data={"alarme":alarme, "temp":vtemp, "lumi":vlumi, "bam_nuvem":bam_nuvem, "bebe":alarme_bebe, "reset":reset_nuvem, "estado": estado_am, "liga_des":ld_nuvem,})
	print "Ar Condicionado Ligado"		
	print ("Temperatura: %2.1f" %vtemp)
	print ("Luminosidade: %2.1f \n" %vlumi)

def Man_Des():

	desliga()	
	alarme = 0
	dweet.dweet_by_name(name="bmfmata", data={"alarme":alarme, "temp":vtemp, "lumi":vlumi, "bam_nuvem":bam_nuvem, "bebe":alarme_bebe, "reset":reset_nuvem, "estado": estado_am, "liga_des":ld_nuvem,})
	print "Ar Condicionado Desligado"		
	print ("Temperatura: %2.1f" %vtemp)
	print ("Luminosidade: %2.1f \n" %vlumi)



with GPIO(pins) as gpio:
	while True:
		digital = [0,0]
		vlumi = readLumi(gpio)
		vtemp = readtemp(gpio)
		#vtemp = (xtemp *5.0/1023-0.5)*100
		resposta = dweet.latest_dweet(name="bmfmata")
		bam_nuvem = resposta['with'][0]['content']['bam_nuvem']
		botao_valor = gpio.digital_read(BOTAO)
		if vlumi > 100:
			digital[0]=1
			digital[1]=1
			writeDigital(gpio, digital)
			
			
		else:
			digital[0]=0
			digital[1]=0
			writeDigital(gpio, digital)
			
		dweet.dweet_by_name(name="bmfmata", data={"bam_nuvem":bam_nuvem})
		print ("Temperatura: %2.1f" %vtemp)
		print ("Luminosidade: %2.1f \n" %vlumi)	
		time.sleep(5)		
		#print "Sistema Manual \n"
		
	
		
		




        
    

