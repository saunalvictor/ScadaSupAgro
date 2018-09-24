def getIniParameters(sFile):
    """
    Read parameters in scada_server.ini
    The ini file must have a [CONFIG] section with the following parameters:
    - port: communication port for modbus (com1 or com2)
    - path: output path (if not defined it's written in the same folder as this program)
    - reg: registries to read separated by comma (ex:3,4,5,6 for 0,1,2,3 analogic entries in TES)
    - ts: time step in seconds between each data acquisition
    - test: test=1 for testing the program without communication
    """
    import os,sys
    from printlog import printlog
    printlog("Starting server...")
    sCurrentPath = os.path.abspath(os.path.dirname(sys.argv[0]))
    os.chdir(sCurrentPath)
    sIniFile = sFile + ".ini"
    sSection="CONFIG"
    import configparser as cp
    CfgPrm = cp.ConfigParser()
    printlog("Reading configuration in {}...".format(sIniFile))
    CfgPrm.read(sIniFile)
    #initialisation de dPrm : dictionnaire des parametres generaux de la compilation
    dPrm={}
    if not CfgPrm.has_section(sSection):
        printlog("Error: Section "+sSection+" not found in "+sIniFile)
        exit
    for item in CfgPrm.items(sSection):
        dPrm[item[0].strip()]=item[1].strip()
    return dPrm
