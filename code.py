import RPi.GPIO as GPIO
import time
import hcsr04sensor
 
# Define GPIO to LCD mapping
LCD_RS = 12
LCD_E  = 13
LCD_D4 = 19
LCD_D5 = 20
LCD_D6 = 26
LCD_D7 = 21
LED_ON = 16

SolMotorI = 2
SolMotorG = 3
SagMotorI =5
SagMotorG = 4

DokunSensor = 6

TRIG = 7
ECHO = 8


# Define some device constants
LCD_WIDTH = 20    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False
 
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line
 
# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005
global second, minute, hour, day, month, year
def main():
	# Main program block
 
	GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
	GPIO.setup(LCD_E, GPIO.OUT)  # E
	GPIO.setup(LCD_RS, GPIO.OUT) # RS
	GPIO.setup(LCD_D4, GPIO.OUT) # DB4
	GPIO.setup(LCD_D5, GPIO.OUT) # DB5
	GPIO.setup(LCD_D6, GPIO.OUT) # DB6
	GPIO.setup(LCD_D7, GPIO.OUT) # DB7
	GPIO.setup(LED_ON, GPIO.OUT) # Backlight enable

	GPIO.setup(SolMotorI, GPIO.OUT)
	GPIO.setup(SolMotorG, GPIO.OUT)
	GPIO.setup(SagMotorI, GPIO.OUT)
	GPIO.setup(SagMotorG, GPIO.OUT)

	GPIO.setup(DokunSensor, GPIO.IN)

	GPIO.setwarnings(False)

	GPIO.setup(TRIG,GPIO.OUT)
	GPIO.setup(ECHO,GPIO.IN)


	# Initialise display
	lcd_init()
	# Toggle backlight on-off-on

	
	# Send some centred test
	lcd_string("GOMULU SISTEMLER",LCD_LINE_1,2)
	lcd_string("ROBOT SUPURGE",LCD_LINE_2,2)
	lcd_string("16008119059",LCD_LINE_3,2)
	lcd_string("AYSEGUL SAYGI",LCD_LINE_4,2)
	time.sleep(3) # 3 second delay
	lcd_byte(0x01,LCD_CMD) # 000001 Clear display

	while True:
		GPIO.output(TRIG, False)
		time.sleep(1)

		GPIO.output(TRIG, True)
		time.sleep(0.00001)
		GPIO.output(TRIG, False)

		while GPIO.input(ECHO)==0:
			pulse_start = time.time()

		while GPIO.input(ECHO)==1:
			pulse_end = time.time()

		pulse_duration = pulse_end - pulse_start

		distance = pulse_duration * 17150
		distance = round(distance/100, 2)
		
				
		DokunSensorDurum = GPIO.input(DokunSensor)
		if DokunSensorDurum == 1:
			lcd_string("CALISMA BASLADI",LCD_LINE_4,2)
			time.sleep(1)
			lcd_byte(0x01,LCD_CMD) # 000001 Clear display
			lcd_string("ORTAM TARANIYOR",LCD_LINE_1,2)
			lcd_string("ROBOT SUPURGE",LCD_LINE_2,2)
			lcd_string("KONUMLANDIRMA",LCD_LINE_3,2)
			lcd_string("YAPIYOR",LCD_LINE_4,2)
			time.sleep(2)
			lcd_byte(0x01,LCD_CMD) # 000001 Clear display
			lcd_string("ROBOT AKTIF EDILDI",LCD_LINE_1,2)
			GPIO.output(SolMotorI,GPIO.HIGH)
			GPIO.output(SagMotorI,GPIO.HIGH)
			lcd_string("ROBOT SUPURGE",LCD_LINE_2,2)
			
			if distance < 1:
				lcd_string("DUVARA CARPMAK UZERE",LCD_LINE_3,2)
				lcd_string("GERI GONULUYOR",LCD_LINE_4,2)
				GeriGidis(2)
				SagaDonus(2)
				IleriGidis(2)
				SagaDonus(2)
			else:
				lcd_byte(0x01,LCD_CMD) # 000001 Clear display
				for sayac in range(3):
					IleriGidis(10)
					SagaDonus(2)
					IleriGidis(2)
					SagaDonus(2)
					IleriGidis(10)
					SolaDonus(2)
					IleriGidis(2)
					SolaDonus(2)
					IleriGidis(10)
		else:
			lcd_string("SUPURGE KAPALI",LCD_LINE_4,2)
		second, minute, hour, day, month, year = date()
		date_info = "{}/{}/{}-{}:{}:{}".format(day,month,year,hour,minute,second)
		lcd_string(date_info,LCD_LINE_1,2)

