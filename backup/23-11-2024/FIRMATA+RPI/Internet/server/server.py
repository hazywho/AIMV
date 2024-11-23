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
        
    def receive(self,maxByteSize=134217728): #recieve data
        self.conn, self.addr = self.s.accept()
        self.data = self.conn.recv(maxByteSize)
        print("received")
        return self.data.decode("utf-8")
        
    def close(self):
        self.conn.close()
