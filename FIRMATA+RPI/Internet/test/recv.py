import socket

# create client socket
sock = socket.socket()
sock.connect(('localhost', 8000))

# recieve bytes until null termination
raw_header = []
recv_byte = sock.recv(1)

while recv_byte != b"\0":
    raw_header.append(recv_byte)
    recv_byte = sock.recv(1)

# decode header
header = str(b''.join(raw_header), "utf-8")
# recieve the amount of bytes foretold by header
recv_img = sock.recv(int(header))
# save image to file or you can use cv2.imendecode to turn it back to numpy.ndarray (cv2 image format)
with open("traveller_panda.jpg", 'wb+') as im_file:
    im_file.write(recv_img)


# transform back from jpg to numpy array
image_decoded = np.frombuffer(recv_img, dtype=np.uint8)
image_decoded = cv.imdecode(image_decoded, cv.IMREAD_COLOR)
# display image
cv.imshow("recieved", image_decoded)
cv.waitKey()