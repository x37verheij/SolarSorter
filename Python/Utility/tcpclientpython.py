import socket
import time


# TCP_IP = '192.168.0.50'
# TCP_PORT = 5005
TCP_IP = '192.168.0.2'
TCP_PORT = 2000
# TCP_IP = '192.168.0.11'
# TCP_PORT = 10000
BUFFER_SIZE = 1024
MESSAGE = b'1234\r\n'

print("Running...")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

print("Connection established")

t = int(time.time())

while 1:
    if (int(time.time()) > t):
        s.send(MESSAGE)
        t = int(time.time())
        print("Sent data on timestamp", t)

        data = s.recv(BUFFER_SIZE)
        print("Received data", data)

# while 1:
# s.send(MESSAGE)
# print("Sent data", MESSAGE)

# data = s.recv(BUFFER_SIZE)
# print("Received data", data)

# s.close()
