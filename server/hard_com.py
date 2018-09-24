from printlog import printlog

class HardCom:
    def __init__(self, bTest = False):
        self.bTest = bTest
        self.bConnected = True
        if not bTest:
            import serial
            printlog("Connecting to hardware...")
            try:
                self.ser = serial.Serial('/dev/ttyACM0',9600)
            except:
                printlog("ERROR: No connection to hardware")
                printlog("Check connections and retry")
                self.bconnected = False
                pass
        else:
            printlog("Testing without connection to hardware")

    def get(self, s):
        sOut = ""
        if not self.bTest:
            try:
                self.ser.write(b'1')
                sOut = self.ser.readline().decode("ISO-8859-1")
            except IOError as e:
                printlog("Error: get({}): {}, {}".format(s, e.errno, e.strerror))
                sOut = "ERROR: reading serial data"
        else:
            from random import random
            sOut = " ".join(map(str,[int(random()*2) for x in range(0,len(s.split(",")))]))
        return sOut
