import motorSystem
from huskylensConnection import lens
from speakerSystem import speaker
import cv2
from Internet.serv import client

#for reference: [self.angle[1],self.frame,[self.limitBottom,self.limitTop],[self.midpoint[0],self.midpoint[1]]] 
class mainCode():
    def __init__(self, com="COM8",printDetails=False,distThresh=20,audioPath = r"siren.wav"): #distThresh is in cm
        print("setting up cv2...")
        self.cap = cv2.VideoCapture(0)
                    
        print("setting up client...")
        self.c = client()
        
        print("setting up motor system...")
        self.motorSys=motorSystem.board(com=com)
        self.distThresh=distThresh
        self.motorSys.servoWrite(0)
        
        print("setting up i2c connection for huskylens...",end="")
        self.hl = lens() #no need to specify port, this is done on raspberry pi.
        print("done!")
        print(self.hl) if printDetails==True else None
        self.audioPath=audioPath
        print("done!")
        
        print("progressing to next phase...")
    
    def calibration(self,verificationRecurrances=10): #there is no x calibration yet.
        verificationRecurrances=verificationRecurrances
        deg=0
        calibrationFlag=False
        recurrances=0
        flag=False #determine whether to run hardware test or not

        print("initializing pyaudio...(you may hear some sounds)",end="")
        self.audioMachine=speaker()
        self.audioMachine.playAudio(path=self.audioPath)

        while True:
            if flag:
                print("starting test run of hardware systems...")
                self.motorSys.testRunMotor()
                flag=False
            print("starting calibration of AI lenses! (program will detect for human)")
            value=self.getAndPredict() #run AI lenses (laptop) and get back value
            if value==None:
                continue #to counter internet losses
            
            # cv2.imshow("frame",frame)
            self.motorSys.servoWrite(deg)
            #adding values to servo angles based on clockwise or anti-clockwise
            if value[0]!=None:
                print(f"found!, stay still. Iterations: {verificationRecurrances-recurrances}")
                recurrances+=1
            else:
                recurrances=0
                if calibrationFlag:
                    deg-=1
                else:
                    deg+=1
                
            #turning clockwise when it reaches counter-clockwise end
            if deg==120:
                calibrationFlag=1
                
            #turning counter-clockwise when it reaches clockwise end
            if deg==0:
                calibrationFlag=0
                            
            if cv2.waitKey(1) & 0xFF==ord("q"):
                self.end()
                break
            elif (value[0]!=False and recurrances>=verificationRecurrances): #did until here: changes: instead of returning y value only returned x and y value.
                print("completed!")
                return deg

    def main(self,movement=50,show=False):
        print("main code starting...")
        self.movement=movement
        while True:
            print("detecting")
            self.value,self.frame=self.getAndPredict() 
            if self.value[0][0]==0 and self.value[0][1]==0:
                continue
            self.movement=self.calculateServoMotorMovement(value=self.value, initialAngle=self.movement) #adjust y value
            self.motorSys.servoWrite(self.movement,delay=0) #adjust x value
            self.repositionCarRotation(value=self.value)
            self.is_choking=self.detectForChoking()
            if self.is_choking:
                self.audioMachine.playAudio(path=self.audioPath) #sound alarm
                self.motorSys.front(willStop=False,delay=0) #go straight until near enough
                # if self.motorSys.getDistance()<self.distThresh:
                #     self.motorSys.stop()
                #     #provide aid

            print(self.movement)
            if show==True:
                cv2.imshow("output",self.frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    self.end()
                    break
   
#can be async        
    def calculateServoMotorMovement(self,value,initialAngle=50,steps=5,servoMax=100):
        #update servo angle
        angle = initialAngle
        midpointY=value[3][1]
        threshYBottom=value[1][0]
        threshYTop=value[1][1]
        
        if midpointY < threshYBottom and angle>0:
            angle-=steps #i want to make it bezier
        elif midpointY > threshYTop and angle<servoMax:
            angle+=steps #i want to make it bezier
            
        return angle
    
    def repositionCarRotation(self,value,willStop=True,delay=0):
        #determine some movement variables
        midpointX=value[3][0] #x angle
        threshXLeft=value[2][0]
        threshXRight=value[2][1]
        
        self.motorSys.stop()
        if midpointX < threshXLeft:
            print("going right")
            self.motorSys.clockwise(willStop=willStop,delay=delay)#move right if person is left. cancel out difference.
        elif midpointX > threshXRight:
            print("going left")
            self.motorSys.counter_clockwise(willStop=willStop,delay=delay)#move left if person is right. cancel out difference.

#can be async
    def detectForChoking(self):
        status = self.hl.requestChokingStatus(chokingID=2)
        return status
            
    def getAndPredict(self):
        ret,frame=self.cap.read()
        frame=cv2.flip(frame,1)
        value = self.c.sendAndCalculate(frame=frame)

        return value,frame
    
    def end(self):
        print("program terminated. Stopping...")
        cv2.destroyAllWindows()
        self.cap.release()
        return False

if __name__ == "__main__":
    system = mainCode(com="/dev/ttyACM0",audioPath=r"siren.wav")
    deg = system.calibration()
    system.main(movement=deg)
    
