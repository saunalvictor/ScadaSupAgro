import socketserver

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        from get_ini_parameters import getIniParameters
        dPrm = getIniParameters("scada_server")

        import socket

        from printlog import printlog
        from hard_com import HardCom
        hardcom = HardCom(dPrm["test"]=="1")
        bConnected = hardcom.bConnected
        while bConnected:
            sRecv = ""
            while sRecv == "":
                # self.request is the TCP socket connected to the client
                self.data = self.request.recv(1024)
                if not self.data:
                    bConnected = False
                    break
                self.data = self.data.strip()
                sRecv = str(self.data, "ISO-8859-1")
            if not bConnected:
                break
            printlog("{} wrote: {}".format(self.client_address[0],sRecv))
            # Parse instructions separated by spaces
            lRecv = sRecv.split(" ")
            sInstruction = lRecv[0].upper()

            if sInstruction == "GET":
                if len(lRecv) > 1:
                    sSend = hardcom.get(lRecv[1])
                else:
                    sSend = "ERROR: Instruction GET needs parameters"

            elif sInstruction == "SET":
                # Output to apply defined by the number of the output and a time in seconds
                lPrm = lRecv[1].split(",")
                if not "test" in dPrm or dPrm["test"]!="1":
                    printlog("SET: {}, {}".format(lPrm[0], lPrm[1]))
                sSend = "Instruction SET applied"
            elif sInstruction == "CLOSE":
                bConnected = False
                sSend = "Connection closed"
            else:
                sSend = "ERROR: Instruction {} not handled by the server".format(lRecv[0])
            sSend = sSend + "\n"
            try:
                self.request.sendall(sSend.encode("ISO-8859-1"))
                printlog("Data sent : "+sSend)
            except socket.error as e:
                printlog("Error: {}, {}".format(e.errno, e.strerror))
                break
        printlog("Connection ended")