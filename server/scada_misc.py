def getIniParameters(sFile):
    """
    Read parameters in ini file
    @param sFile Paht to the ini file to read
    @return Dictionary with sections and parameters contained in the INI file
    """
    import os,sys
    sCurrentPath = os.path.abspath(os.path.dirname(sys.argv[0]))
    os.chdir(sCurrentPath)
    sIniFile = sFile
    import configparser as cp
    cfg = cp.ConfigParser()

    with open(sIniFile) as f:
        cfg.read_file(f)

    # https://stackoverflow.com/a/28990982
    return {s:dict(cfg.items(s)) for s in cfg.sections()}


def createLog(sLogLevel, sFormat = "", sFileName = "", sLoggerName = __name__):
    """
    Create a log object
    http://sametmax.com/ecrire-des-logs-en-python/
    """
    import logging
    # création de l'objet logger qui va nous servir à écrire dans les logs
    log = logging.getLogger(sLoggerName)

    # Check if this logger has already been configured
    if log.hasHandlers(): log.handlers = []

    # on met le niveau du logger à DEBUG, comme ça il écrit tout
    logLevel = logging.getLevelName(sLogLevel.upper())
    log.setLevel(logLevel)

    # création d'un formateur qui va ajouter le temps, le niveau
    # de chaque message quand on écrira un message dans le log
    if sFormat == "":
        if sLogLevel.upper() == 'DEBUG':
            sFormat = '%(asctime)s :: %(levelname)s :: %(filename)s:%(lineno)s - %(funcName)s() :: %(message)s'
        else:
            sFormat = '%(asctime)s :: %(levelname)s :: %(message)s'
    formatter = logging.Formatter(sFormat)

    # création d'un handler qui va rediriger chaque écriture de log
    # sur la console
    if sFileName == "":
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(logLevel)
        log.addHandler(stream_handler)
    else:
        import logging.handlers
        file_handler = logging.handlers.RotatingFileHandler(sFileName, maxBytes=1E6, backupCount=1)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        log.addHandler(file_handler)
    return log

def scadaParse(s, sep = "[,;\t ]+"):
    """
    Return a list of parameter from a string with parameters separated by comma, semicolon, space or tabulation
    """
    import re
    return list(filter(None, re.split(sep, s)))

