import RPi.GPIO as GPIO
import random
import time

red_pin = 23
green_pin = 24
blue_pin = 25

pins = [{'pin_num': red_pin, 'color': 'red'},
        {'pin_num': green_pin, 'color': 'green'},
        {'pin_num': blue_pin, 'color': 'blue'}]

GPIO.setmode(GPIO.BCM)  # use GPIO numbering, not generic
GPIO.setwarnings(False)

for pin in pins:
    GPIO.setup(pin['pin_num'], GPIO.OUT, initial=GPIO.LOW)

def change_bright(pin_num: int):
    p = GPIO.PWM(pin_num, 50) 
    p.start(0)
    while 1:
        for dc in range(0, 101, 5):
            p.ChangeDutyCycle(dc)
            time.sleep(0.05)
        for dc in range(100, -1, -5):
            p.ChangeDutyCycle(dc)
            time.sleep(0.05)

def set_bright(pin_num: int, dutyCycle: int):
    p = GPIO.PWM(pin_num, 50) 
    p.ChangeDutyCycle(dutyCycle)

def set_orange():
    r = GPIO.PWM(red_pin, 50) 
    r.start(0)
    g = GPIO.PWM(green_pin, 50) 
    g.start(0)
    b = GPIO.PWM(blue_pin, 50) 
    b.start(0)
    r.ChangeDutyCycle(100)
    g.ChangeDutyCycle(65)
    b.ChangeDutyCycle(0)
    while 1:
        time.sleep(0.05)

def toggle_color(color: str, state: str):
    for pin in pins:
        if pin['color'] == color:
            if state == 'on':
                GPIO.output(pin['pin_num'], GPIO.HIGH)
            elif state == 'off':
                GPIO.output(pin['pin_num'], GPIO.LOW)


def color_on(color: str):
    toggle_color(color, 'on')


def color_off(color: str):
    toggle_color(color, 'off')


def all_on():
    for pin in pins:
        GPIO.output(pin['pin_num'], GPIO.HIGH)


def all_off():
    for pin in pins:
        GPIO.output(pin['pin_num'], GPIO.LOW)


def pin_on(pin_num: int):
    GPIO.output(pin_num, GPIO.HIGH)


def pin_off(pin_num: int):
    GPIO.output(pin_num, GPIO.LOW)


def strobe_reg(period=0.5):
    while True:
        all_on()
        time.sleep(period)
        all_off()
        time.sleep(period)


def strobe_rand(min_time=0, max_time=1.2):
    while True:
        all_on()
        time.sleep(random.uniform(min_time, max_time))
        all_off()
        time.sleep(random.uniform(min_time, max_time))


def wave_reg(period=0.1):
    while True:
        for pin in pins:
            GPIO.output(pin['pin_num'], GPIO.HIGH)
            time.sleep(period)

        for pin in reversed(pins):
            GPIO.output(pin['pin_num'], GPIO.LOW)
            time.sleep(period)


def wave_rand(min_time=0, max_time=0.4):
    while True:
        period = random.uniform(min_time, max_time)
        for pin in pins:
            GPIO.output(pin['pin_num'], GPIO.HIGH)
            time.sleep(period)

        period = random.uniform(min_time, max_time)
        for pin in reversed(pins):
            GPIO.output(pin['pin_num'], GPIO.LOW)
            time.sleep(period)


def wave_rand_ex(min_time=0, max_time=0.4):
    while True:
        for pin in pins:
            GPIO.output(pin['pin_num'], GPIO.HIGH)
            time.sleep(random.uniform(min_time, max_time))

        for pin in reversed(pins):
            GPIO.output(pin['pin_num'], GPIO.LOW)
            time.sleep(random.uniform(min_time, max_time))
