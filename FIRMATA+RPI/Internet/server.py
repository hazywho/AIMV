import socket

class server():
    def __init__(self,host='',port=5000):
        self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.bind((host,port))
        self.s.listen()
        
    def send(self,item):
        self.conn, self.addr = self.s.accept()
        print("connected to",self.addr)
        self.conn.send(bytes(str(item),"utf-8"))
        print("sent")
        
    def receive(self,maxByteSize=2048): #recieve data
        self.conn, self.addr = self.s.accept()
        self.data = self.conn.recv(maxByteSize)
        print("received")
        return self.data.decode("utf-8")
        
    def close(self):
        self.conn.close()

# cap = cv2.VideoCapture(0)
# HOST = ''                 # Symbolic name meaning all available interfaces
# PORT = 5000       # Arbitrary non-privileged port
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind((HOST, PORT))
# s.listen()
# flag = False
# while True:
#     _,frame=cap.read()
#     conn, addr = s.accept()
#     print('Connected by', addr)
#     conn.send(bytes(str(frame),"utf-8"))
#     data = conn.recv(134217728)
#     print("sent")
#     cv2.imshow("frame",frame)
#     if cv2.waitKey(1) & 0xFF==ord("q"):
#         break

# cap.release()
# conn.close()
# cv2.destroyAllWindows()

