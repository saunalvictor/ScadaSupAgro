
class ScadaGateway():
    def __init__(self, dPrm):
        self.dPrm = dPrm
        self.dPrmG = dPrm['GATEWAY']

        from scada_misc import createLog
        self.log = createLog(dPrm['LOGGER']['level'])
        self.log.info('Starting Scada Gateway')

        # Scheduled measurement
        import sched, time
        self.s = sched.scheduler(time.time, time.sleep)
        try:
            self.frequency = float(self.dPrmG['frequency'])
        except Exception as e:
            self.log.error('scada.ini: Parameter [GATEWAY] frequency: '+ str(e))
            raise SystemExit(1)

    def update_vars(self):
        from scada_database import ScadaDatabase
        self.scadaDB = ScadaDatabase(self.log, self.dPrm)

        # Variable list corresponds to all variables handled by the database
        self.lVars = list(self.scadaDB.vars.keys())

        # Remaining number of send before next update of variable list from database
        try:
            self.next_update = int(self.dPrmG['update_var'])
        except Exception as e:
            self.log.error('scada.ini: Parameter [GATEWAY] update_var: '+ str(e))
            raise SystemExit(1)
        return self.lVars

    def do_send(self):
        self.dTelemetry = {}
        for key in self.lVars:
            timestamp = self.dLastDateTime[key]
            try:
                data = self.scadaDB.get(key)
                timestamp = self.scadaDB.getTimeStamp(key)
                self.log.debug('key={} timestamp={} value={}'.format(key,timestamp,data))
            except Exception as e:
                self.log.debug('Impossible to get variable {}: {}'.format(key,str(e)))
            if timestamp != self.dLastDateTime[key]:
                self.dLastDateTime[key] = timestamp
                self.dTelemetry[key] = data

        if len(self.dTelemetry)>0:
            import json
            self.log.info("Sending: "+json.dumps(self.dTelemetry))
            import requests
            try:
                r = requests.post(self.dPrmG['url'], json=self.dTelemetry)
                self.log.debug("Request response: " + r.text)
            except requests.exceptions.RequestException as e:
                self.log.warning("Request post error: " + str(e))
        return self.dTelemetry

    def loop_send(self):
        self.setloop(self.frequency)
        # Control next update of variable list
        self.next_update -= 1
        if self.next_update == 0: self.update_vars()
        # Sending
        self.do_send()

    def setloop(self, delay):
        self.s.enter(delay, 1, self.loop_send)

    def run(self):
        self.update_vars()
        self.setloop(self.frequency)
        self.dLastDateTime = {key:"" for key in self.lVars}
        self.s.run()

if __name__ == '__main__':
    from scada_misc import getIniParameters
    dPrm = getIniParameters("scada.ini")
    scadaGateway = ScadaGateway(dPrm)
    scadaGateway.run()
