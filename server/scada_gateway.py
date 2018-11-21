
def scadaGateway(dPrm):
    import json
    import requests

    dPrmG = dPrm['GATEWAY']

    from scada_misc import createLog
    log = createLog(dPrm['LOGGER']['level'])
    log.info('Starting Scada Gateway')

    from scada_database import ScadaDatabase
    scadaDB = ScadaDatabase(log, dPrm)

    # Variable list corresponds to all variables handled by the database
    lVars = list(scadaDB.vars.keys())

    def send_to_plateform(dLastDateTime, sc):
        dTelemetry = {}
        for key in lVars:
            timestamp = dLastDateTime[key]
            try:
                data = scadaDB.get(key)
                timestamp = scadaDB.getTimeStamp(key)
            except Exception as e:
                log.error('Impossible to get variable {}: {}'.format(key,str(e)))
            except Exception as e:
                log.error('Retriving TimeStamp: '+str(e))
            if timestamp != dLastDateTime[key]:
                dLastDateTime[key] = timestamp
                dTelemetry[key] = data
        s.enter(float(dPrmG['frequency']), 1, send_to_plateform, (dLastDateTime, sc,))
        if len(dTelemetry)>0:
            log.info("Sending "+json.dumps(dTelemetry)+"...")
            try:
                r = requests.post(dPrmG['url'], json=dTelemetry)
                log.debug("Request response: " + r.text)
            except requests.exceptions.RequestException as e:
                log.error("Request post error: " + str(e))

    # Scheduling
    import time
    import sched
    s = sched.scheduler(time.time, time.sleep)
    s.enter(float(dPrmG['frequency']), 1, send_to_plateform, ({key:"" for key in lVars}, s,))
    s.run()


if __name__ == '__main__':
    from scada_misc import getIniParameters
    dPrm = getIniParameters("scada.ini")
    scadaGateway(dPrm)
