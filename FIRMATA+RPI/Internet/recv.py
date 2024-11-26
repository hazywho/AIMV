import socket
import struct
import numpy as np
import cv2

class Server:
    def __init__(self, PORT=8000, HOST=""):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((HOST, PORT))
        self.s.listen(5)
        print(f"Server listening on {HOST}:{PORT}")
        self.conn, addr = self.s.accept()
        print(f"Connected by {addr}")

    def get_frame(self):
        # Receive the length of the incoming data
        data_length_bytes = self.recvall(self.conn, 4)
        if not data_length_bytes:
            return None
        data_length = struct.unpack('!I', data_length_bytes)[0]

        # Receive the actual data
        data = self.recvall(self.conn, data_length)
        if not data:
            return None

        received_data = np.frombuffer(data, dtype="uint8")
        frame = cv2.imdecode(received_data, cv2.IMREAD_COLOR)
        return frame

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

    def close(self):
        self.conn.close()
        self.s.close()

if __name__ == '__main__':
    server = Server()
    while True:
        frame = server.get_frame()
        if frame is None:
            break
        cv2.imshow("Received Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cv2.destroyAllWindows()
    server.close()
