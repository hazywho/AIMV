from gpiozero.pins.pigpio import PiGPIOFactory
import time
import math
from gpiozero import Servo
import RPi.GPIO as GPIO

class car():
    def stop(self):
        GPIO.output(self.leftM1APin,0)
        GPIO.output(self.leftM2APin,0)
        GPIO.output(self.rightM1APin,0)
        GPIO.output(self.rightM2APin,0)
        
        GPIO.output(self.leftM1BPin,0)
        GPIO.output(self.leftM2BPin,0)
        GPIO.output(self.rightM1BPin,0)
        GPIO.output(self.rightM2BPin,0)

    def front(self,delay=5,willStop=True):
        GPIO.output(self.leftM1APin,1)
        GPIO.output(self.leftM2APin,1)
        GPIO.output(self.rightM1APin,1)
        GPIO.output(self.rightM2APin,1)

        time.sleep(delay)
        self.stop() if willStop else None

    def back(self,delay=5,willStop=True):
        GPIO.output(self.leftM1BPin,1)
        GPIO.output(self.leftM2BPin,1)
        GPIO.output(self.rightM1BPin,1)
        GPIO.output(self.rightM2BPin,1)

        time.sleep(delay)
        self.stop() if willStop else None

    def left(self,delay=5,willStop=True):
        GPIO.output(self.leftM1BPin,1)
        GPIO.output(self.leftM2BPin,1)
        GPIO.output(self.rightM1APin,1)
        GPIO.output(self.rightM2APin,1)

        time.sleep(delay)
        self.stop() if willStop else None

    def right(self,delay=5,willStop=True):
        GPIO.output(self.leftM1APin,1)
        GPIO.output(self.leftM2APin,1)
        GPIO.output(self.rightM1BPin,1)
        GPIO.output(self.rightM2BPin,1)

        time.sleep(delay)
        self.stop() if willStop else None

    def clockwise(self,delay=5,willStop=True):
        GPIO.output(self.leftM1APin,1)
        GPIO.output(self.leftM2BPin,1)
        GPIO.output(self.rightM1BPin,1)
        GPIO.output(self.rightM2APin,1)

        time.sleep(delay)       
        self.stop() if willStop else None

    def counter_clockwise(self,delay=5,willStop=True):
        GPIO.output(self.leftM1BPin,1)
        GPIO.output(self.leftM2APin,1)
        GPIO.output(self.rightM1APin,1)
        GPIO.output(self.rightM2BPin,1)

        time.sleep(delay)
        self.stop() if willStop else None
        
    # def getDistance(self):
    #         dist=None
    #     # while dist==None:
    #         count=0
    #         print("getting dist")
    #         GPIO.output(self.Trig, GPIO.HIGH)
    #         time.sleep(0.00001)
    #         GPIO.output(self.Trig, GPIO.LOW)
    #         pulse_start=time.time()
    #         pulse_end=time.time()
    #         ls=[]
    #         while GPIO.input(self.Echo)==0:
    #             pulse_start = time.time()
    #             count+=1
    #             ls.append(pulse_start)
    #             if count>300:
    #                 break
    #             # GPIO.output(self.Trig, GPIO.HIGH)
    #             # time.sleep(0.00001)
    #             # GPIO.output(self.Trig, GPIO.LOW)
            
    #         while GPIO.input(self.Echo)==1:
    #             pulse_end = time.time()

    #         pulseDuration = pulse_end-ls[-2]
    #         dist = pulseDuration*34300/2
    #         return dist
        
    def servoWrite(self,angle):
        angle = self.num_to_range(angle, 0,100,270,360)
        print(angle)
        self.servoCam.value = math.sin(math.radians(angle))

    def __init__(self,  servo_pin=12, leftM1APin=14, leftM1BPin=15, leftM2APin=18, leftM2BPin=5, rightM1APin=6,
                 rightM1BPin=7, rightM2APin=8, rightM2BPin=9, Trig=10, Echo=11):  
        
        print("setup rpi...")
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        print("initialized, starting setup...") #havent setup servo
        self.leftM1APin=leftM1APin
        self.leftM1BPin=leftM1BPin
        self.leftM2APin=leftM2APin
        self.leftM2BPin=leftM2BPin
        self.rightM1APin=rightM1APin
        self.rightM1BPin=rightM1BPin
        self.rightM2APin=rightM2APin
        self.rightM2BPin=rightM2BPin
        self.Trig=Trig
        self.Echo=Echo
        #the camera servo
        factory = PiGPIOFactory()
        self.servoCam = Servo(servo_pin, pin_factory=factory, min_pulse_width=(0.5/1000), max_pulse_width=(2.5/1000))
        self.servoCam.value = None

        #setup ultrasonic
        GPIO.setup(self.Trig, GPIO.OUT)
        GPIO.setup(self.Echo, GPIO.IN)

        #setup self.leftM1BPin side dc motor
        GPIO.setup(self.leftM1APin,GPIO.OUT)
        GPIO.setup(self.leftM1BPin,GPIO.OUT)
        GPIO.setup(self.leftM2APin,GPIO.OUT)
        GPIO.setup(self.leftM2BPin,GPIO.OUT)

        #setup right side dc motor
        GPIO.setup(self.rightM1APin, GPIO.OUT)
        GPIO.setup(self.rightM1BPin, GPIO.OUT)
        GPIO.setup(self.rightM2APin, GPIO.OUT)
        GPIO.setup(self.rightM2BPin, GPIO.OUT)
        
        
        time.sleep(2)
        
        print("finished setting up. moving onto next phase")

    def num_to_range(self,num, inMin, inMax, outMin, outMax):
        return int(outMin + (float(num - inMin) / float(inMax - inMin) * (outMax
                        - outMin)))

    def testRunMotor(self,tDelay=2):
        print("running tests on DC motors...")
        print("font")
        self.front(delay=tDelay)

        print("back")
        self.back(delay=tDelay)
        
        print("left")
        self.left(delay=tDelay)
        
        print("right")
        self.right(delay=tDelay)
        
        print("turning clockwise")
        self.clockwise(delay=tDelay)
        
        print("turning counter-clockwise")
        self.counter_clockwise(delay=tDelay)
        
        # print("testing ultrasonic sensor...")
        # dist = self.getDistance()
        # print(f"distance: {dist}")
        
        print("testing servo")
        self.servoWrite(1)
        time.sleep(1)
        self.servoWrite(90)
        
        print("test run complete! All hardware modules working.")

if __name__ == "__main__":
    nano = car()
    nano.stop()
    nano.testRunMotor()
