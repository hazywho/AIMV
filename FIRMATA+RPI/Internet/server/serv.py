import cv2
import socket
import struct

class Client:
    def __init__(self, HOST='localhost', PORT=8000):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST, PORT))
        print(f"Connected to {HOST}:{PORT}")

    def encode_frame(self, frame):
        # Encode the frame as JPEG
        result, frame_encoded = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
        data = frame_encoded.tobytes()
        # Prepare the data length
        data_length = struct.pack('!I', len(data))
        return data_length, data

    def send_frame(self, frame):
        data_length, data = self.encode_frame(frame)
        self.s.sendall(data_length)
        self.s.sendall(data)

    def close(self):
        self.s.close()

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)  # Open the default camera
    client = Client()
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        client.send_frame(frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()
    client.close()