def SolaDonus(i):
	GPIO.output(SagMotorI,GPIO.HIGH)
	GPIO.output(SolMotorI,GPIO.LOW)
	for sayac in range(i+1):
		lcd_string("ROBOT SUPURGE",LCD_LINE_1,2)
		lcd_string("SOLA DONUYOR: {}".format(sayac),LCD_LINE_2,2)
		time.sleep(0.5)

def SagaDonus(i):
	GPIO.output(SagMotorI,GPIO.LOW)
	GPIO.output(SolMotorI,GPIO.HIGH)
	for sayac in range(i+1):
		lcd_string("ROBOT SUPURGE",LCD_LINE_1,2)
		lcd_string("SAGA DONUYOR: {}".format(sayac),LCD_LINE_2,2)
		time.sleep(0.5)

def IleriGidis(i):
	GPIO.output(SagMotorI,GPIO.HIGH)
	GPIO.output(SolMotorI,GPIO.HIGH)
	GPIO.output(SagMotorG,GPIO.LOW)
	GPIO.output(SolMotorG,GPIO.LOW)
	for sayac in range(i+1):
		lcd_string("ROBOT SUPURGE",LCD_LINE_1,2)
		lcd_string("DUZ GIDIYOR: {}".format(sayac),LCD_LINE_2,2)
		time.sleep(0.5)

def GeriGidis(i):
	GPIO.output(SagMotorG,GPIO.HIGH)
	GPIO.output(SolMotorG,GPIO.HIGH)
	GPIO.output(SagMotorI,GPIO.LOW)
	GPIO.output(SolMotorI,GPIO.LOW)
	for sayac in range(i+1):
		lcd_string("ROBOT SUPURGE",LCD_LINE_1,2)
		lcd_string("GERI GIDIYOR: {}".format(sayac),LCD_LINE_2,2)
		time.sleep(0.5)

def date():
	zaman = time.localtime()
	second = zaman.tm_sec
	minute = zaman.tm_min
	hour = zaman.tm_hour
	day = zaman.tm_mday
	month = zaman.tm_mon
	year = zaman.tm_year
	date = "{}/{}/{}-{}:{}:{}".format(day,month,year,hour,minute,second)
	lcd_string(date,LCD_LINE_1,2)
	return second, minute, hour, day, month, year

def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)
 
def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command
 
  GPIO.output(LCD_RS, mode) # RS
 
  # High bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)
 
  # Toggle 'Enable' pin
  lcd_toggle_enable()
 
  # Low bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)
 
  # Toggle 'Enable' pin
  lcd_toggle_enable()
 
def lcd_toggle_enable():
  # Toggle enable
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)
 
def lcd_string(message,line,style):
  # Send string to display
  # style=1 Left justified
  # style=2 Centred
  # style=3 Right justified
 
  if style==1:
    message = message.ljust(LCD_WIDTH," ")
  elif style==2:
    message = message.center(LCD_WIDTH," ")
  elif style==3:
    message = message.rjust(LCD_WIDTH," ")
 
  lcd_byte(line, LCD_CMD)
 
  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)
 
def lcd_backlight(flag):
  # Toggle backlight on-off-on
  GPIO.output(LED_ON, flag)
 
if __name__ == '__main__':
 
  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(0x01, LCD_CMD)
    lcd_string("Goodbye!",LCD_LINE_1,2)
    GPIO.cleanup()




