import cv2
import socket
import struct
import numpy as np

HOST = 'server_ip_address'  # Replace with your server's IP address
PORT = 12345                # Must be the same as the server's port

def main():
    cap = cv2.VideoCapture(0)  # Open the default camera

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print('Failed to capture frame')
                break

            # Encode the frame as JPEG
            result, frame_encoded = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
            data = frame_encoded.tobytes()

            # Send the size of the data and the data itself
            data_length = struct.pack('!I', len(data))
            s.sendall(data_length)
            s.sendall(data)

            # Receive the size of the incoming data
            data_length_bytes = recvall(s, 4)
            if not data_length_bytes:
                print('Failed to receive data length from server')
                break
            data_length = struct.unpack('!I', data_length_bytes)[0]

            # Receive the actual data
            data = recvall(s, data_length)
            if not data:
                print('Failed to receive data from server')
                break

            # Decode the received frame
            frame_data = np.frombuffer(data, dtype='uint8')
            frame_received = cv2.imdecode(frame_data, cv2.IMREAD_COLOR)

            # Display the received frame
            cv2.imshow('Received Frame', frame_received)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        s.close()
        cap.release()
        cv2.destroyAllWindows()

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
    main()
