from ultralytics import YOLO
import cv2
import pyfirmata2

#algo to get the biggest bounding box
def getBiggest(l):
    return abs(l[2]-l[0])+abs(l[3]-l[1])

def getAngleY(cap, frame, percentage=10):
    model = YOLO(r"/home/hezy/Downloads/ClonedAIMV2/AIMV/faceDetection.pt")
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    #calculate edge boxes
    bottomWidth = int(width/10)
    bottomHeight = int(height/10)
    topWidth = int(width)-bottomWidth
    topHeight = int(height)-bottomHeight
    limitTop=round(height/2+height*percentage/100)
    limitBottom=round(height/2-height*percentage/100)

    # mark edge boxes
    cv2.rectangle(frame, (bottomWidth,bottomHeight),(topWidth,topHeight),color=(255,0,0),thickness=1)
    
    #declare and assign variables 2
    try:
        prediction = model.predict(source=frame,stream_buffer=False,classes=[0],verbose=False)
        totalBoxes = sorted(list(prediction[0].boxes.xyxy),key=getBiggest,reverse=True)
        classes = prediction[0].names[prediction[0].boxes.cls.tolist()[0]]
        confidence = sorted(prediction[0].boxes.conf.tolist(),reverse=True)[0]
        midpoint = list(map(lambda x:int(x), totalBoxes[0]))
        boxes = [int(n) for n in totalBoxes[0]]
        midpoint = (midpoint[0]+abs(round((boxes[2]-boxes[0])/2)),
                    midpoint[1]+abs(round((boxes[3]-boxes[1])/2)))

        #framing, for visualization
        cv2.rectangle(frame, (boxes[0],boxes[1]),(boxes[2],boxes[3]),color=(255,0,0),thickness=2)
        frame = cv2.line(frame, (0,limitTop), (round(width),limitTop), (0,255,0), 1)
        frame = cv2.line(frame, (0,limitBottom), (round(width),limitBottom), (0,255,0), 1)
        frame = cv2.circle(frame, (midpoint[0],midpoint[1]), radius=10, color=(0, 0, 255), thickness=-1)
        cv2.putText(frame,f"{classes}, {confidence}",(boxes[0],boxes[1]-10),cv2.FONT_HERSHEY_COMPLEX,1,color=(0,0,0),thickness=2,lineType=cv2.LINE_AA)

        #servo rotation calculation
        servoXlimit=100
        servoYlimit=90
        angle = ((round(midpoint[0]/(topWidth-bottomWidth)*servoXlimit)),(round(midpoint[1]/(topHeight-bottomHeight)*servoYlimit)))
        return [angle[1],frame,[limitBottom,limitTop],[midpoint[0],midpoint[1]]]
    except IndexError:
        return [None,frame,[limitBottom,limitTop],[None,(limitTop-limitBottom)/2]]

# for debugging
if __name__ == "__main__":     
    cap = cv2.VideoCapture(0)
    a=0
    addedAngles=0   
    board = pyfirmata2.ArduinoNano('/dev/ttyACM0')
    alignmentServo = board.get_pin('d:11:s')
    alignmentServo.write(0)
    deg=0
    angle=[None,None]
    subflag=0
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    count=0
    movement=50  
    steps = 10
    print(f"camera width/height is (please verify): {(width,height)}")
    while angle[0]==None and count!=10:
        ret,frame=cap.read()
        frame = cv2.flip(frame, 1) 
        ret,frame=cap.read()
        frame = cv2.flip(frame, 1) 
        print("calibrating")
        angle = getAngleY(cap=cap,frame=frame)
        if angle[0]!=None:
            count+=1
            continue
        print(angle[0])
        cv2.imshow("frame",angle[1])
        alignmentServo.write(deg)
        if subflag:
            deg-=1
        else:
            deg+=1
        if deg==120:
            subflag=1
        if deg==0:
            subflag=0

    while True:
        ret,frame=cap.read()
        frame = cv2.flip(frame, 1) 
        #declare and assign variables
        angle = getAngleY(cap=cap,frame=frame)
        print(angle[0])
        cv2.imshow("frame",angle[1])
        if angle[0] != None:
            angle = getAngleY(cap=cap,frame=frame,percentage=10)
            if angle[3][1] <angle[2][0] and movement>0:
                print(angle[3][1])
                movement-=steps #i want to make it bezier
            elif angle[3][1]>angle[2][1] and movement<100:
                movement+=steps #i want to make it bezier
            else:
                movement+=0
            print(movement)
            alignmentServo.write(movement)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        
    cap.release()
    cv2.destroyAllWindows()
