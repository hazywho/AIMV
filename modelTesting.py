from ultralytics import YOLO
import cv2
import time

cap = cv2.VideoCapture(0)
model = YOLO("yolo11s.pt")
model.to("cuda")
while True:
    ret,frame=cap.read()
    frame = cv2.flip(frame, 1) 
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    print((width,height))
    cv2.rectangle(frame, (64,48),(576,432),color=(255,0,0),thickness=1)
    
    prediction = model.predict(source=frame,stream_buffer=False,classes=[0],verbose=False)
    for index,xyxy in enumerate(prediction[0].boxes.xyxy):
        classes = prediction[0].names[prediction[0].boxes.cls.tolist()[index]]
        midpoint = list(map(lambda x:int(x), prediction[0].boxes.xywh.tolist()[index][:2]))
        boxes = [int(val) for val in xyxy.tolist()]
        cv2.rectangle(frame, (boxes[0],boxes[1]),(boxes[2],boxes[3]),color=(255,0,0),thickness=2)
        cv2.putText(frame,classes,(boxes[0],boxes[1]-10),cv2.FONT_HERSHEY_COMPLEX,1,color=(0,0,0),thickness=2,lineType=cv2.LINE_AA)
        print(f"midpoint at {midpoint}")
        
        servoXlimit=180
        servoYlimit=90
        angle = ((round(midpoint[0]/width*servoXlimit)),(round(midpoint[1]/height*servoYlimit)))
        print(f"angle of xy is: {angle}")
        
    cv2.imshow("frame",frame)
    time.sleep(0.1)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()