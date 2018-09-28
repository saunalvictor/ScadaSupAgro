from get_ini_parameters import getIniParameters
dPrm = getIniParameters("scada_gateway")


from read_data import ReadData
from printlog import printlog
import requests
import json

rd = ReadData(dPrm)

import sched, time
s = sched.scheduler(time.time, time.sleep)

def send_to_plateform(dPrm, rd, sLastDateTime, sc):
    sData = rd.last_line(ignore_ending_newline=True).decode('utf-8')
    lData = sData.split(";")
    s.enter(float(dPrm['frequency']), 1, send_to_plateform, (dPrm, rd, lData[0], sc,))
    if lData[0] != sLastDateTime:
        lData.pop(0)
        dTelemetry = {}
        for idx, val in enumerate(lData):
            try:
                dTelemetry["rpi_"+str(idx)] = float(val)
            except ValueError:
                pass
        printlog("Sending "+json.dumps(dTelemetry)+"...")
        try:
            r = requests.post(dPrm['url'], json = dTelemetry)
        except requests.exceptions.RequestException as e:
            printlog("Request post error: " + str(e))

# MAIN PROGRAM
s.enter(float(dPrm['frequency']), 1, send_to_plateform, (dPrm, rd, "", s,))
s.run()
