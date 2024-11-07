import motorSystem
from faceRecog import facialDatector
import cv2

class mainCode():
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.videoMachine = facialDatector(cap=self.cap)

    def start(self):
        self.ret,self.frame=self.cap.read()
        self.value = self.videoMachine.getVal(frame=self.frame)
        
        self.calculate(numbers=self.value)
        cv2.imshow("output",self.value[1])
        self.checkKeyPresses()
       
    def calculate(self,numbers):
        
        
     
    def checkKeyPresses(self):
        if cv2.waitKey(1) & 0xFF == ord("q"):
            self.end()
        else:
            self.start()

    def end(self):
        cv2.destroyAllWindows()
        self.cap.release()

if __name__ == "__main__":
    system = mainCode()
    system.start()
    
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
#     subflag=0
#     height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
#     width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
#     count=0
#     movement=50  
#     steps = 10
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
#         if subflag:
#             deg-=1
#         else:
#             deg+=1
#         if deg==120:
#             subflag=1
#         if deg==0:
#             subflag=0

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
#                 movement-=steps #i want to make it bezier
#             elif angle[3][1]>angle[2][1] and movement<100:
#                 movement+=steps #i want to make it bezier
#             else:
#                 movement+=0
#             print(movement)
#             alignmentServo.write(movement)
#         if cv2.waitKey(1) & 0xFF == ord("q"):
#             break
        
#     cap.release()
#     cv2.destroyAllWindows()