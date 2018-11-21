# -*- coding: utf-8 -*-

# Script pour récupérer les données temps réel des niveaux d'eau du Mekong et les injecter dans la plateforme IoT ThingsBoard hébergée sur le serveur Aubes d'Irstea Montpellier
# Le script doit être lancé par un cron toutes les 15 minutes à l'aide la configuration suivante
# */15 * * * * python3 /home/aubes/mekong/thingsboard_gateway.py >> /var/log/thingsboard_gateway.log 2>&1

# Parameters
dPrm = {
    'url': "https://api.mrcmekong.org/static/station-forum-status.xml",
    'thingsboard': {
        'url': 'http://10.34.192.92:8082/api/v1/A1_TEST_TOKEN/telemetry',
    }
}

from datetime import datetime
import sys

def printlog(s, sep = ": "):
    """
    Print message with date and time and flush the console
    @see https://www.turnkeylinux.org/blog/unix-buffering
    """
    sDateTime = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    print(sDateTime + sep + s)

    sys.stdout.flush()


import urllib.request
import requests
from lxml import etree

opener = urllib.request.build_opener()

printlog("Open " + dPrm['url'])
tree = etree.parse(opener.open(dPrm['url']))
keys = []
for station in tree.xpath("/stations/station/name"):
    keys.append(station.text)
dJSON = {}
i = 0
for station in tree.xpath("/stations/station/waterLevel"):
    try:
        dJSON[keys[i]] = float(station.text.replace(" m",""))
    except ValueError:
        pass
    i += 1
printlog("Post to " + dPrm['thingsboard']['url'])
printlog("data:"+str(dJSON))
try:
    r = requests.post(dPrm['thingsboard']['url'], json=dJSON)
    printlog("Reponse: " + r.text)
except Exception as e: 
    printlog("ERROR: "+str(e))
