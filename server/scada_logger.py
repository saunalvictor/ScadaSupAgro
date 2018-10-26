# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 19:25:49 2018

@author: dorch
"""

def scadaLogger(dPrm):

    from scada_misc import createLog
    log = createLog(dPrm['LOGGER']['level'])
    log.info("Starting scada aggregator...")

    from hard_com import HardCom
    hardcom = HardCom(log, dPrm["HARDWARE"])

    # création de l'objet logger qui va nous servir à écrire les données dans les logs
    dataLog = createLog("DEBUG", sFormat='%(asctime)s;%(message)s', sFileName=dPrm['DATA_LOGGER']['file'], sLoggerName="data_logger")

    # Set the pin list
    dPrmDL = dPrm['DATA_LOGGER']
    try:
        import re
        lPins = [int(s) for s in filter(None, re.split("[,;\t ]+",dPrmDL['pins']))]
    except Exception as e:
        log.critical("Wrong parameter DATA_LOGGER/pins in scada.ini: " + str(e))
        raise SystemExit(1)

    # Set the minimum value
    try:
        rValueMin = float(dPrmDL['valuemin'])
    except Exception as e:
        log.critical("Wrong parameter DATA_LOGGER/valuemin in scada.ini: " + str(e))
        raise SystemExit(1)

    # Scheduled measurement
    import sched, time
    s = sched.scheduler(time.time, time.sleep)

    def do_measurement(sc):
        lData = hardcom.get(lPins)
        s.enter(float(dPrmDL['freq']), 1, do_measurement, (sc,))
        bOK = False
        try:
            for sItem in lData: 
                if float(sItem) > rValueMin:
                    bOK = True
                    break
        except Exception as e:
            log.error(str(e))
        if bOK: dataLog.info(";".join(lData))

    s.enter(float(dPrmDL['freq']), 1, do_measurement, (s,))
    s.run()


if __name__ == '__main__':
    from scada_misc import getIniParameters
    dPrm = getIniParameters("scada.ini")
    scadaLogger(dPrm)
