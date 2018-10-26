
def scadaGateway(dPrm):
    import json
    import requests

    dPrmG = dPrm['GATEWAY']

    from scada_misc import createLog
    log = createLog(dPrm['LOGGER']['level'])
    log.info('Starting Scada Gateway')

    from scada_var import ScadaDatabase
    scadaDB = ScadaDatabase(log, dPrm['DATA_LOGGER'])

    # Variable list corresponds to all variables handled by the database
    lVars = list(scadaDB.vars.keys())

    def send_to_plateform(sLastDateTime, sc):
        try:
            sData = scadaDB.getValues(lVars)
        except Exception as e:
            log.critical('Wrong parameter (scada.ini->[GATEWAY]/variables) : the variable %s doesn\'t exist' % e)
            raise SystemExit(1)
        lData = sData.split(";")
        s.enter(float(dPrmG['frequency']), 1,
                send_to_plateform, (lData[0], sc,))
        if lData[0] != sLastDateTime:
            lData.pop(0)
            dTelemetry = {}
            for idx, val in enumerate(lData):
                try:
                    dTelemetry[lVars[idx]] = float(val)
                except ValueError:
                    pass
            log.debug("Sending "+json.dumps(dTelemetry)+"...")
            try:
                r = requests.post(dPrmG['url'], json=dTelemetry)
                log.debug("Request response: " + r.text)
            except requests.exceptions.RequestException as e:
                log.error("Request post error: " + str(e))

    # Scheduling
    import time
    import sched
    s = sched.scheduler(time.time, time.sleep)
    s.enter(float(dPrmG['frequency']), 1, send_to_plateform, ("", s,))
    s.run()


if __name__ == '__main__':
    from scada_misc import getIniParameters
    dPrm = getIniParameters("scada.ini")
    scadaGateway(dPrm)
