#!/usr/bin/env python


from dweet import Dweet
import spidev
import time
from libsoc import gpio
from gpio_96boards import GPIO


GPIO_CS = GPIO.gpio_id('GPIO_CS')
RELE = GPIO.gpio_id('GPIO_A')
BOTAO = GPIO.gpio_id('GPIO_C')

pins = ((GPIO_CS, 'out'), (RELE, 'out'),  (BOTAO, 'in'))





spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 10000
spi.mode = 0b00
spi.bits_per_word = 8



dweet = Dweet()






alarme_bebe = 0
reset_nuvem = 0
bam_nuvem = 0
ld_nuvem = 0
estado_am = 0







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







def Leitura_nuvem():
	global bam_nuvem, ld_nuvem, reset_nuvem
	resposta = dweet.latest_dweet(name="bmfmata")
	bam_nuvem = resposta['with'][0]['content']['bam_nuvem']
	ld_nuvem = resposta['with'][0]['content']['liga_des']
	reset_nuvem = resposta['with'][0]['content']['reset']








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










def Aut_Liga():

	#gpio.digital_write(LED, GPIO.HIGH)
	gpio.digital_write(RELE, GPIO.HIGH)
	alarme = 1
	dweet.dweet_by_name(name="bmfmata", data={"alarme":alarme, "temp":vtemp, "lumi":vlumi, 
	"bam_nuvem":bam_nuvem, "bebe":alarme_bebe, "reset":reset_nuvem, "estado": estado_am, 
	"liga_des":ld_nuvem,})
	print "Sistema Automatico! \n"		
	print "Ar Condicionado Ligado"		
	print ("Temperatura: %2.1f" %vtemp)
	print ("Luminosidade: %2.1f \n" %vlumi)






def Aut_Des():

	#gpio.digital_write(LED, GPIO.LOW)
	gpio.digital_write(RELE, GPIO.LOW)	
	alarme = 0
	dweet.dweet_by_name(name="bmfmata", data={"alarme":alarme, 
	"temp":vtemp, "lumi":vlumi, "bam_nuvem":bam_nuvem, 
	"bebe":alarme_bebe, "reset":reset_nuvem, 
	"estado": estado_am, "liga_des":ld_nuvem,})
	print "Sistema Automatico! \n"				
	print "Ar Condicionado Desligado"		
	print ("Temperatura: %2.1f" %vtemp)
	print ("Luminosidade: %2.1f \n" %vlumi)








def Man_Liga():

	#gpio.digital_write(LED, GPIO.HIGH)
	gpio.digital_write(RELE, GPIO.HIGH)
	alarme = 1
	dweet.dweet_by_name(name="bmfmata", data={"alarme":alarme, 
	"temp":vtemp, "lumi":vlumi, "bam_nuvem":bam_nuvem, 
	"bebe":alarme_bebe, "reset":reset_nuvem, 
	"estado": estado_am, "liga_des":ld_nuvem,})
	print "Ar Condicionado Ligado"		
	print ("Temperatura: %2.1f" %vtemp)
	print ("Luminosidade: %2.1f \n" %vlumi)







def Man_Des():

	#gpio.digital_write(LED, GPIO.LOW)
	gpio.digital_write(RELE, GPIO.LOW)	
	alarme = 0
	dweet.dweet_by_name(name="bmfmata", data={"alarme":alarme, 
	"temp":vtemp, "lumi":vlumi, "bam_nuvem":bam_nuvem, 
	"bebe":alarme_bebe, "reset":reset_nuvem, 
	"estado": estado_am, "liga_des":ld_nuvem,})
	print "Ar Condicionado Desligado"		
	print ("Temperatura: %2.1f" %vtemp)
	print ("Luminosidade: %2.1f \n" %vlumi)






with GPIO(pins) as gpio:
	while True:		
		
		Leitura_nuvem()
		botao_valor = gpio.digital_read(BOTAO)
		vtemp = readtemp(gpio)
		vlumi = readLumi(gpio)		
		
		if botao_valor == 0 and bam_nuvem == 0:			
			
			estado_am = 1
			if vtemp > 23:
				Aut_Liga()			
			
			else:
				Aut_Des()		
			
		else:
	 		estado_am = 0
			print "Sistema Manual \n"			
			
			if ld_nuvem == 1:
				Man_Liga()
			else:
				Man_Des()
			
		time.sleep(10)
		
		
		#if reset_nuvem == 1:	
		#	alarme_bebe = 0



















		
		
        
    

