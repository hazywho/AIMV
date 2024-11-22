import socket

class client():
    def __init__(self,host='LAPTOP-D32MH4UH',port=5000):
        self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.connect((host,port))
        
    def send(self,item):
        self.s.send(bytes(str(item),"utf-8"))
        print("sent")
        
    def receive(self):
        try:
            self.data = self.s.recv(134217728)
            print("recieved image")
            return self.data
        except socket.gaierror:
            return None

# import socket
# import time
# HOST = 'LAPTOP-D32MH4UH'    # The remote host
# PORT = 5000              # The same port as used by the server

# while True:
#     time.sleep(0.001)
#     try:
#         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         s.connect((HOST, PORT))
#         data=s.recv(16384)
#         if data:
#             s.send(bytes("1","utf-8"))
#         print ('Received', data.decode("utf-8"))
#     except socket.gaierror:
#         continue
    
