#!/usr/bin/env python3
#-------------------------------------------------------------------------------
## @mainpage
## TES_GetData : Programme python d'acquisition de donnees pour une carte TES
## @author David Dorchies
## @date 28/03/2013
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Programme principal
#-------------------------------------------------------------------------------

from get_ini_parameters import getIniParameters
dPrm = getIniParameters("scada_server")

#-------------------------------------------------------------------------------
# Mise en route du serveur TCP
HOST, PORT = dPrm['tcp_host'], int(dPrm['tpc_port'])

# Create the server, binding to localhost on port dPrm['tpc_port']
from printlog import printlog
printlog("Listening TCP communication on host {} port {}".format(HOST, PORT))
import socketserver
from my_tcp_handler import MyTCPHandler
server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

# Activate the server; this will keep running until you
# interrupt the program with Ctrl-C
printlog("Starting server...")
server.serve_forever()

#-------------------------------------------------------------------------------
