# subst X: "D:\Technische Informatica\2020-2021\Project GTM\Python"

"""
Voor het eerste bedrijfsproject in de minor heeft GTM gevraagd of wij een systeem kunnen bouwen die trays met zonnecellen en een excelsheet accepteert en dat omzet naar gesorteerde trays met ieder een bepaalde klasse cellen. De robot zal initieel verbinding maken met de TCP server van de python pc en reageren op elk bericht dat de pc stuurt.
Gedurende het programma zal de robot vanuit de rustpositie wachten tot de pc uit de invoercamera beeld heeft ontvangen en de robot vertelt waar de ongesorteerde cellen liggen. De robot pakt dan een voor een elke ongesorteerde cel op en verplaatst deze boven de qrcamera. De robot zal de pc een bericht sturen dat deze op locatie is.
De pc zal het serienummer laten scannen door de qrcamera en koppelen aan deze cel in de eerste foto. Vervolgens wordt de klasse opgezocht in de excelsheet en stuurt de pc de klasse naar de robot. De robot verplaatst de cel dan naar de uitvoertray met cellen van die klasse. De robot verplaatst zich dan weer naar de rustpositie.
Mocht een uitvoertray vol zitten, laat de robot dit via de pc weten en stopt met verdergaan totdat hij expliciet te horen krijgt dat de uitvoertray is verwijderd. Dit gaat via de hmi. Vervolgens plaatst de robot een lege tray op de geleegde plek en vervolgt hij zijn programma.
Mocht de invoertray leeg zijn, dan vertelt de pc niet welke cel de robot moet pakken, maar dat de tray leeg is en vervangen moet worden. De robot verplaatst dan de lege tray en gaat terug naar de rustpositie. De robot laat vervolgens de pc vertellen waar de volgende cellen liggen en gaat deze een na een af.
"""

import re                               # Regular expressions
import sys                              # System variables, like error values
import cv2                              # Opencv, for image extraction
import time                             # To measure time intervals
import socket                           # To connect to all devices with the TCP protocol
from ftplib import FTP                  # FTP protocol to download images from the cameras
from collections import namedtuple      # Datatype for easy access to device properties
from openpyxl import load_workbook      # Function to import Excel sheets
from openpyxl import cell as xlcell     # Compare and extract Excel cell properties

# Documentation for openpyxl: https://openpyxl.readthedocs.io/en/stable/
# Documentation for opencv:   https://docs.opencv.org/master/

# Path to Excel sheet and a dict for its contents (where (k, v) is (serialnr, grade))
xlsxPath = "80518_Measurement Data_Lot XXX.xlsx"
excelData = {}

# General Socket properties
s_size = 255                # Can receive up to 255 bytes
s_ipv4 = socket.AF_INET     # Use ipv4 configuration
s_tcp = socket.SOCK_STREAM  # Use TCP configuration

# Variables to keep connections alive and avoid timeouts by refreshing
timeout = 10                # Seconds
lastRefresh = time.time()   # Timestamp of last refresh

