import RPi.GPIO as GPIO
from gpiozero.pins.pigpio import PiGPIOFactory
import time
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
TRIG_PIN = 23
ECHO_PIN = 24

GPIO.setup(M1A,GPIO.OUT)
GPIO.setup(M1B,GPIO.OUT)
GPIO.setup(M2A,GPIO.OUT)
GPIO.setup(M2B,GPIO.OUT)
GPIO.setup(M3A,GPIO.OUT)
GPIO.setup(M3B,GPIO.OUT)
GPIO.setup(M4A,GPIO.OUT)
GPIO.setup(M4B,GPIO.OUT)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

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
    
def getDistance():
    GPIO.output(TRIG_PIN, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, GPIO.LOW)
    while GPIO.input(ECHO_PIN)==0:
        pulse_start = time.time()
    while GPIO.input(ECHO_PIN)==1:
        pulse_end = time.time()
        
    pulseDuration = pulse_end-pulse_start
    dist = pulseDuration*34300/2
    return dist

# sleeptime=5
# while True:
#     # servo.turn()
#     gostraight()
#     time.sleep(sleeptime)
#     stop()
#     goback()
#     time.sleep(sleeptime)
#     stop()
#     turnleft()
#     time.sleep(sleeptime)
#     stop()
#     turnright()
#     time.sleep(sleeptime)
#     stop()
#     goleft()
#     time.sleep(sleeptime)
#     stop()
#     goright()
#     time.sleep(sleeptime)

#     # servo.returnToZero()
#     stop()
#     time.sleep(sleeptime)
