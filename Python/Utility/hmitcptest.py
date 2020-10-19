# HMI TCP Test program

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

# Send function
def send(device, msg):
    print("PC :", msg.encode())
    device.socket.send(msg.encode())

# Receive function
def receive(device):
    data = device.socket.recv(s_size).decode()
    print(device.name, ": ", data, sep="")
    return data

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
plc = Device("PLC", "192.168.0.2", 2000, newSocket())

###################
# Connect devices #
###################

# Setup a client socket for the PLC and connect
print("Connecting to PLC...", end="\r", flush=True)
connect(plc)

#############################
# Main program #
#############################

print("Type your message. Send with enter key...", end="\n> ")

while True:
    msg = input()
    send(plc, msg)
    receive(plc)
    print("> ", end="")

# disconnect(plc)
