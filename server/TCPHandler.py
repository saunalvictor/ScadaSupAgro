# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 18:40:00 2016

@author: david.dorchies
"""

import socketserver

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        import logging
        import socket
        bConnected = True
        logging.info("{} connected".format(self.client_address[0]))
        while bConnected:        
            sRecv = ""
            while sRecv == "":            
                # self.request is the TCP socket connected to the client
                try:
                    self.data = self.request.recv(1024)
                except socket.error as e:
                    # The TCP connection is broken
                    logging.error("request.recv: {}, {}".format(e.errno, e.strerror))
                    self.data = False
                if not self.data:
                    # Receiving empty string : the TCP connection is closed
                    bConnected = False                    
                    break
                self.data = self.data.strip()
                sRecv = str(self.data, "utf-8")
            if not bConnected:
                break
            logging.info("{} wrote: {}".format(self.client_address[0],sRecv))
            if sRecv == "CLOSE":
                # Order for explicitely closing the connection by the server
                break
            sReturn = self.server.TES_JS.RunNow(sRecv)
            logging.info("Sending for {} : {}".format(self.client_address[0],sReturn))
            try:
                self.request.sendall(bytes(sReturn, "utf-8"))
            except socket.error as e:
                logging.error("request.sendall: {}, {}".format(e.errno, e.strerror))
                break
            logging.debug("Instruction End")
        logging.info("Connection ended")