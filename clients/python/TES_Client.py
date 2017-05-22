#!/usr/bin/env python3
#-------------------------------------------------------------------------------
## @mainpage
## TES_GetData : Programme python d'acquisition de donnees pour une carte TES
## @author David Dorchies
## @date 28/03/2013
#-------------------------------------------------------------------------------
import logging
logging.basicConfig(
    format='%(asctime)s %(levelname)s  %(threadName)s %(funcName)s %(message)s', 
    level=logging.DEBUG
)

def getConnection():
    # Create a socket (SOCK_STREAM means a TCP socket)
    import socket
    logging.info("Connecting to host "+dPrm['host']+":"+dPrm['port']+"...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((dPrm['host'], int(dPrm['port'])))
    logging.info("Connection established to host "+dPrm['host']+":"+dPrm['port'])
    return sock    


#-------------------------------------------------------------------------------
## Function to be loop with a timer for acquisition and writing
def getData(sock):
    global dPrm,csvOut
    import os.path
    if os.path.exists("stop.txt"):
        logging.info("stop.txt file found : stop acquisition")
        sock.sendall(bytes("CLOSE\n", "utf-8"))
        sock.close()
        return False # Indicate to stop acquisition
    #Data acquisition
    sInstr = "GET " + dPrm["reg"]
    logging.info("Send instruction : "+sInstr)
    sock.sendall(bytes(sInstr + "\n", "utf-8"))
    # Receive data from the server and shut down
    received = str(sock.recv(1024), "utf-8")
    logging.info("Received : "+received)
    import datetime
    now = datetime.datetime.now()
    lD=[now.strftime("%Y-%m-%d %H:%M:%S.%f")]
    lD+=received.split(" ")
    csvOut.writerow(lD)
    return True # Indicate to continue for next acquisition


#-------------------------------------------------------------------------------
# Reading of the parameters in TES_GetData.ini
## @section parameters Parameters in TES_GetData.ini
## The TES_GetData.ini must have a [CONFIG] section with following parameters:
## - port: communication port for modbus (com1 or com2)
## - path: output path (if not defined it's written in the same folder as this program)
## - reg: registries to read separated by comma (ex:3,4,5,6 for 0,1,2,3 analogic entries in TES)
## - ts: time step in seconds between each data acquisition
## - test: test=1 for testing the program without communication
import os,sys
sCurrentPath = os.path.abspath(os.path.dirname(sys.argv[0]))
os.chdir(sCurrentPath)
sIniFile="TES_Client.ini"
sSection="CONFIG"
import configparser as cp
CfgPrm = cp.ConfigParser()
CfgPrm.read(sIniFile)
#initialisation de dPrm : dictionnaire des parametres generaux de la compilation
dPrm={}
if not CfgPrm.has_section(sSection):
    logging.info("Erreur: Section "+sSection+" not found in "+sIniFile)
    exit
for item in CfgPrm.items(sSection):
    dPrm[item[0]]=item[1]



# Opening the output file
import csv
import datetime
now = datetime.datetime.now()
sFileOut=  "TES_"+now.strftime("%Y%m%d-%H%M%S")+".txt"
if "path" in dPrm and dPrm("path")!="":
    os.chdir(dPrm("path"))

fCsv = open(sFileOut,"w")
csvOut = csv.writer(fCsv, delimiter='\t',escapechar='\\',quoting=csv.QUOTE_NONE,lineterminator='\n')

sock = getConnection()

bLoop = True
import time
while bLoop:
    start_time = time.time()
    bLoop = getData(sock)
    time_sleep = float(dPrm["ts"]) - (time.time() - start_time)
    #logging.info(time_sleep)
    if time_sleep > 0:
        time.sleep(time_sleep)

# Fermeture du fichier de chronique
fCsv.close()