class HMImessage:
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

    def print(self):
        print(self.air, self.light, self.excel, self.grade, self.outputTray, self.trays,
            self.halt, self.done, self.connRobot, self.connQRcam, self.connINcam)

msg = "\x02\x03\x02\x03\x02\x03\x04\x03\x02\x03\x02"
h = HMImessage()

print(type(h.air))
h.print()
h.decode(h.encode())
print(type(h.air))
h.print()
h.decode(msg)
print(type(h.air))
h.print()

msg = "\x01\x01\x00\x64\x64\x00\x03\x04\x05\x06\x07"
h.decode(msg)
print(type(h.air))
h.print()
