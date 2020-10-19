import socket


TCP_IP = '192.168.0.50'
TCP_PORT = 5005
BUFFER_SIZE = 32  # Normally 1024, but we want fast response

print("debug1")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

print("debug2")

conn, addr = s.accept()
print('Connection address:', addr)
while 1:
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    print("received data:", data)
    conn.send(data)  # echo
conn.close()
