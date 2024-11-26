import socket
import struct
import numpy as np
import cv2

#is actually client
class server():
    def __init__(self, HOST='raspberrypi', PORT=8000):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST, PORT))
        print(f"Connected to {HOST}:{PORT}")

    def get_frame(self):
        # Receive the length of the incoming data
        data_length_bytes = self.recvall(4)
        if not data_length_bytes:
            return None
        data_length = struct.unpack('!I', data_length_bytes)[0]

        # Receive the actual data
        data = self.recvall(data_length)
        if not data:
            return None

        # Decode the frame
        received_data = np.frombuffer(data, dtype="uint8")
        frame = cv2.imdecode(received_data, cv2.IMREAD_COLOR)
        return frame

    def recvall(self, count):
        """Helper function to receive exactly count bytes from the socket."""
        buf = b''
        while count:
            newbuf = self.s.recv(count)
            if not newbuf:
                return None
            buf += newbuf
            count -= len(newbuf)
        return buf

    def close(self):
        self.s.close()

if __name__ == '__main__':
    client = server()
    while True:
        frame = client.get_frame()
        if frame is None:
            print("No frame received. Exiting...")
            break
        cv2.imshow("Received Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cv2.destroyAllWindows()
    client.close()
