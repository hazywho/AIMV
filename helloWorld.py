import RPi.GPIO as GPIO
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
from gpiozero import Servo

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

myCorrection=0.45
maxPW=(2.0+myCorrection)/1000
minPW=(1.0-myCorrection)/1000
M2A = 13
M2B = 6
M1A = 12
M1B = 5
M3A = 20
M4A = 16
M3B = 21
M4B = 1
GPIO.setup(M1A,GPIO.OUT)
GPIO.setup(M1B,GPIO.OUT)
GPIO.setup(M2A,GPIO.OUT)
GPIO.setup(M2B,GPIO.OUT)
GPIO.setup(M3A,GPIO.OUT)
GPIO.setup(M3B,GPIO.OUT)
GPIO.setup(M4A,GPIO.OUT)
GPIO.setup(M4B,GPIO.OUT)

#-----------------------servo rotation------------------------------#

factory = PiGPIOFactory()
servo1  = Servo(1, pin_factory=factory,
                           min_pulse_width=(0.5/1000), max_pulse_width=(2.5/1000))
servo1.value = 0


def turn(self, degree):
        self.degree = degree
        self.servo.value = degree

def stop():
    GPIO.output(M1A,0)
    GPIO.output(M2A,0)
    GPIO.output(M3A,0)
    GPIO.output(M4A,0)
    GPIO.output(M1B,0)
    GPIO.output(M2B,0)
    GPIO.output(M3B,0)
    GPIO.output(M4B,0)

def gostraight():
    GPIO.output(M1A,1)
    GPIO.output(M2A,1)
    GPIO.output(M3A,1)
    GPIO.output(M4A,1)

def goback():
    GPIO.output(M1B,1)
    GPIO.output(M2B,1)
    GPIO.output(M3B,1)
    GPIO.output(M4B,1)

def turnleft():
    GPIO.output(M1B,1)
    GPIO.output(M2B,1)
    GPIO.output(M3A,1)
    GPIO.output(M4A,1)

def turnright():
    GPIO.output(M1A,1)
    GPIO.output(M2A,1)
    GPIO.output(M3B,1)
    GPIO.output(M4B,1)

def goleft():
    GPIO.output(M1A,1)
    GPIO.output(M2B,1)
    GPIO.output(M3B,1)
    GPIO.output(M4A,1)

def goright():
    GPIO.output(M1B,1)
    GPIO.output(M2A,1)
    GPIO.output(M3A,1)
    GPIO.output(M4B,1)

sleeptime=5
while True:
    # servo.turn()
    gostraight()
    sleep(sleeptime)
    stop()
    goback()
    sleep(sleeptime)
    stop()
    turnleft()
    sleep(sleeptime)
    stop()
    turnright()
    sleep(sleeptime)
    stop()
    goleft()
    sleep(sleeptime)
    stop()
    goright()
    sleep(sleeptime)

    # servo.returnToZero()
    stop()
    sleep(sleeptime)
