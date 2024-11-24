import socket
import struct

HOST = ''  # Listen on all network interfaces
PORT = 8000     # Port to listen on

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"Server listening on {HOST}:{PORT}")

    conn, addr = s.accept()
    print(f"Connected by {addr}")

    try:
        while True:
            # Receive the length of the incoming data
            data_length_bytes = recvall(conn, 4)
            if not data_length_bytes:
                break
            data_length = struct.unpack('!I', data_length_bytes)[0]

            # Receive the actual data
            data = recvall(conn, data_length)
            if not data:
                break

            # Send back the length and data
            conn.sendall(data_length_bytes)
            conn.sendall(data)
    finally:
        conn.close()

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