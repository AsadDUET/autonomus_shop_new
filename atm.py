
from time import sleep
import random
import RPi.GPIO as GPIO
from gpiozero import LED, Button
import easydriver as ed
#~ import label_image

servo=LED(17)
top_light=LED(3)
bottom_light=LED(2)
ir=Button(10)
pir=Button(9)   


servo.off()
top_light.off()
bottom_light.off()

taka = ed.easydriver(27, 0.0004, 22)
chips_motor=ed.easydriver(19, 0.004)
drawer=ed.easydriver(21, 0.0004,20)
def supply():
	drawer.set_direction(True) # True = close
	for i in range(4300):
		drawer.step()
	sleep(10)
	drawer.set_direction(False) # True = close
	for i in range(4300):
		drawer.step()
def give_chips(num):
	for i in range(num*1600):
		chips_motor.step()
def take_taka():
	taka.set_direction(True)
	servo.on()
	for i in range(0,5000):
		taka.step()
	servo.off()
def back_taka():
	taka.set_direction(False)
	for i in range(0,5000):
		taka.step()
def start_atm():
	ir.wait_for_press()
	sleep(1)
	take_taka()
	back_taka()
if __name__=="__main__":
	supply()
	