# Time interval to check whether connections are still alive
# TODO

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
    // status [0, 1, 2]: either not started, started or finished [inout]
    // conn... [0, 1]: whether the connections with these devices are still live [out]
    """
    def __init__(self):
        self.air, self.light, self.excel, self.grade = 0, 0, 0, 100
        self.outputTray, self.trays, self.halt, self.status = 100, 0, 0, 0
        self.connRobot, self.connQRcam, self.connINcam = 0, 0, 0
    
    # Decodes and stores the received message
    def fromString(self, msg):
        (self.air, self.light, self.excel, self.grade, self.outputTray, self.trays, self.halt,
            self.status, self.connRobot, self.connQRcam, self.connINcam) = [ord(i) for i in msg]
    
    # Concatenate the properties of this object into a string (without encoding)
    def toString(self):
        return (chr(self.air) + chr(self.light) + chr(self.excel) + chr(self.grade) +
            chr(self.outputTray) + chr(self.trays) + chr(self.halt) + chr(self.status) +
                chr(self.connRobot) + chr(self.connQRcam) + chr(self.connINcam))

# Instantiate the class
HMImsg = HMImessage()

#################
# Counter class #
#################

# Counter object that keeps track of the occupied output spaces
class Counter:
    def __init__(self):
        self.outputs = [1, 1, 1, 1]     # Index 0 refers to grade 7, index 3 to grade 10
        self.emptyHeight = 0
        self.inputHeight = 0
    
    # Increments the counter for the output tray of this grade and returns its value after incrementing
    def increment(self, grade):
        self.outputs[grade - 7] += 1
        return self.outputs[grade - 7]
    
    # Resets the counter for the output tray of this grade to 0
    def reset(self, grade):
        self.outputs[grade - 7] = 1

# Instantiate the class
counter = Counter()

#############
# Functions #
#############

# Read the Excel sheet and collect its data
def readExcel():
    wb = load_workbook(filename = xlsxPath, data_only = True, read_only = True)
    ws = wb.active

    # Grab columns M, N and O (col M has grades, col O has serial numbers)
    rows = ws["M1:O500"]

    # Collect all serial numbers and their corresponding grades
    for row in rows:
        if type(row[0]) is not xlcell.read_only.EmptyCell and type(row[0].value) is int:
            grade = row[0].value
            serialnr = row[2].value
            # print("Cell", serialnr, "has grade", grade)
            excelData[serialnr] = grade
    wb.close()

# FTP Retrieve photo function
def retrievePhoto():
    ftp = FTP(invoerCamera.ip, user="admin", timeout=3)
    with open('image.jpg', 'wb') as imageBuffer:
        ftp.retrbinary('RETR image.jpg', imageBuffer.write)
        imageBuffer.close()
    ftp.quit()
    return cv2.imread("image.jpg")

# Opencv locate cells function
def locateCells(image):
    pass # TODO implement
    # returns list of filled locations
    return [3, 6, 12]
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

# TCP Disconnect function
def disconnect(device):
    device.socket.close()

# TCP Handle Errors function updates the connection info to display on the HMI and disconnect devices, perhaps
def handleError(device):
    print("TCP Error for device", device.name, sys.exc_info()[0])
    pass # TODO disconnect needs devices, which are declared later on...
    send(robot, "disconnect")
    disconnect(robot)
    disconnect(plc)
    disconnect(qrCamera)
    disconnect(invoerCamera)
    exit(-1)

# TCP Send function
def send(device, msg, verbal = True):
    try:
        if verbal: print("PC > ", device.name, ":\t", msg.encode(), sep="")
        device.socket.send(msg.encode())
    except:
        handleError(device)

# TCP Receive function. If index is provided, the received data will be split
def receive(device, index = None, verbal = True):
    if device == plc:
        flush(plc)
    try:
        data = device.socket.recv(s_size)
        if verbal: print(device.name, " > PC:\t", data, sep="")
        data = data.decode()
        if index is not None:
            data = data.split("\r\n")[index]
        return data
    except:
        handleError(device)

# TCP flush function that empties its receive buffer to ensure actual data (e.g. HMI keeps sending data)
def flush(device):
    try:
        while len(device.socket.recv(s_size)) == s_size:
            pass
    except:
        handleError(device)

# TCP Refresh function
def refresh():
    while True:
        print("Refreshing devices")
        lastRefresh = time.time()

        # Refresh all connections
        send(robot, "refresh", verbal = False)
        receive(robot, verbal = False)
        send(qrCamera, "refresh\r\n", verbal = False)
        receive(qrCamera, verbal = False)
        send(invoerCamera, "refresh\r\n", verbal = False)
        receive(invoerCamera, verbal = False)
        HMImsg.fromString(receive(plc, verbal = False))

        # If the program is running, not halted and no output trays are full, then return
        if HMImsg.status == 1 and HMImsg.halt == 0 and HMImsg.outputTray == 100:
            return

        # While within the timeout interval, check the PLC/HMI twice per second
        while time.time() - lastRefresh < timeout:
            HMImsg.fromString(receive(plc, verbal = False))

            # Return when the program is running, not halted and without full output trays
            if HMImsg.status == 1 and HMImsg.halt == 0 and HMImsg.outputTray == 100:
                return

            # Print some debug messages while waiting for the user to acknowledge via the HMI
            if HMImsg.status != 1: print("Waiting for start acknowledge by user via HMI...")
            if HMImsg.halt != 0: print("Program halted. Waiting for user acknowledge via HMI...")
            if HMImsg.outputTray != 100: print("Waiting for user to acknowledge ouput tray removal via HMI...")

            time.sleep(0.5)

# Robot Message function for easy message creation using convention "X-YY-ZZ"
def robotMsg(instruction, heightGrade, celIndex):
    heightGrade = str(heightGrade) if heightGrade > 9 else "0" + str(heightGrade)
    celIndex = str(celIndex) if celIndex > 9 else "0" + str(celIndex)
    return instruction + "-" + heightGrade + "-" + celIndex

# Create new socket function
def newSocket():
    s = socket.socket(s_ipv4, s_tcp)
    s.settimeout(timeout)
    return s

#####################
# Device properties #
#####################

# Device object to enable named fields: camera.socket instead of camera[2]
Device = namedtuple("Device", "name, ip, port, socket")

# Properties of the connecting devices (Name, IP, Port, Client socket)
# The PLC and cameras always immediately respond, since their socket handling is non-blocking. The robot will not
plc = Device("PLC", "192.168.0.2", 2000, newSocket())  # Connect to the HMI via the PLC
robot = Device("Robot", "192.168.0.1", 10000, newSocket())
qrCamera = Device("QRcam", "192.168.0.10", 10000, newSocket())
invoerCamera = Device("INcam", "192.168.0.11", 10000, newSocket())

############################################
# Read the excel sheet and connect devices #
############################################

# Read Excel sheet and put the data in excelData
readExcel()
print("Excel sheet has been read successfully")

# Setup a client socket for the PLC and connect
print("Connecting to PLC...", end="\r", flush=True)
connect(plc)

# Setup a client socket for the Robot and connect
print("Connecting to Robot...", end="\r", flush=True)
connect(robot)
HMImsg.connRobot = 1
send(plc, HMImsg.toString(), verbal = False)

# Setup a client socket for the QR Camera, connect and login
print("Connecting to QR Camera...", end="\r", flush=True)
connect(qrCamera)
login(qrCamera)
HMImsg.connQRcam = 1
send(plc, HMImsg.toString(), verbal = False)

# Setup a client socket for the Invoer Camera, connect and login
print("Connecting to Invoer Camera...", end="\r", flush=True)
connect(invoerCamera)
login(invoerCamera)
HMImsg.connINcam = 1
send(plc, HMImsg.toString(), verbal = False)

################
# Main program #
################

# Connections are established, so we wait for the user to start the program on the HMI
refresh()

# At this point, we received the amount of input trays from the HMI
counter.inputHeight = HMImsg.trays      # Start the size of the inputHeight at HMImsg.trays
send(robot, "neutral")                  # We then Instruct the robot to move to its neutral position
receive(robot)                          # Robot has reached its neutral position

# Repeat this loop while there are input trays left
while counter.inputHeight:
    refresh()                           # Revalidate all tcp connections
    send(invoerCamera, "sw8\r\n")       # Trigger a photo
    receive(invoerCamera, 0)            # Acknowledge
    locs = locateCells(retrievePhoto()) # Use FTP to retrieve the photo and locate all cells

    # Instruct the robot to go to cell i in the input tray "I" and also provide the height
    for i in locs:
        refresh()
        send(robot, robotMsg("I", counter.inputHeight, i))
        receive(robot)                  # Robot has reached cell location

        refresh()
        HMImsg.air = 1
        send(plc, HMImsg.toString())    # Instruct the PLC to enable the vacuum generator
        time.sleep(0.5)                 # Give the PLC time to process
        HMImsg.fromString(receive(plc)) # Collect response and store it

        refresh()
        send(robot, "scan")             # Instruct the robot to move the cell to the QR camera for a scan
        receive(robot)                  # Robot has reached its destination

        refresh()
        HMImsg.light = 1
        send(plc, HMImsg.toString())    # Instruct the PLC to enable the lighting for the QR camera
        time.sleep(0.5)                 # Give the PLC time to process
        HMImsg.fromString(receive(plc)) # Collect response and store it

        # Read the serial number (data matrix), retry five times, if needed
        for i in range(5):
            refresh()
            send(qrCamera, "sw8\r\n")       # Trigger a photo
            receive(qrCamera, 0)            # Acknowledge
            time.sleep(0.5)                 # Give the camera time to process the data matrix
            send(qrCamera, "gvb002\r\n")
            sid = receive(qrCamera, 1)      # Get the serial number from the camera

            # If this sid matches the format of "xxxxx xxxx xx" where x are all digits, get the grade
            if re.search("\d{5} \d{4} \d{2}", sid):
                try:
                    grade = excelData[sid]
                    break
                # If the sid is not present in the Excel sheet
                except KeyError:
                    print("Excel sheet does not contain<", sid, ">")
                    # TODO User error. Excel might be out of date. Serial number was not found
                    send(robot, "disconnect")
                    disconnect(robot)
                    disconnect(plc)
                    disconnect(qrCamera)
                    disconnect(invoerCamera)
                    exit(-1)
        
        # If this else clause is executed, it means that the data matrix is not recognized after 5 retries
        else:
            print("Data matrix cannot be recognized")
            pass
            # TODO this clause
        
        refresh()
        HMImsg.grade = grade            # Store this grade in the HMImsg object
        HMImsg.light = 0                # Also, the light can be turned off again
        send(plc, HMImsg.toString())    # Instruct the PLC to enable the lighting for the QR camera
        time.sleep(0.5)                 # Give the PLC time to process
        HMImsg.fromString(receive(plc)) # Collect response and store it

        refresh()
        cell = counter.increment(grade) - 1     # Increment output tray cell counter and store free spot
        send(robot, robotMsg("Q", grade, cell)) # Instruct the robot to place the cell there
        receive(robot)                  # Robot has reached its destination

        refresh()
        HMImsg.air = 0
        send(plc, HMImsg.toString())    # Instruct the PLC to disable the vacuum generator
        time.sleep(0.5)                 # Give the PLC time to process
        HMImsg.fromString(receive(plc)) # Collect response and store it

        refresh()
        send(robot, "neutral")          # Instruct the robot return to its neutral position
        receive(robot)                  # Robot has reached its neutral position

        HMImsg.grade = 100
        send(plc, HMImsg.toString())    # Instruct the PLC to remove the grade value from the HMI
        time.sleep(0.5)                 # Give the PLC time to process
        HMImsg.fromString(receive(plc)) # Collect response and store it

        # If output tray is full, the 12th cell has just been placed in that output tray
        if cell == 12:
            refresh()
            counter.reset(grade)        # The user will physically remove the tray, reset counter to 0
            HMImsg.outputTray = grade
            send(plc, HMImsg.toString())    # Instruct the HMI to execute the tray replacement procedure
            time.sleep(0.5)                 # Give the PLC time to process
            HMImsg.fromString(receive(plc)) # Collect response and store it

            # We will wait for the user to acknowledge output tray removal via the HMI
            refresh() # Will also be called next iteration in this loop, or the one below.

    # If input tray has no cells left, move the tray to the empty tray stack
    # TODO
    refresh() # Loop will also start with refresh!


    counter.inputHeight -= 1

# Program finished

# TODO

######################
# Disconnect devices #
######################

HMImsg.status = 2
send(plc, HMImsg.toString())

send(robot, "disconnect")

disconnect(robot)
disconnect(plc)
disconnect(qrCamera)
disconnect(invoerCamera)
