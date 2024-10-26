from ultralytics import YOLO
import cv2
import time
import motorSystem
import RPi.GPIO as GPIO
from lens.predictor import protocol
import math

cap = cv2.VideoCapture(0)
model = YOLO("yolo11n.pt")
model.to("cuda")
huskee = protocol("I2C")
a=0
addedAngles=0
#algo to get the biggest bounding box
def getBiggest(l):
    return abs(l[2]-l[0])+abs(l[3]-l[1])
    
while True:
    #declare and assign variables
    ret,frame=cap.read()
    frame = cv2.flip(frame, 1) 
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    print(f"camera width/height is (please verify): {(width,height)}")
    
    #calculate edge boxes
    bottomWidth = int(width/10)
    bottomHeight = int(height/10)
    topWidth = int(width)-bottomWidth
    topHeight = int(height)-bottomHeight
    
    #mark edge boxes
    cv2.rectangle(frame, (bottomWidth,bottomHeight),(topWidth,topHeight),color=(255,0,0),thickness=1)
    
    #make it so that yolo only runs when choking is detected.
    isChoking = huskee.request()    
    if not isChoking:
        a = math.sin(math.radians(a))
        addedAngles+=a
        motorSystem.moveCamTo(a)
        if a<360:
            a+=1
        else:
            a = 0
            addedAngles=0
    else:
        #reset orientation to **about right** facing object
        angleToMovement = map(addedAngles,-114.6,114.6,0,1)
        if addedAngles>0:
            motorSystem.turnleft()
            time.sleep(angleToMovement)
        elif addedAngles<0:
            motorSystem.turnright()
            time.sleep(angleToMovement)
        motorSystem.moveCamTo(0)
        
        #declare and assign variables 2
        prediction = model.predict(source=frame,stream_buffer=False,classes=[0],verbose=False)
        try:
            totalBoxes = sorted(list(prediction[0].boxes.xyxy),key=getBiggest,reverse=True)
            classes = prediction[0].names[prediction[0].boxes.cls.tolist()[0]]
            confidence = sorted(prediction[0].boxes.conf.tolist(),reverse=True)[0]
            midpoint = list(map(lambda x:int(x), totalBoxes[0]))
            boxes = [int(n) for n in totalBoxes[0]]

            #framing, for visualization
            cv2.rectangle(frame, (boxes[0],boxes[1]),(boxes[2],boxes[3]),color=(255,0,0),thickness=2)
            cv2.putText(frame,f"{classes}, {confidence}",(boxes[0],boxes[1]-10),cv2.FONT_HERSHEY_COMPLEX,1,color=(0,0,0),thickness=2,lineType=cv2.LINE_AA)
            print(f"midpoint at {midpoint}")

            #servo rotation calculation
            servoXlimit=180
            servoYlimit=90
            angle = ((round(midpoint[0]/width*servoXlimit)),(round(midpoint[1]/height*servoYlimit)))
            print(f"angle of xy is: {angle}")
            
            #check if object is centered
            while (width/2+(width/10))/servoXlimit < angle[1] < (width/2-(width/10))/servoXlimit:
                #obj is too right
                motorSystem.stop()
                while (width/2+(width/10))/servoXlimit < angle[1]:
                    motorSystem.turnleft()
                    time.sleep(0.2)
                #obj too left
                while angle[1] < (width/2-(width/10))/servoXlimit:
                    motorSystem.turnright()
                    time.sleep(0.2)

            # #move foward
            # dist = motorSystem.getDistance()
            # while dist>10:
            #     motorSystem.gostraight()
            #     dist = motorSystem.getDistance()
            # motorSystem.stop()
            # motorSystem.openDoor()
            # time.sleep(3)
            # motorSystem.closeDoor()
            
        except IndexError:
            print("huh??? you are fucked")
            None
        
    cv2.imshow("frame",frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        cv2.imwrite(r"C:\Users\zanyi\Documents\GitHub\AIMV\outputFolder\lastImage.jpg",frame)
        break

cap.release()
cv2.destroyAllWindows()
GPIO.cleanup()