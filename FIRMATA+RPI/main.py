import motorSystem
from faceRecog import facialDatector
import cv2


#for reference: [self.angle[1],self.frame,[self.limitBottom,self.limitTop],[self.midpoint[0],self.midpoint[1]]] \
    
class mainCode():
    def __init__(self, servoMotorMovementSteps=10, servoMotorMax=100,com="COM8",verificationRecurrances=10,defaultMovement=50,GPU_Compute=True):
        print("setting up cv2...")
        self.cap = cv2.VideoCapture(0)
        self.videoMachine = facialDatector(cap=self.cap)
        if GPU_Compute:
            print("connecting to GPU")
            self.videoMachine.toGPU()
        print("setting up motor system...")
        self.motorSys=motorSystem.board(com=com)
        self.motorSys.servoWrite(0)
        print("setting up auxillery variables...",end="")
        self.movement=defaultMovement
        self.steps=servoMotorMovementSteps
        self.servoMax=servoMotorMax
        self.deg=0
        self.calibrationFlag=False
        self.recurrances=0
        self.verificationRecurrances=verificationRecurrances
        self.flag=True
        print("done!")
        print("progressing to next phase...")
    
    def calibration(self):
        if self.flag:
            print("starting test run of hardware systems...")
            self.motorSys.testRunMotor()
            self.flag=False
        print("starting calibration of AI lenses! (program will detect for human)")
        self.getAndPredict() #run AI lenses (laptop) and get back value
        
        cv2.imshow("frame",self.frame)
        self.motorSys.servoWrite(self.deg)
        #adding values to servo angles based on clockwise or anti-clockwise
        if self.value[0]!=None:
            print(f"found!, stay still. Iterations: {self.verificationRecurrances-self.recurrances}")
            self.recurrances+=1
        else:
            self.recurrances=0
            if self.calibrationFlag:
                self.deg-=1
            else:
                self.deg+=1
            
        #turning clockwise when it reaches counter-clockwise end
        if self.deg==120:
            self.calibrationFlag=1
            
        #turning counter-clockwise when it reaches clockwise end
        if self.deg==0:
            self.calibrationFlag=0
                        
        if cv2.waitKey(1) & 0xFF==ord("q"):
            self.end()
        elif (self.value[0]!=None and self.recurrances>=self.verificationRecurrances):
            print("completed!")
            return True
        else:
            self.calibration()
                    
    def main(self):
        print("main code starting...")
        self.getAndPredict()
        self.calculateServoMotorMovement(value=self.value)
        self.motorSys.servoWrite(self.movement)
        
        print(self.movement)
        cv2.imshow("output",self.value[1])
        
        self.checkKeyPresses()
           
    def calculateServoMotorMovement(self,value):
        #update servo angle
        self.midpointY=value[3][1]
        self.threshYBottom=value[2][0]
        self.threshYTop=value[2][1]
        if self.midpointY < self.threshYBottom and self.movement>0:
            self.movement-=self.steps #i want to make it bezier
        elif self.midpointY > self.threshYTop and self.movement<self.servoMax:
            self.movement+=self.steps #i want to make it bezier
     
    def checkKeyPresses(self):
        if cv2.waitKey(1) & 0xFF == ord("q"):
            self.end()
        else:
            self.main()
            
    def getAndPredict(self):
        self.ret,self.frame=self.cap.read()
        self.frame=cv2.flip(self.frame,1)
        self.value = self.videoMachine.getVal(frame=self.frame)
    
    def end(self):
        print("program terminated. Stopping...")
        cv2.destroyAllWindows()
        self.cap.release()
        return False

if __name__ == "__main__":
    system = mainCode()
    system.main()
    
# # for debugging
# if __name__ == "__main__":     
#     cap = cv2.VideoCapture(0)
#     a=0
#     addedAngles=0   
#     board = pyfirmata2.ArduinoNano('/dev/ttyACM0')
#     alignmentServo = board.get_pin('d:11:s')
#     alignmentServo.write(0)
#     deg=0
#     angle=[None,None]
#     self.calibrationFlag=0
#     height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
#     width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
#     count=0
#     movement=50  
#     self.steps = 10
#     print(f"camera width/height is (please verify): {(self.width,self.height)}")
#     while angle[0]==None and count!=10:
#         ret,frame=cap.read()
#         frame = cv2.flip(frame, 1) 
#         ret,frame=cap.read()
#         frame = cv2.flip(frame, 1) 
#         print("calibrating")
#         angle = getAngleY(cap=cap,frame=frame)
#         if angle[0]!=None:
#             count+=1
#             continue
#         print(angle[0])
#         cv2.imshow("frame",angle[1])
#         alignmentServo.write(deg)
#         if self.calibrationFlag:
#             deg-=1
#         else:
#             deg+=1
#         if deg==120:
#             self.calibrationFlag=1
#         if deg==0:
#             self.calibrationFlag=0

#     while True:
#         ret,frame=cap.read()
#         frame = cv2.flip(frame, 1) 
#         #declare and assign variables
#         angle = getAngleY(cap=cap,frame=frame)
#         print(angle[0])
#         cv2.imshow("frame",angle[1])
#         if angle[0] != None:
#             angle = getAngleY(cap=cap,frame=frame,percentage=10)
#             if angle[3][1] <angle[2][0] and movement>0:
#                 print(angle[3][1])
#                 movement-=self.steps #i want to make it bezier
#             elif angle[3][1]>angle[2][1] and movement<100:
#                 movement+=self.steps #i want to make it bezier
#             else:
#                 movement+=0
#             print(movement)
#             alignmentServo.write(movement)
#         if cv2.waitKey(1) & 0xFF == ord("q"):
#             break
        
#     cap.release()
#     cv2.destroyAllWindows()