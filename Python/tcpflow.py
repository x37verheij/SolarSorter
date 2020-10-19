# subst X: "D:\Technische Informatica\2020-2021\Project GTM\Python"

import sys
import socket as SOCKET
from collections import namedtuple

# General Socket properties
s_size = 255                # Can receive up to 255 bytes
s_ipv4 = SOCKET.AF_INET     # Use ipv4 configuration
s_tcp = SOCKET.SOCK_STREAM  # Use TCP configuration

#############
# Functions #
#############

# Connect function
def connect(device):
    device.socket.connect((device.ip, device.port))
    print(device.name, " connected at ", device.ip, ":", device.port, sep="")

# Login function
def login(device):
    if "User" not in device.socket.recv(s_size).decode():   # Welcome to In-Sight(tm)  7200C Session 0
        device.socket.recv(s_size)                          # User:
    device.socket.send(b"admin\r\n")
    device.socket.recv(s_size)                              # Password:
    device.socket.send(b"\r\n")
    device.socket.recv(s_size)                              # User Logged In
    print(device.name, "login success")

# Send function
def send(device, msg):
    print("PC > ", device.name, ":\t", msg.encode(), sep="")
    device.socket.send(msg.encode())

# Receive function
def receive(device):
    data = device.socket.recv(s_size).decode()
    if device in [qrCamera, invoerCamera]:
        data = data.split("\r\n")[1]
    print(device.name, " > PC:\t", data, sep="")

# Disconnect function
def disconnect(device):
    device.socket.close()

# Create new socket function
def newSocket():
    return SOCKET.socket(s_ipv4, s_tcp)

#####################
# Device properties #
#####################

# Device object to enable named fields: camera.socket instead of camera[2]
# Note: tuples are immutable, so editing a value requires: device1 = device1._replace(port = 10)
Device = namedtuple("Device", "name, ip, port, socket")

# Properties of the connecting devices (Name, IP, Port, Client socket)
robot = Device("Robot", "192.168.0.1", 10000, newSocket())
plc = Device("PLC", "192.168.0.2", 2000, newSocket())
qrCamera = Device("QRcam", "192.168.0.10", 10000, newSocket())
invoerCamera = Device("INcam", "192.168.0.11", 10000, newSocket())

###################
# Connect devices #
###################

# Setup a client socket for the Robot and connect
print("Connecting to Robot...", end="\r", flush=True)
connect(robot)

# Setup a client socket for the PLC and connect
print("Connecting to PLC...", end="\r", flush=True)
connect(plc)

# Setup a client socket for the QR Camera, connect and login
print("Connecting to QR Camera...", end="\r", flush=True)
connect(qrCamera)
login(qrCamera)

# Setup a client socket for the Invoer Camera, connect and login
print("Connecting to Invoer Camera...", end="\r", flush=True)
connect(invoerCamera)
login(invoerCamera)

print("")

#############################
# Send and receive messages #
#############################

for i in range(0, 2):
    # Test connection with the Robot
    send(robot, "abcd")
    receive(robot)

    # Test connection with the PLC
    send(plc, "1234")
    receive(plc)

    # Test connection with the QR Camera
    send(qrCamera, "gvb002\r\n")
    receive(qrCamera)

    # Test connection with the Invoer Camera
    send(invoerCamera, "gvb002\r\n")
    receive(invoerCamera)

######################
# Disconnect devices #
######################

disconnect(robot)
disconnect(plc)
disconnect(qrCamera)
disconnect(invoerCamera)
