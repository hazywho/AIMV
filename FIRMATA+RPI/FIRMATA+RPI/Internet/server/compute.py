from recv import server
import cv2
from ultralytics import YOLO
import keyboard
import json

#this code is to carry out the heavy processing on rpi through laptop. this saves computing power and prevents lagging & overheating of rpi.
class cloud():
    def __init__(self,path=r"C:\Users\zanyi\Documents\GitHub\AIMV\faceDetection.pt",yPercentage=10, xPercentage=15):
        self.model = YOLO(path)
        self.model.to("cuda")
        self.s=server()
        
        #precompute some values
        self.width,self.height=640,480
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
        print("init complete.")
        
    def request(self): #request frame from serv.py
        frame = self.s.getFrame()
        return frame
        
    #algo to get the biggest bounding box
    def getBiggest(self,l):
        return abs(l[2]-l[0])+abs(l[3]-l[1])
    
    def calculate(self):
        #precompute some values
        frame=self.request()
        prediction = self.model.predict(source=frame,stream_buffer=False, classes=[0],verbose=False)
        exists=1
        if prediction[0]:
            #declare and assign variables
            totalBoxes = sorted(list(prediction[0].boxes.xyxy),key=self.getBiggest,reverse=True)
            classes = prediction[0].names[prediction[0].boxes.cls.tolist()[0]]
            confidence = sorted(prediction[0].boxes.conf.tolist(),reverse=True)[0]
            midpoint = list(map(lambda x:int(x), totalBoxes[0]))
            boxes = [int(n) for n in totalBoxes[0]]
            midpoint = (midpoint[0]+abs(round((boxes[2]-boxes[0])/2)),
                        midpoint[1]+abs(round((boxes[3]-boxes[1])/2)))
            
            #putting boxes on detrected items
            cv2.rectangle(frame, (boxes[0],boxes[1]),(boxes[2],boxes[3]),color=(255,0,0),thickness=2)

            #mark edge boxes
            cv2.rectangle(frame,(self.bottomHeight,self.topHeight),(self.topWidth,self.bottomWidth),color=(255,0,0),thickness=1) 
            
            #y top/bottom limit
            frame = cv2.line(frame, (0,self.limitTop), (round(self.width),self.limitTop), (0,255,0), 1)
            frame = cv2.line(frame, (0,self.limitBottom), (round(self.width),self.limitBottom), (0,255,0), 1)
            #x left/right limit
            frame = cv2.line(frame, (self.limitLeft,0), (self.limitLeft,round(self.height)), (0,255,0), 1)
            frame = cv2.line(frame, (self.limitRight,0), (self.limitRight,round(self.height)), (0,255,0), 1)
            #midpoiconfidence
            frame = cv2.circle(frame, (midpoint[0],midpoint[1]), radius=10, color=(0, 0, 255), thickness=-1)
            cv2.putText(frame,f"{classes}, {confidence}",(boxes[0],boxes[1]-10),cv2.FONT_HERSHEY_COMPLEX,1,color=(0,0,0),thickness=2,lineType=cv2.LINE_AA)
            
            #calculate servo angles
            self.servoXlimit=100
            self.servoYlimit=90
            exists=0
            return [[exists,exists],[self.limitBottom,self.limitTop], [self.limitLeft, self.limitRight],[midpoint[0],midpoint[1]]] 
        else:
            return [[0,0],[self.limitBottom,self.limitTop], [self.limitLeft, self.limitRight],[None,(self.limitTop-self.limitBottom)/2]]
        

#run this only when the code in the car is ran     
if __name__=="__main__":
    laptop=cloud()
    if laptop:
        while not keyboard.is_pressed("q"):
            values = laptop.calculate()
            json_data = json.dumps(values)
            bytes_data = json_data.encode('utf-8')
            laptop.s.reply(len(bytes_data),bytes_data)
    
    