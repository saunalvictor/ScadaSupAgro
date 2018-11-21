#!/usr/bin/python3
from http.server import BaseHTTPRequestHandler

class MyServer(BaseHTTPRequestHandler):
    # Wifi device handler as a property of the class
    netHdlr = None

    def do_GET(self):
        self.send_response(200)
        self.wfile.write(bytes(self.netHdlr.get(self.path), "utf-8"))

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
            self.log.error("Token not known: {}".format(token))
            return "ERROR: The network device does not exist in the database. Connect to the SCADA server and type HELP NET for help."
        # Check the number of data declared in the database
        if len(lV) != device.n:
            self.log.error("Number of data provided ({}) does not match with the device one ({})".format(len(lV),device.n))
            return "ERROR: The number of data to record ({:d}) does not match with the number of data declared in the database {:d}. Connect to the SCADA server and type HELP NET for help.".format(len(lV), device.n)
        # Record the data in the appropriate file
        return self.record(device.id, lV)

    def record(self, sDevice, lData):
        filename=self.dPrm['NET_DATA_LOGGER']['file'].format(sDevice)
        self.log.debug("Start record to {}".format(filename))
        try:
            f = open(filename, 'a')
        except IOError as e:
            self.log.error("Recording {}: ".format(filename)+str(e))
            return 'ERROR during recording: '+ str(e)
        else:
            with f:
                try:
                    from datetime import datetime
                    sDateTime = datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f")[:-3]
                    f.writelines(sDateTime+";"+";".join(lData)+"\n")
                except Exception as e:
                    self.log.error("Writing in {}: ".format(filename)+str(e))
                    return 'ERROR during writing: '+ str(e)
        sOut='{:d} data recorded for device {} with timestamp: {}'.format(len(lData), sDevice, sDateTime)
        self.log.debug(sOut)
        return sOut




def scadaNetDataLogger(dPrm):
    from scada_misc import createLog
    log = createLog(dPrm['LOGGER']['level'])
    log.info("Starting scada wifi data logger...")

    hostName = ""
    try:
        hostPort = int(dPrm['NET_DATA_LOGGER']['tcp_port'])
    except Exception as e:
        log.critical('Parameter [NET_DATA_LOGGER]/tcp_port in scada.ini: '+e)

    MyServer.netHdlr = NetDeviceHandler(dPrm, log)

    from http.server import HTTPServer
    myServer = HTTPServer((hostName, hostPort), MyServer)

    log.info("Server Starts - %s:%s" % (hostName, hostPort))

    try:
        myServer.serve_forever()
    except KeyboardInterrupt:
        pass

    myServer.server_close()
    log.info("Server Stops - %s:%s" % (hostName, hostPort))


if __name__ == '__main__':
    from scada_misc import getIniParameters
    dPrm = getIniParameters("scada.ini")
    scadaNetDataLogger(dPrm)
