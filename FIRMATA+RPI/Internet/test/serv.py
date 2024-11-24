import socket
import cv2 as cv

# read a test image
img = cv.imread('panda.jpg')
# encode it to jpg format, you can do this without redundant file openings
retval, buf = cv.imencode(".JPEG", img)
# get number of bytes
number_of_bytes = len(buf)
# create a null terminated string
header = "" + str(number_of_bytes) + "\0"
# encode it to utf-8 byte format
raw_header = bytes(header, "utf-8")
# create server socket
sock = socket.socket()
sock.bind(('localhost', 8000))
sock.listen()
conn, addr = sock.accept()
# send header first, reciever will use it to recieve image
conn.send(raw_header)
# send the rest of image
conn.send(buf)