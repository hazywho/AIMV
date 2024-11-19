from ultralytics import YOLO
import cv2

class facialDatector():
    #algo to get the biggest bounding box
    def getBiggest(self,l):
        return abs(l[2]-l[0])+abs(l[3]-l[1])
    
    def __init__(self,model_path=r"C:\Users\zanyi\Documents\GitHub\AIMV\faceDetection.pt", cap=cv2.VideoCapture(0), yPercentage=10, xPercentage=15):
        print("initialising...",end="")
        self.model = YOLO(model_path)
        self.height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        
        #calculate edge boxes
        self.bottomWidth = int(self.width/10)
        self.bottomHeight = int(self.height/10)
        self.topWidth = int(self.width)-self.bottomWidth
        self.topHeight = int(self.height)-self.bottomHeight
        #y thresholds
        self.limitTop=round(self.height/2+self.height*yPercentage/100)
        self.limitBottom=round(self.height/2-self.height*yPercentage/100)
        #x thresholds
        self.limitLeft=round(self.width/2+self.width*xPercentage/100)
        self.limitRight=round(self.width/2-self.width*xPercentage/100)
        
        self.camera=cap
        print("done!")
        print("Going to next phase...")
        
    def toGPU(self):
        self.model.to("cuda")
        
    def getVal(self,frame):
        self.frame=frame
        cv2.rectangle(self.frame,(self.bottomHeight,self.topHeight),(self.topWidth,self.bottomWidth),color=(255,0,0),thickness=1) #mark edge boxes
        self.prediction = self.model.predict(source=self.frame,stream_buffer=False,classes=[0],verbose=False)
        if self.prediction[0]:
            #declare and assign variables
            self.totalBoxes = sorted(list(self.prediction[0].boxes.xyxy),key=self.getBiggest,reverse=True)
            self.classes = self.prediction[0].names[self.prediction[0].boxes.cls.tolist()[0]]
            self.confidence = sorted(self.prediction[0].boxes.conf.tolist(),reverse=True)[0]
            self.midpoint = list(map(lambda x:int(x), self.totalBoxes[0]))
            self.boxes = [int(n) for n in self.totalBoxes[0]]
            self.midpoint = (self.midpoint[0]+abs(round((self.boxes[2]-self.boxes[0])/2)),
                        self.midpoint[1]+abs(round((self.boxes[3]-self.boxes[1])/2)))
            
            #putting boxes on detrected items
            cv2.rectangle(self.frame, (self.boxes[0],self.boxes[1]),(self.boxes[2],self.boxes[3]),color=(255,0,0),thickness=2)
            
            #y top/bottom limit
            self.frame = cv2.line(self.frame, (0,self.limitTop), (round(self.width),self.limitTop), (0,255,0), 1)
            self.frame = cv2.line(self.frame, (0,self.limitBottom), (round(self.width),self.limitBottom), (0,255,0), 1)
            #x left/right limit
            self.frame = cv2.line(self.frame, (0,self.limitLeft), (round(self.width),self.limitLeft), (0,255,0), 1)
            self.frame = cv2.line(self.frame, (0,self.limitRight), (round(self.width),self.limitRight), (0,255,0), 1)
            #midpoint & confidence
            self.frame = cv2.circle(self.frame, (self.midpoint[0],self.midpoint[1]), radius=10, color=(0, 0, 255), thickness=-1)
            cv2.putText(self.frame,f"{self.classes}, {self.confidence}",(self.boxes[0],self.boxes[1]-10),cv2.FONT_HERSHEY_COMPLEX,1,color=(0,0,0),thickness=2,lineType=cv2.LINE_AA)
            
            #calculate servo angles
            self.servoXlimit=100
            self.servoYlimit=90
            self.angle = ((round(self.midpoint[0]/(self.topWidth-self.bottomWidth)*self.servoXlimit)),(round(self.midpoint[1]/(self.topHeight-self.bottomHeight)*self.servoYlimit)))
            return [self.angle,self.frame,[self.limitBottom,self.limitTop],[self.midpoint[0],self.midpoint[1]]] 
        else:
            return [None,self.frame,[self.limitBottom,self.limitTop],[None,(self.limitTop-self.limitBottom)/2]]
            
if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    machine = facialDatector(cap=cap)
    while True:
        ret,frame=cap.read()
        value = machine.getVal(frame=frame)
        cv2.imshow("frame",value[1])
        if cv2.waitKey(1) & 0xFF==ord('q'):
            break
    
    
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
#             angle = getAngleY(cap=cap,frame=frame,yPercentage=10)
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