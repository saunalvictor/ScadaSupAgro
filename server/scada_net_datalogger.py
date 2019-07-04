#!/usr/bin/python3
from http.server import BaseHTTPRequestHandler

class NetDeviceHandler:
    def __init__(self, dPrm, log):
        self.dPrm = dPrm
        self.log = log
        from scada_database import ScadaDatabase
        self.scadaDB = ScadaDatabase(log, dPrm)


    def get(self, path):
        self.log.debug('GET request: '+path)
        # Parse the path
        lV = path.split('/')
        del lV[0] # Remove empty item before first /
        token = lV[0]
        del lV[0]
        # Check if the device exists in the database
        device = self.scadaDB.getDeviceFromToken(token)
        if not device:
            # Reload database in case of new device
            from scada_database import ScadaDatabase
            self.scadaDB = ScadaDatabase(self.log, self.dPrm)
            device = self.scadaDB.getDeviceFromToken(token)
            if not device: 
                self.log.error("Token not known: {}".format(token))
                return "404|ERROR: Token not known.\r\nConnect to the SCADA server and type HELP NET for help."
        # Check the number of data declared in the database
        if len(lV) != device.n:
            self.log.error("Number of data provided ({}) does not match with the device one ({})".format(len(lV),device.n))
            return "404|ERROR: The number of data to record ({:d}) does not match with the number of data declared in the database {:d}.\nConnect to the SCADA server and type HELP NET for help.".format(len(lV), device.n)
        # Record the data in the appropriate file
        return self.record(device.id, lV)
        

    def record(self, sDevice, lData):
        filename=self.dPrm['NET_DATA_LOGGER']['file'].format(sDevice)
        self.log.debug("Start record to {}".format(filename))
        try:
            f = open(filename, 'a')
        except IOError as e:
            self.log.error("Recording {}: ".format(filename)+str(e))
            return '500|ERROR during recording: '+ str(e)
        else:
            with f:
                try:
                    from datetime import datetime
                    sDateTime = datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f")[:-3]
                    f.writelines(sDateTime+";"+";".join(lData)+"\n")
                except Exception as e:
                    self.log.error("Writing in {}: ".format(filename)+str(e))
                    return '500|ERROR during writing: '+ str(e)
        sOut='{:d} data recorded for device {} with timestamp: {}'.format(len(lData), sDevice, sDateTime)
        self.log.debug(sOut)
        return "200|" + sOut

    def serve(self):
        netHdlr = self
        class MyServer(BaseHTTPRequestHandler):
            
            def do_GET(self):
                r = netHdlr.get(self.path).split("|")
                self.send_response(int(r[0]))
                self.send_header('Content-Type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write(bytes(r[1], "utf-8"))
        
        self.log.info("Starting scada wifi data logger...")
        hostName = ""
        try:
            hostPort = int(self.dPrm['NET_DATA_LOGGER']['tcp_port'])
        except Exception as e:
            log.critical('Parameter [NET_DATA_LOGGER]/tcp_port in scada.ini: '+e)

        from http.server import HTTPServer
        myServer = HTTPServer((hostName, hostPort), MyServer)

        self.log.info("Server Starts - %s:%s" % (hostName, hostPort))

        try:
            myServer.serve_forever()
        except KeyboardInterrupt:
            pass

        myServer.server_close()
        self.log.info("Server Stops - %s:%s" % (hostName, hostPort))


def scadaNetDataLogger(dPrm):
    from scada_misc import createLog
    netHdlr = NetDeviceHandler(dPrm, createLog(dPrm['NET_DATA_LOGGER']['log_level']))
    netHdlr.serve()


if __name__ == '__main__':
    from scada_misc import getIniParameters
    scadaNetDataLogger(getIniParameters("scada.ini"))
