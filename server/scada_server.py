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

from scada_misc import getIniParameters
dPrm = getIniParameters("scada.ini")
dPrmS = dPrm['SERVER']

#-------------------------------------------------------------------------------
# Mise en route du serveur TCP
HOST, PORT = dPrmS['tcp_host'], int(dPrmS['tpc_port'])

# Create the server, binding to localhost on port dPrm['tpc_port']
import socketserver
from scada_server_handler import ScadaTCPRequestHandler
server = socketserver.TCPServer((HOST, PORT), ScadaTCPRequestHandler)
# Activate the server; this will keep running until you
# interrupt the program with Ctrl-C
server.serve_forever()

# Multi users
# import threading
# with socketserver.ThreadingTCPServer((HOST, PORT), ScadaTCPRequestHandler) as server:
#     # Start a thread with the server -- that thread will then start one
#     # more thread for each request
#     server_thread = threading.Thread(target=server.serve_forever)
#     server_thread.start()

# while True:
#     pass
#-------------------------------------------------------------------------------
