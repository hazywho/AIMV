from ultralytics import YOLO
import cv2
import time
import motorSystem
import RPi.GPIO as GPIO
from lens.predictor import protocol
import math
import faceDetector

cap = cv2.VideoCapture(0)
model = YOLO("yolo11n.pt")
model.to("cuda")
huskee = protocol("I2C")
a=0
addedAngles=0
#algo to get the biggest bounding box
def getBiggest(l):
    return abs(l[2]-l[0])+abs(l[3]-l[1])
motorSystem.moveCamTo(0)
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
