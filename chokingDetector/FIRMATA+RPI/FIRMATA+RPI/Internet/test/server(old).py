import socket
import pickle

class server():
    def __init__(self,host='',port=5000):
        self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.bind((host,port))
        self.s.listen()
        
    def send(self,item):
        # self.conn, self.addr = self.s.accept()
        print("connected to",self.addr)
        item = pickle.dumps(item)
        self.conn.send(item)
        print("sent")
        
    def receive(self): #recieve data
        data=[]
        while True:
            packet = self.s.recv(4096)
            if not packet: break
            data.append(packet)
        data_arr = pickle.loads(b"".join(data))
        return data_arr
        
    def accept(self):
        self.conn, self.addr = self.s.accept()
        
    def close(self):
        self.conn.close()

import keyboard

if __name__ == "__main__":
    serverMachine = server()
    while not keyboard.is_pressed("q"):
        serverMachine.accept()
        value = serverMachine.receive()
        serverMachine.send("got it")
        
    serverMachine.close()
        
