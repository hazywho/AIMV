import motorSystem
from faceRecog import facialDatector
from huskylensConnection import lens
from speakerSystem import speaker
import cv2

#for reference: [self.angle[1],self.frame,[self.limitBottom,self.limitTop],[self.midpoint[0],self.midpoint[1]]] \ 
class mainCode():
    def __init__(self, com="COM8",GPU_Compute=True,printDetails=False,distThresh=20,defaultPath = r"C:\Users\zanyi\Documents\GitHub\AIMV\chaseAtlantic.wav"): #distThresh is in cm
        print("setting up cv2...")
        self.cap = cv2.VideoCapture(0)
        self.videoMachine = facialDatector(cap=self.cap)
        if GPU_Compute:
            print("connecting to GPU")
            self.videoMachine.toGPU()
            
        print("setting up motor system...")
        self.motorSys=motorSystem.board(com=com)
        self.distThresh=distThresh
        self.motorSys.servoWrite(0)
        
        print("setting up i2c connection for huskylens...",end="")
        self.hl = lens() #no need to specify port, this is done on raspberry pi.
        print("done!")
        print(self.hl) if printDetails==True else None
        
        print("initializing pyaudio...(you may hear some sounds)",end="")
        self.audioMachine=speaker()
        self.audioMachine.playAudio(path=r"C:\Users\zanyi\Documents\GitHub\AIMV\FIRMATA+RPI\pop.wav")
        print("done!")
        
        print("progressing to next phase...")
    
    def calibration(self,verificationRecurrances=10): #there is no x calibration yet.
        verificationRecurrances=verificationRecurrances
        deg=0
        calibrationFlag=False
        recurrances=0
        flag=True
        
        if flag:
            print("starting test run of hardware systems...")
            self.motorSys.testRunMotor()
            flag=False
        print("starting calibration of AI lenses! (program will detect for human)")
        value,frame=self.getAndPredict() #run AI lenses (laptop) and get back value
        
        cv2.imshow("frame",frame)
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
        elif (value[0][1]!=None and recurrances>=verificationRecurrances): #did until here: changes: instead of returning y value only returned x and y value.
            print("completed!")
            return True
        else:
            self.calibration()
                    
    def main(self,audio=r"C:\Users\zanyi\Documents\GitHub\AIMV\FIRMATA+RPI\siren.wav"):
        print("main code starting...")
        self.value,self.frame=self.getAndPredict() 
        self.movement=self.calculateServoMotorMovement(value=self.value) #adjust y value
        self.motorSys.servoWrite(self.movement) #adjjust x value
        self.motorSys.stop()
        self.repositionCarRotation()
        if self.detectForChoking():
            self.audioMachine.playAudio(path=audio) #sound alarm
            self.runStraight() #go straight until near enough
            if self.motorSys.getDistance()<self.distThresh:
                self.motorSys.stop()
                #provide aid

        print(self.movement)
        cv2.imshow("output",self.value[1])
        
        self.checkKeyPresses()
           
    def calculateServoMotorMovement(self,value,initialAngle=50,steps=10,servoMax=100):
        #update servo angle
        angle = initialAngle
        midpointY=value[3][1]
        threshYBottom=value[2][0]
        threshYTop=value[2][1]
        
        if midpointY < threshYBottom and angle>0:
            angle-=steps #i want to make it bezier
        elif midpointY > threshYTop and angle<servoMax:
            angle+=steps #i want to make it bezier
            
        return angle
    
    def repositionCarRotation(self,value,willStop=False,delay=0):
        #determine some movement variables
        midpointX=value[3][0] #x angle
        threshXLeft=value[2][0]
        threshXRight=value[2][1]
        
        if midpointX < threshXLeft:
            self.motorSys.stop()
            self.motorSys.right(willStop=willStop,delay=delay)#move right if person is left. cancel out difference.
        elif midpointX > threshXRight:
            self.motorSys.stop()
            self.motorSys.left(willStop=willStop,delay=delay)#move left if person is right. cancel out difference.
            
        return True
        
    def detectForChoking(self):
        status = self.hl.requestChokingStatus(chokingID=2)
        return status

    def runStraight(self,willStop=False,delay=0):
        self.motorSys.front(willStop=willStop,delay=delay)
            
    def checkKeyPresses(self):
        if cv2.waitKey(1) & 0xFF == ord("q"):
            self.end()
        else:
            self.main()
            
    def getAndPredict(self):
        ret,frame=self.cap.read()
        frame=cv2.flip(frame,1)
        value = self.videoMachine.getVal(frame=frame)
        return value,frame
    
    def end(self):
        print("program terminated. Stopping...")
        cv2.destroyAllWindows()
        self.cap.release()
        return False

if __name__ == "__main__":
    system = mainCode()
    system.calibration()
    system.main()
    
