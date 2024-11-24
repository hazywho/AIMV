import socket
import struct
import numpy as np
import cv2

HOST = ''  # Listen on all network interfaces
PORT = 8000     # Port to listen on
class server():
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((HOST, PORT))
        self.s.listen(5)
        print(f"Server listening on {HOST}:{PORT}")
        self.conn, addr = self.s.accept()
        print(f"Connected by {addr}")
        
    def getFrame(self):
        # Receive the length of the incoming data
        data_length_bytes = self.recvall(self.conn, 4)

        data_length = struct.unpack('!I', data_length_bytes)[0]

        # Receive the actual data
        data = self.recvall(self.conn, data_length)

        print(data)
        received_Data= np.frombuffer(data,dtype="uint8")
        frame= cv2.imdecode(received_Data,cv2.IMREAD_COLOR)
        
        # Send back the length and data
        self.conn.sendall(data_length_bytes)
        self.conn.sendall(data)
        return frame

    def end(self):
        self.conn.close()

    def recvall(self, sock, count):
        """Helper function to receive exactly count bytes from the socket."""
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf:
                return None
            buf += newbuf
            count -= len(newbuf)
        return buf

if __name__ == '__main__':
    m = server()
    while True:
        frame = m.request()
        cv2.imshow("f",frame)
        if cv2.waitKey(1) & 0xFF==ord("q"):
            break
    
    m.end()
    cv2.destroyAllWindows()