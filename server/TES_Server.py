#!/usr/bin/env python3
#-------------------------------------------------------------------------------
## @mainpage
## TES_GetData : Programme python d'acquisition de donnees pour une carte TES
## @author David Dorchies
## @date 28/03/2013
#-------------------------------------------------------------------------------


import socketserver

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        sRecv = str(self.data, "utf-8")
        print("{} wrote: {}".format(self.client_address[0],sRecv))
        # Parse instructions separated by spaces
        lRecv = sRecv.split(" ")
        if "test" in dPrm and dPrm["test"]=="1":
            import random
            import time

        if lRecv[0].upper() == "GET":
            # Creating a list from the registries number to acquire
            lReg = lRecv[1].split(",")
            lD = []
            for Reg in lReg:
                if not "test" in dPrm or dPrm["test"]!="1":
                    D=instr.read_register(int(Reg), 0)
                else:
                    time.sleep(0.1)
                    D=random.random()*255
                lD.append(D)
            sD = " ".join(map(str,lD))
            self.request.sendall(bytes(sD, "utf-8"))
            print("Data sent : "+sD)
        elif lRecv[0].upper() == "SET":
             # Output to apply defined by the number of the output and a time in seconds
             lPrm = lRecv[1].split(",")
             if not "test" in dPrm or dPrm["test"]!="1":
                instr.write_register(int(19), int(lPrm[0]))




#-------------------------------------------------------------------------------
# Programme principal
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# Reading of the parameters in TES_GetData.ini
## @section parameters Parameters in TES_GetData.ini
## The TES_Server.ini must have a [CONFIG] section with following parameters:
## - port: communication port for modbus (com1 or com2)
## - path: output path (if not defined it's written in the same folder as this program)
## - reg: registries to read separated by comma (ex:3,4,5,6 for 0,1,2,3 analogic entries in TES)
## - ts: time step in seconds between each data acquisition
## - test: test=1 for testing the program without communication
import os,sys
sCurrentPath = os.path.abspath(os.path.dirname(sys.argv[0]))
os.chdir(sCurrentPath)
sIniFile="TES_Server.ini"
sSection="CONFIG"
import configparser as cp
CfgPrm = cp.ConfigParser()
CfgPrm.read(sIniFile)
#initialisation de dPrm : dictionnaire des parametres generaux de la compilation
dPrm={}
if not CfgPrm.has_section(sSection):
    print("Erreur: Section "+sSection+" not found in "+sIniFile)
    exit
for item in CfgPrm.items(sSection):
    dPrm[item[0]]=item[1]

#-------------------------------------------------------------------------------
# Initialisation of Modbus communication
if not "test" in dPrm or dPrm["test"]!="1":
    import minimalmodbus
    print("Connecting to modbus hardware")
    minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL = True
    minimalmodbus.BAUDRATE = 9600
    minimalmodbus.PARITY = 'E'
    minimalmodbus.BYTESIZE = 8
    minimalmodbus.STOPBITS = 1
    #print minimalmodbus._getDiagnosticString()
    instr = minimalmodbus.Instrument('/'+dPrm['serial_port'], 1)
else:
    print("Testing without connection to modbus hardware")
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# Mise en route du serveur TCP

HOST, PORT = dPrm['tcp_host'], int(dPrm['tpc_port'])

# Create the server, binding to localhost on port dPrm['tpc_port']
server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

print("Listening TCP communication on host "+dPrm['tcp_host']+" port "+dPrm['tpc_port'])

# Activate the server; this will keep running until you
# interrupt the program with Ctrl-C
server.serve_forever()

#-------------------------------------------------------------------------------