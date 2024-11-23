import cv2

cap = cv2.VideoCapture(0)

while True:
    ret,frame=cap.read()
    print(frame.shape[0],frame.shape[1])
    cv2.imshow("f",frame)
    
    if cv2.waitKey(1) & 0xFF==ord("q"):
        break
    
cap.release()
cv2.destroyAllWindows()