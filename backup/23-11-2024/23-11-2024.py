import socket
import time
HOST = 'LAPTOP-D32MH4UH'    # The remote host
PORT = 5000              # The same port as used by the server

while True:
    time.sleep(0.001)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        data=s.recv(16384)
        if data:
            s.send(bytes("1","utf-8"))
        print ('Received', data.decode("utf-8"))
    except socket.gaierror:
        continue