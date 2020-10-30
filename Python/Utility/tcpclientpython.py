import socket
# import time
# import select

# TCP_IP = '192.168.0.50'
# TCP_PORT = 5005
# TCP_IP = '192.168.0.2'
# TCP_PORT = 2000
TCP_IP = '192.168.0.11'
TCP_PORT = 10000
BUFFER_SIZE = 1024
MESSAGE = b'123456789\r\n'

print("Running...")

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((TCP_IP, TCP_PORT))
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.connect((TCP_IP, TCP_PORT))
TCP_PORT = 5006
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.connect((TCP_IP, TCP_PORT))

print("Connection established")

# Als andere kant timeout is gegaan
# ConnectionAbortedError: [WinError 10053] An established connection was aborted by the software in your host machine

# Als andere kant gekilled is ergens geleden of nu
# ConnectionResetError: [WinError 10054] An existing connection was forcibly closed by the remote host

# Spreekt voor zich
# socket.timeout: timed out

# s1.settimeout(2)

# def refresh():
#     # read_sockets, write_sockets, error_sockets = select.select([s1, s2], [s1, s2], [s1, s2])
#     for l in select.select([s1, s2], [s1, s2], [s1, s2]):
#         print("[", end="")
#         for s in l:
#             if s == s1: print("s1", end="")
#             elif s == s2: print("s2", end="")
#             else: print("0", end="")
#         print("]")


while True:
    if int(input()) == 2:
        # refresh()
        print(s2.send(b"A"))
        print(s2.recv(BUFFER_SIZE).decode())
    else:
        # refresh()
        print(s1.send(b"A"))
        print(s1.recv(BUFFER_SIZE).decode())
    # print(s1.send(input().encode()))
    # print(s1.recv(BUFFER_SIZE).decode())
    # print(s2.send(input().encode()))
    # print(s2.recv(BUFFER_SIZE).decode())
    # print(s.send(b""))
    # time.sleep(1)

# s.close()
"""
def flush():
    while len(s.recv(BUFFER_SIZE)) == BUFFER_SIZE:
        pass

def line():
    flush()
    print(s.recv(BUFFER_SIZE))

b'\x02\x02\x00\x05d\x01\x00\x00\x00\x00\x00'
s.send(b'\x03\x02\x00\x05d\x01\x00\x00\x00\x00\x00')
"""
