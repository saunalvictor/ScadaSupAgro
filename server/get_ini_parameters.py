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
    sCurrentPath = os.path.abspath(os.path.dirname(sys.argv[0]))
    os.chdir(sCurrentPath)
    sIniFile = sFile + ".ini"
    sSection="CONFIG"
    import configparser as cp
    cfg = cp.ConfigParser()
    printlog("Reading configuration in {}...".format(sIniFile))
    try:
        with open(sIniFile) as f:
            cfg.read_file(f)
    except IOError:
        printlog("ERROR : Fail to open "+sIniFile)
        sys.exit()
    #initialisation de dPrm : dictionnaire des parametres generaux de la compilation

    dPrm={}
    if not cfg.has_section(sSection):
        printlog("ERROR: Section "+sSection+" not found in "+sIniFile)
        sys.exit()
    for item in cfg.items(sSection):
        dPrm[item[0].strip()]=item[1].strip()
    return dPrm
