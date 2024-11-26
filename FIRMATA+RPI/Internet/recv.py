import cv2
import socket
import struct

#is actually server
class client():
    def __init__(self, PORT=8000, HOST=""):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((HOST, PORT))
        self.s.listen(5)
        print(f"Server listening on {HOST}:{PORT}")
        self.conn, addr = self.s.accept()
        print(f"Connected by {addr}")

    def encode_frame(self, frame):
        # Encode the frame as JPEG
        result, frame_encoded = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
        data = frame_encoded.tobytes()
        # Prepare the data length
        data_length = struct.pack('!I', len(data))
        return data_length, data

    def send_frame(self, frame):
        data_length, data = self.encode_frame(frame)
        try:
            self.conn.sendall(data_length)
            self.conn.sendall(data)
        except BrokenPipeError:
            print("Connection closed by the client.")
            return False
        return True

    def close(self):
        self.conn.close()
        self.s.close()

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)  # Open the default camera
    server = client()
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        success = server.send_frame(frame)
        if not success:
            break
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()
    server.close()
