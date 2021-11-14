import RPi.GPIO as GPIO
import threading
import time

red_pin = 23
green_pin = 24
blue_pin = 25

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(red_pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(green_pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(blue_pin, GPIO.OUT, initial=GPIO.LOW)

r = GPIO.PWM(red_pin, 50)
g = GPIO.PWM(green_pin, 50)
b = GPIO.PWM(blue_pin, 50)

cv = threading.Condition()

def set_bright(pin, dutyCycle):
    pin.start(0)
    pin.ChangeDutyCycle(dutyCycle)

def set_orange():
    with cv:
        cv.notify_all()
        set_bright(r,100)
        set_bright(g,65)
        set_bright(b,0) 
        cv.wait()
        print('set_orange notified')

def set_blue():
    time.sleep(5)
    with cv:
        cv.notify_all()
        set_bright(r,0)
        set_bright(g,0)
        set_bright(b,100)
        cv.wait()
        print('set_blue notified')

def off_lights():
    time.sleep(10)
    print('attempting to off the lights')
    with cv:
        cv.notify_all()
        r.stop()
        g.stop()
        b.stop()

def pin_on(pin_num: int):
    GPIO.output(pin_num, GPIO.HIGH)

def pin_off(pin_num: int):
    GPIO.output(pin_num, GPIO.LOW)

#def start():
orange_thread = threading.Thread(target=set_orange)
blue_thread = threading.Thread(target=set_blue)
off_thread = threading.Thread(target=off_lights)

orange_thread.start()
blue_thread.start()
off_thread.start()