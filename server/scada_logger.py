# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 19:25:49 2018

@author: dorch
"""

class ScadaLogger():
    def __init__(self,dPrm):

        from scada_misc import createLog
        self.log = createLog(dPrm['LOGGER']['level'])
        self.log.info("Starting scada logger...")

        from scada_logger_arduino import ArduinoCommunication
        self.hardcom = ArduinoCommunication(self.log, dPrm["HARDWARE"])

        # création de l'objet logger qui va nous servir à écrire les données dans les logs
        self.dataLog = createLog("DEBUG", sFormat='%(asctime)s;%(message)s', sFileName=dPrm['DATA_LOGGER']['file'], sLoggerName="data_logger")

        # Set the pin list
        self.dPrmDL = dPrm['DATA_LOGGER']
        try:
            import re
            self.lPins = [int(s) for s in filter(None, re.split("[,;\t ]+",self.dPrmDL['pins']))]
        except Exception as e:
            self.log.critical("Wrong parameter DATA_LOGGER/pins in scada.ini: " + str(e))
            raise SystemExit(1)

        # Set the minimum value
        try:
            self.rValueMin = float(self.dPrmDL['valuemin'])
        except Exception as e:
            self.log.critical("Wrong parameter DATA_LOGGER/valuemin in scada.ini: " + str(e))
            raise SystemExit(1)

        # Scheduled measurement
        import sched, time
        self.s = sched.scheduler(time.time, time.sleep)

    def do_measurement(self):
        lData = self.hardcom.get(self.lPins)
        bOK = False
        try:
            for sItem in lData:
                if float(sItem) > self.rValueMin:
                    bOK = True
                    break
        except Exception as e:
            self.log.error(str(e))
        if bOK: self.dataLog.info(";".join(lData))

    def loop_measurement(self):
        self.nb_loop -= 1
        if self.nb_loop == -1: return
        self.setloop(float(self.dPrmDL['freq']))
        self.do_measurement()

    def setloop(self, delay):
        self.s.enter(delay, 1, self.loop_measurement)

    def run(self, nb_loop=-1):
        self.nb_loop = nb_loop
        self.setloop(float(self.dPrmDL['freq']))
        self.s.run()


if __name__ == '__main__':
    from scada_misc import getIniParameters
    dPrm = getIniParameters("scada.ini")
    sl = ScadaLogger(dPrm)
    sl.run()
