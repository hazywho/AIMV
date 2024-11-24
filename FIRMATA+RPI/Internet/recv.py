import cv2
import socket
import struct
import numpy as np

HOST = 'shiroles'  # Replace with your server'self.s IP address
PORT = 8000               # Must be the same as the server'self.s port

class client():
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST, PORT))
        
    def encode(self,src):
        # Encode the frame as JPEG
        result, frame_encoded = cv2.imencode('.jpg', src, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
        data = frame_encoded.tobytes()

        # Send the size of the data and the data itself
        data_length = struct.pack('!I', len(data))
        
        return data,data_length
        
    def sendAndCalculate(self,frame):
        data,data_length = self.encode(frame)
        self.s.sendall(data_length)
        self.s.sendall(data)

        # Receive the size of the incoming data
        data_length_bytes = self.recvall(self.s, 4)

        data_length = struct.unpack('!I', data_length_bytes)[0]

        # Receive the actual data
        data = self.recvall(self.s, data_length)

        # Decode the received frame
        frame_data = np.frombuffer(data, dtype='uint8')
        print(frame_data)
        
        return frame_data
            
    def end(self):
        self.s.close()

    def recvall(sock, count):
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
    cap = cv2.VideoCapture(0)  # Open the default camera
    m = client()
    while True:
        ret,frame=cap.read()
        # Display the received frame
        r = m.sendAndCalculate()
        cv2.imshow('Received Frame', r[1])
        if cv2.waitKey(1) & 0xFF==ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()

