y= plus minus 10%
x = plus minus 15%

code is pretty messed up
 
steps we can take to increase speed/reduce lag.

- better communication
- better processing method destributions
















# boxes = [value[4][0],value[4][1],value[5][0],value[5][1]]
# midpoint=[value[3][0],value[3][1]]
# limitBottom=value[1][0]
# limitTop=value[1][1]
# limitLeft=value[2][0]
# limitRight=value[2][1]
# width=value[7][0]
# height=value[7][1]
# classes=value[6][1]
# confidence=value[6][0]

# #y top/bottom limit
# frame = cv2.line(frame, (0,limitTop), (round(width),limitTop), (0,255,0), 1)
# frame = cv2.line(frame, (0,limitBottom), (round(width),limitBottom), (0,255,0), 1)
# #x left/right limit
# frame = cv2.line(frame, (limitLeft,0), (limitLeft,round(height)), (0,255,0), 1)
# frame = cv2.line(frame, (limitRight,0), (limitRight,round(height)), (0,255,0), 1)
# print(midpoint)
# if value[0][0]==1 and value[0][1]==1:
#     #putting boxes on detrected items
#     cv2.rectangle(frame, (boxes[0],boxes[1]),(boxes[2],boxes[3]),color=(255,0,0),thickness=2)

#     #midpoiconfidence
#     frame = cv2.circle(frame, (midpoint[0],midpoint[1]), radius=10, color=(0, 0, 255), thickness=-1)
#     cv2.putText(frame,f"{classes}, {confidence}",(boxes[0],boxes[1]-10),cv2.FONT_HERSHEY_COMPLEX,1,color=(0,0,0),thickness=2,lineType=cv2.LINE_AA)

