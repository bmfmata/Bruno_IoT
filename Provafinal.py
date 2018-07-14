#!/usr/bin/env python

#Declaração e importação das Bibliotecas
from dweet import Dweet
import spidev
import time
from libsoc import gpio
from gpio_96boards import GPIO


#Declaração e definição das Entradas e Saídas
GPIO_CS = GPIO.gpio_id('GPIO_CS')
RELE = GPIO.gpio_id('GPIO_A')
BOTAO = GPIO.gpio_id('GPIO_C')

pins = ((GPIO_CS, 'out'), (RELE, 'out'),  (BOTAO, 'in'))





#Definição de parâmetros para portas analógicas
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 10000
spi.mode = 0b00
spi.bits_per_word = 8



#Declaração de uma variável Dweet para interface com sistema 
# de nuvem
dweet = Dweet()






#Declaração de variáveis
alarme_bebe = 0
reset_nuvem = 0
bam_nuvem = 0
ld_nuvem = 0
estado_am = 0







#Leitura e conversão da leitura do sensor para °C
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






#Leitura do sensor de Luminosidade
def readLumi(gpio):

	gpio.digital_write(GPIO_CS, GPIO.HIGH)
	time.sleep(0.0002)
	gpio.digital_write(GPIO_CS, GPIO.LOW)
	r = spi.xfer2([0x01, 0xA0, 0x00])
	gpio.digital_write(GPIO_CS, GPIO.HIGH)

	adcout = (r[1] << 8) & 0b1100000000
	adcout = adcout | (r[2] & 0xff)

	return  adcout






#Leitura dos valores de variáveis na nuvem e seus resultados
#armazenados em variáveis locais para ser utilizada no programa
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









#No automático, liga o relé(ar condicionado), tranforma variável alarme (que informa a nuvem se o
# sistema está ligado ou não) em 1, atualiza o valor de todas as variáveis na nuvem de acordo com essa
#condição e print na tela do terminal informações sobre essa condição.
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





#No automático, desliga o relé(ar condicionado), tranforma variável alarme (que informa a nuvem se o
# sistema está ligado ou não) em 0, atualiza o valor de todas as variáveis na nuvem de acordo com essa
#condição e print na tela do terminal informações sobre essa condição.
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







#No estado manual, liga o relé(ar condicionado), tranforma variável alarme (que informa a nuvem se o
# sistema está ligado ou não) em 1, atualiza o valor de todas as variáveis na nuvem de acordo com essa
#condição e print na tela do terminal informações sobre essa condição.
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






#No estado manual, desliga o relé(ar condicionado), tranforma variável alarme (que informa a nuvem se o
# sistema está ligado ou não) em 0, atualiza o valor de todas as variáveis na nuvem de acordo com essa
#condição e print na tela do terminal informações sobre essa condição.
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





#Aqui é executado o programa principal até que seja interrompido
with GPIO(pins) as gpio:
	while True:
		
		#Faz a leitura e atualização das variáveis
		Leitura_nuvem()
		botao_valor = gpio.digital_read(BOTAO)
		vtemp = readtemp(gpio)
		vlumi = readLumi(gpio)
		
		#Verifica se o botão local ou botão na nuvem(aplicativo) foi acionado
		if botao_valor == 0 or bam_nuvem == 0:
			
			#Se nenhum acionado o sistema está em automático e caso temperatura maior que 24, liga
			#o ar condicionadi e uma variável na nuvem estado_am receberá 1, informado ao app que
			#está em automático
			estado_am = 1
			if vtemp > 24:
				Aut_Liga()
			
			#caso temperatura medida for menor que 24, desliga ar condicionado		
			else:
				Aut_Des()
		
		#Caso um dos botões seja acionado, o sistema vai para manual e a variável estado_am recebe 0
		# E informa estar em manual para nuvem (app)		
		else:
	 		estado_am = 0
			print "Sistema Manual \n"
			
			#Verifica se o botão de ligar da nuvem(App) está na condição de liga ou desliga
			if ld_nuvem == 1:
				Man_Liga()
			else:
				Man_Des()
		
		#Atualiza o sistema de 10 em 10 segundos		
		time.sleep(10)
		
		
		#if reset_nuvem == 1:	
		#	alarme_bebe = 0



















		
		
        
    

