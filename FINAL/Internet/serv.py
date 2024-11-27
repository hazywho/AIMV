import cv2
import socket
import struct
import json

#is actually server
class client():
    def __init__(self, PORT=8000, HOST=""):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((HOST, PORT))
        self.s.listen(5)
        print(f"Server listening on {HOST}:{PORT}")
        self.conn, addr = self.s.accept()
        print(f"Connected by {addr}")

    def encode(self, frame):
        # Encode the frame as JPEG
        result, frame_encoded = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
        data = frame_encoded.tobytes()
        # Prepare the data length
        data_length = struct.pack('!I', len(data))
        return data_length, data

    def sendAndCalculate(self, frame):
        data_length, data = self.encode(frame)
        try:
            #send length of data and data
            self.conn.sendall(data_length)
            self.conn.sendall(data)
            
            # Receive the size of the incoming data
            data_length_bytes = self.recvall(self.conn, 4)
            data_length = struct.unpack('!I', data_length_bytes)[0]
            
            #receive actual data
            data = self.recvall(self.conn, data_length)
            json_data=data.decode("utf-8")
            frame_data= json.loads(json_data)
            
            return frame_data
        except BrokenPipeError:
            print("Connection closed by the client.")
            return False
    
    def recvall(self,sock, count):
        """Helper function to receive exactly count bytes from the socket."""
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf:
                return None
            buf += newbuf
            count -= len(newbuf)
        return buf
    
    def end(self):
        self.conn.close()
        self.s.close()

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)  # Open the default camera
    server = client()
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        success = server.sendAndCalculate(frame)
        if not success:
            break
        print(success)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()
    server.end()
