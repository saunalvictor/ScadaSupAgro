class ArduinoCommunication:
    def __init__(self, log, dPrmHard):
        self.log = log
        self.dPrm = dPrmHard
        self.bTest = dPrmHard['test']=='1'
        self.bConnected = True
        if not self.bTest:
            import serial
            log.info("Connecting to hardware...")
            try:
                self.ser = serial.Serial(dPrmHard['port'], dPrmHard['baudrate'])
            except:
                log.error("No connection to hardware: check connections and retry")
                self.bconnected = False
                pass
        else:
            log.info("Testing without connection to hardware")

    def get(self, lPins):
        """
        Return data from hardware
        @param list of the pins to get
        @return ordered list of data for each asked pin or string if error
        """
        self.log.debug(lPins)
        # Getting the string from the arduino given all the available data separated by spaces
        if not self.bTest:
            try:
                self.ser.write(b'1')
                sArduino = self.ser.readline().decode("ISO-8859-1")
                self.log.debug('Arduino sent: '+sArduino)
            except IOError as e:
                self.log.error("HardCom.get Arduino readline: {}, {}".format(e.errno, e.strerror))
                return "ERROR: reading serial data"
        else:
            from random import random
            sArduino = " ".join(map(str,[int(random()*int(self.dPrm['test_maxval'])) for x in range(int(self.dPrm['nb_pins']))]))
        # Convert to list
        lAllData = sArduino.split()
        # Select pins
        try:
            self.log.debug(lAllData)
            lData = [lAllData[i] for i in lPins]
        except Exception as e:
            sErr = "HardCom.get data selection: {}".format(e)
            self.log.error(sErr)
            return "ERROR: " + sErr
        return lData
