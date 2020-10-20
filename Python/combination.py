# subst X: "D:\Technische Informatica\2020-2021\Project GTM\Python"

import time
import socket as SOCKET
from collections import namedtuple
from openpyxl import load_workbook
from openpyxl import cell as xlcell

# Documentation for openpyxl:
# https://openpyxl.readthedocs.io/en/stable/

# Path to Excel sheet and its contents (where (k, v) is (serialnr, grade))
xlsxPath = "80518_Measurement Data_Lot XXX.xlsx"
excelData = {}

# General Socket properties
s_size = 255                # Can receive up to 255 bytes
s_ipv4 = SOCKET.AF_INET     # Use ipv4 configuration
s_tcp = SOCKET.SOCK_STREAM  # Use TCP configuration

# Time variables to keep connections alive and avoid timeouts by refreshing
refreshInterval = 50        # Seconds
lastRefresh = time.time()   # Timestamp of last refresh of the robot

# Time interval to check whether connections are still alive
# TODO

#############
# Functions #
#############

# Read Excel function
def readExcel():
    wb = load_workbook(filename = xlsxPath, data_only = True, read_only = True)
    ws = wb.active

    # Grab columns M, N and O (col M has grades, col O has serial numbers)
    rows = ws["M1:O20"]

    # Collect all serial numbers and their corresponding grades
    for row in rows:
        if type(row[0]) is not xlcell.read_only.EmptyCell and type(row[0].value) is int:
            grade = row[0].value
            serialnr = row[2].value
            print("Cell", serialnr, "has grade", grade)
            excelData[serialnr] = grade

# TCP Connect function
def connect(device):
    device.socket.connect((device.ip, device.port))
    print(device.name, " connected at ", device.ip, ":", device.port, sep="")

# TCP Login function
def login(device):
    if "User" not in device.socket.recv(s_size).decode():   # Welcome to In-Sight(tm)  7200C Session 0
        device.socket.recv(s_size)                          # User:
    device.socket.send(b"admin\r\n")
    device.socket.recv(s_size)                              # Password:
    device.socket.send(b"\r\n")
    device.socket.recv(s_size)                              # User Logged In
    print(device.name, "login success")

# TCP Send function
def send(device, msg):
    print("PC > ", device.name, ":\t", msg.encode(), sep="")
    device.socket.send(msg.encode())

# TCP Receive function
def receive(device):
    data = device.socket.recv(s_size).decode()
    if device in [qrCamera, invoerCamera]:
        data = data.split("\r\n")[1]
    print(device.name, " > PC:\t", data, sep="")

# TCP Disconnect function
def disconnect(device):
    device.socket.close()

# Create new socket function
def newSocket():
    s = SOCKET.socket(s_ipv4, s_tcp)
    s.settimeout(5)
    return s

#####################
# HMI message class #
#####################

# HMI Message object for easy read/write access.
class HMImessage:
    """All fields in a HMImessage object retain their values
    // air [0, 1]: turn air pressure on/off [out]
    // light [0, 1]: turn led strip on/off [out]
    // excel [0, 1, 2, 3]: reserved [inout]
    // grade [7-10, 100]: the grade of the cell that has just been classified [inout]
    // outputTray [7-10, 100]: when that output tray needs replacement [inout]
    // trays [0, 1-6]: start signal, the amount of trays stacked on the input pile [in]
    // halt [0, 1]: whether the user asked for a soft stop via the HMI [in]
    // done [0, 1]: whether all cells have been sorted to their output trays [out]
    // conn... [0, 1]: whether the connections with these devices are still live [out]
    """
    def __init__(self):
        self.air, self.light, self.excel, self.grade = 0, 0, 0, 100
        self.outputTray, self.trays, self.halt, self.done = 100, 0, 0, 0
        self.connRobot, self.connQRcam, self.connINcam = 0, 0, 0
    
    # Decodes and stores the received message
    def decode(self, msg):
        (self.air, self.light, self.excel, self.grade, self.outputTray, self.trays, self.halt,
            self.done, self.connRobot, self.connQRcam, self.connINcam) = [ord(i) for i in msg]
    
    # Concatenate the properties of this object into a string (without encoding)
    def encode(self):
        return (chr(self.air) + chr(self.light) + chr(self.excel) + chr(self.grade) +
            chr(self.outputTray) + chr(self.trays) + chr(self.halt) + chr(self.done) +
                chr(self.connRobot) + chr(self.connQRcam) + chr(self.connINcam))

# Instantiate the class
HMImsg = HMImessage()

#####################
# Device properties #
#####################

# Device object to enable named fields: camera.socket instead of camera[2]
Device = namedtuple("Device", "name, ip, port, socket")

# Properties of the connecting devices (Name, IP, Port, Client socket)
plc = Device("PLC", "192.168.0.2", 2000, newSocket())  # Connect first to the HMI via the PLC
robot = Device("Robot", "192.168.0.1", 10000, newSocket())
qrCamera = Device("QRcam", "192.168.0.10", 10000, newSocket())
invoerCamera = Device("INcam", "192.168.0.11", 10000, newSocket())

###################
# Connect devices #
###################

# Setup a client socket for the PLC and connect
print("Connecting to PLC...", end="\r", flush=True)
connect(plc)

# Setup a client socket for the Robot and connect
print("Connecting to Robot...", end="\r", flush=True)
connect(robot)
HMImsg.connRobot = 1
send(plc, HMImsg.encode())

# Setup a client socket for the QR Camera, connect and login
print("Connecting to QR Camera...", end="\r", flush=True)
connect(qrCamera)
login(qrCamera)
HMImsg.connQRcam = 1
send(plc, HMImsg.encode())

# Setup a client socket for the Invoer Camera, connect and login
print("Connecting to Invoer Camera...", end="\r", flush=True)
connect(invoerCamera)
login(invoerCamera)
HMImsg.connINcam = 1
send(plc, HMImsg.encode())

print("")

################
# Main program #
################

# Connections are established, so we wait for the user to start the program on the HMI # TODO keep connections alive and check them
while True:
    try:
        HMImsg.decode(receive(plc))
        if HMImsg.trays != 0:       # Indicates program start
            break
    except:
        # TODO refresh. Above line already timeouts every 5 seconds
        pass


for i in range(0, 2):
    # Test connection with the Robot
    # send(robot, "abcd")
    # receive(robot)

    # Test connection with the PLC
    # send(plc, "1234")
    # receive(plc)

    # Test connection with the QR Camera
    send(qrCamera, "gvb002\r\n")
    receive(qrCamera)

    # Test connection with the Invoer Camera
    send(invoerCamera, "gvb002\r\n")
    receive(invoerCamera)

    time.sleep(2)

######################
# Disconnect devices #
######################

disconnect(robot)
disconnect(plc)
disconnect(qrCamera)
disconnect(invoerCamera)
