# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 19:25:49 2018

@author: dorch
"""
from printlog import printlog
printlog("Starting scada aggregator...")

import sched, time
s = sched.scheduler(time.time, time.sleep)

from get_ini_parameters import getIniParameters
dPrm = getIniParameters("scada_logger")

from hard_com import HardCom
hardcom = HardCom(dPrm["test"]=="1")

def do_measurement(dPrm, hardcom, last_data, sc):
    sData = hardcom.get("1,2,3,4").replace(" ", ";").strip()
    s.enter(0.5, 1, do_measurement, (dPrm, hardcom, sData, sc,))
    lData = sData.split(";")
    try:
        if any(float(sItem) > float(dPrm['valuemin']) for sItem in lData):
            printlog(sData, True, ";")
    except:
        pass

last_data = ""
s.enter(0.5, 1, do_measurement, (dPrm, hardcom, last_data, s,))
s.run()
