import socket

class client():
    def __init__(self,host='shiroes',port=5000):
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


    
