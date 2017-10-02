#!/usr/bin/env python3
#-------------------------------------------------------------------------------
## @mainpage
## TES_GetData : Programme python d'acquisition de donnees pour une carte TES
## @author David Dorchies
## @date 28/03/2013
#-------------------------------------------------------------------------------

# Defining logger
import logging
logging.basicConfig(
    format='%(asctime)s %(levelname)s  %(threadName)s %(funcName)s %(message)s', 
    level=logging.DEBUG
)

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
logging.info("Starting server...")
sCurrentPath = os.path.abspath(os.path.dirname(sys.argv[0]))
os.chdir(sCurrentPath)
sIniFile="TES_Server.ini"
sSection="CONFIG"
import configparser as cp
CfgPrm = cp.ConfigParser()
logging.info("Reading configuration in {}...".format(sIniFile))
CfgPrm.read(sIniFile)
#initialisation de dPrm : dictionnaire des parametres generaux de la compilation
dPrm={}
if not CfgPrm.has_section(sSection):
    logging.info("Error: Section "+sSection+" not found in "+sIniFile)
    exit
for item in CfgPrm.items(sSection):
    dPrm[item[0]]=item[1]

#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# Mise en route du serveur d'instruction au TES
import TES_JobScheduler
TES_JS=TES_JobScheduler.TES_JobScheduler(dPrm)
t = TES_JobScheduler.threading.Thread(name='TES_JS', target=TES_JS.Start)
t.start()
#-------------------------------------------------------------------------------
# Mise en route du serveur TCP

HOST, PORT = dPrm['tcp_host'], int(dPrm['tpc_port'])

# Create the server, binding to localhost on port dPrm['tpc_port']
import TCPHandler
server = TCPHandler.socketserver.TCPServer((HOST, PORT), TCPHandler.MyTCPHandler)
logging.info("Listening TCP communication on host {} port {}".format(dPrm['tcp_host'],dPrm['tpc_port']))
# Adding parameters (http://stackoverflow.com/questions/8549177/is-there-a-way-for-baserequesthandler-classes-to-be-statful)
server.TES_JS = TES_JS
# Activate the server; this will keep running until you
# interrupt the program with Ctrl-C
logging.info("Starting server...")
server.serve_forever()

#-------------------------------------------------------------------------------
