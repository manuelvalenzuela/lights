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

r = GPIO.PWM(red_pin, 1000)
g = GPIO.PWM(green_pin, 1000)
b = GPIO.PWM(blue_pin, 1000)

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

def set_color_waiting(r_color: int, g_color: int, b_color: int):
    with cv:
        cv.notify_all()
        set_bright(r, r_color)
        set_bright(g, g_color)
        set_bright(b, b_color) 
        cv.wait()
        print('set_color r:'+str(r_color)+', g:'+str(g_color)+', b:'+str(b_color)+' notified')

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

def set_color(r_color: int, g_color: int, b_color: int):
    set_bright(r, r_color)
    set_bright(g, g_color)
    set_bright(b, b_color) 
    print('set_color r:'+str(r_color)+', g:'+str(g_color)+', b:'+str(b_color)+' notified')

def switch_color_every_1_sec():
    rcolor = 100
    gcolor = 0
    bcolor = 0

    for x in range(0, 101, 25):
        gcolor = x
        set_color(rcolor,gcolor,bcolor)
        time.sleep(1)
    
    for x in range(75, -1, -25):
        rcolor = x
        set_color(rcolor,gcolor,bcolor)
        time.sleep(1)
    
    for x in range(25, 101, 25):
        bcolor = x
        set_color(rcolor,gcolor,bcolor)
        time.sleep(1)
    
    for x in range(75, -1, -25):
        gcolor = x
        set_color(rcolor,gcolor,bcolor)
        time.sleep(1)
        
    for x in range(25, 101, 25):
        rcolor = x
        set_color(rcolor,gcolor,bcolor)
        time.sleep(1)
    
    for x in range(75, -1, -25):
        bcolor = x
        set_color(rcolor,gcolor,bcolor)
        time.sleep(1)

    r.stop()
    g.stop()
    b.stop()

def start():
    orange_thread = threading.Thread(target=set_orange)
    blue_thread = threading.Thread(target=set_blue)
    off_thread = threading.Thread(target=off_lights)

    orange_thread.start()
    blue_thread.start()
    off_thread.start()