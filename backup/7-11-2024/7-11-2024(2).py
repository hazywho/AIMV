import pyfirmata2
import time

class board():
    
    def stop(self):
        self.leftM1B.write(0)
        self.leftM2B.write(0)
        self.rightM1B.write(0)
        self.rightM2B.write(0)
        
        self.leftM1A.write(0)
        self.leftM2A.write(0)
        self.rightM1A.write(0)
        self.rightM2A.write(0)
    
    def front(self,delay=5,willStop=True):
        self.leftM1A.write(1)
        self.leftM2A.write(1)
        self.rightM1A.write(1)
        self.rightM2A.write(1)
        time.sleep(delay)
        self.stop() if willStop else None
    
    def back(self,delay=5,willStop=True):
        self.leftM1B.write(1)
        self.leftM2B.write(1)
        self.rightM1B.write(1)
        self.rightM2B.write(1)
        time.sleep(delay)
        self.stop() if willStop else None
        
    def left(self,delay=5,willStop=True):
        self.leftM1B.write(1)
        self.leftM2A.write(1)
        self.rightM1B.write(1)
        self.rightM2A.write(1)
        time.sleep(delay)
        self.stop() if willStop else None

    def right(self,delay=5,willStop=True):
        self.leftM1A.write(1)
        self.leftM2B.write(1)
        self.rightM1A.write(1)
        self.rightM2B.write(1)
        time.sleep(delay)
        self.stop() if willStop else None

    def clockwise(self,delay=5,willStop=True):
        self.leftM1A.write(1)
        self.leftM2A.write(1)
        self.rightM1B.write(1)
        self.rightM2B.write(1)
        time.sleep(delay)
        self.stop() if willStop else None

    def counter_clockwise(self,delay=5,willStop=True):
        self.leftM1B.write(1)
        self.leftM2B.write(1)
        self.rightM1A.write(1)
        self.rightM2A.write(1)
        time.sleep(delay)
        self.stop() if willStop else None
    
    def readPin(self,data):
        self.pin11Data=data
    
    def getDistance(self):
        self.ultrasonicTrigg.write(1)
        time.sleep(0.00001)
        self.ultrasonicTrigg.write(0)
        
        while self.pin11Data==0:
            self.pulse_start=time.time()
        while self.pin11Data==1:
            self.pulse_end=time.time()
        self.pulseDuration = self.pulse_end-self.pulse_start
        self.dist = self.pulseDuration*34300/2
        return self.dist
        
    def __init__(self, com='/dev/ttyACM0', servo_pin=12, leftM1APin=2, leftM1BPin=3, leftM2APin=4, leftM2BPin=5, rightM1APin=6,
                 rightM1BPin=7, rightM2APin=8, rightM2BPin=9, Trig=10, Echo=11, interval=19, printLog=True):  
        
        print("initializing arduino...")
        self.arduino = pyfirmata2.ArduinoNano(com)
        self.arduino.samplingOn(interval)
        
        print("arduino initialized, starting setup...")
        self.alignmentServo = self.arduino.get_pin(f"d:{servo_pin}:s")
        
        #setup left side dc motor
        self.leftM1A=self.arduino.get_pin(f"d:{leftM1APin}:o")
        self.leftM1B=self.arduino.get_pin(f"d:{leftM1BPin}:o")
        self.leftM2A=self.arduino.get_pin(f"d:{leftM2APin}:o")
        self.leftM2B=self.arduino.get_pin(f"d:{leftM2BPin}:o")
        self.leftM1A.register_callback(lambda value:print("Button released") if value and printLog else print("Button pressed"))
        self.leftM1B.register_callback(lambda value:print("Button released") if value and printLog else print("Button pressed"))
        self.leftM2A.register_callback(lambda value:print("Button released") if value and printLog else print("Button pressed"))
        self.leftM2B.register_callback(lambda value:print("Button released") if value and printLog else print("Button pressed"))

        #setup right side dc motor
        self.rightM1A=self.arduino.get_pin(f"d:{rightM1APin}:o")
        self.rightM1B=self.arduino.get_pin(f"d:{rightM1BPin}:o")
        self.rightM2A=self.arduino.get_pin(f"d:{rightM2APin}:o")
        self.rightM2B=self.arduino.get_pin(f"d:{rightM2BPin}:o")
        self.rightM1A.register_callback(lambda value:print("Button released") if value and printLog else print("Button pressed"))
        self.rightM1B.register_callback(lambda value:print("Button released") if value and printLog else print("Button pressed"))
        self.rightM2A.register_callback(lambda value:print("Button released") if value and printLog else print("Button pressed"))
        self.rightM2B.register_callback(lambda value:print("Button released") if value and printLog else print("Button pressed"))
        
        #setup ultrasonic
        self.ultrasonicTrigg=self.arduino.get_pin(f"d:{Trig}:o")
        self.ultrasonicEcho=self.arduino.get_pin(f"d:{Echo}:i")
        self.ultrasonicTrigg.register_callback(lambda value:print("ultrasound sent") if value and printLog else None)
        self.ultrasonicEcho.register_callback(self.readPin)
        self.ultrasonicEcho.enable_reporting()
        self.pin11Data=0
        
        print("finished setting up. moving onto next phase")

    def testRunDCMotor(self):
        print("running tests on DC motors...")
        print("font")
        self.front()

        print("back")
        self.back()
        
        print("left")
        self.left()
        
        print("right")
        self.right()
        
        print("turning clockwise")
        self.clockwise()
        
        print("turning counter-clockwise")
        self.counter_clockwise()
        
        print("testing ultrasonic sensor...")
        dist = self.getDistance()
        print(f"distance: {dist}")
        
        print("testing servo")
        self.alignmentServo.write(0)
        time.sleep(2)
        self.alignmentServo.write(180)
        time.sleep(3)
        
        print("test run complete! All modules working.")

if __name__ == "__main__":
    nano = board(com="COM8")
    nano.testRunDCMotor()
