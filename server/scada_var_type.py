class ScadaVar:
    """
    Data management
    """
    def __init__(self, database, name, options = {}, description = ""):
        self.database = database
        self.name = name
        self.options = options
        self.description = description
        self.setOptions(options)
        self.timestamp = ""
        self.lastdata = None

    def setOptions(self, options = {}):
        """
        Check, format and assign attributes for options of the variable. Raise error if necessary.
        """
        if 'input' in options:
            try:
                self.database.vars[options['input']]
            except KeyError:
                raise Exception('Definition of variable {}: {} input variable doesn\'t exist'.format(self.name, options['input']))
            self.input = options['input']
        # All others options should be of type float
        for k,v in options.items():
            if not k in ['input', 'device']:
                try:
                    setattr(self, k, float(v))
                except Exception:
                    raise Exception('Definition of variable {}: argument {}={} should be a float number'.format(self.name, k, v))

    def get(self):
        raise NotImplementedError('Subclasses must override ScadaVar::get()')

    def getInput(self):
        return self.database.get(self.input)

    def getTimeStamp(self):
        return self.timestamp


class ScadaVarArd(ScadaVar):
    """
    Management of Raw data provided by the sensors connected to the Arduino
    """

    def get(self):
        d = self.database.getAnalogic(int(self.name[1:]))
        self.timestamp = self.database.lastData['timestamp']
        self.database.log.debug('ScadaVarArd.get({})={}'.format(self.name,str(d)))
        return d


class ScadaVarNet(ScadaVar):
    """
    Management of local network data
    """
    def __init__(self, database, name, options = {}, description = ""):
        super().__init__(database, name, options, description)
        self.index = int(self.options['index'])
        self.device = self.options['device']

    def get(self):
        filename = self.database.dPrm['NET_DATA_LOGGER']['file'].format(self.options['device'])
        from scada_var_readers import LoggerReader
        lr = LoggerReader(filename)
        lD = lr.get_last_data(True, numericCast=float)
        self.timestamp = lD[0]
        self.lastdata = lD[self.index + 1]
        self.database.log.debug('ScadaVarNet.get({})={}'.format(self.name,str(self.lastdata)))
        return self.lastdata


class ScadaVarCalc(ScadaVar):
    def __init__(self, database, name, options = {}, description = ""):
        ScadaVar.__init__(self, database, name, options, description)
        if 'input' in options:
            try:
                self.database.vars[options['input']]
            except KeyError:
                raise Exception('Definition of variable {}: {} input variable doesn\'t exist'.format(self.name, options['input']))
            self.input = options['input']
        else:
            raise Exception('Definition of variable {} should have \"input\" in its options'.format(self.name))

    def getTimeStamp(self):
        return self.database.vars[self.input].getTimeStamp()


class ScadaVarLin(ScadaVarCalc):
    """
    Management of data calculated from Y=a*X+b
    """
    def __init__(self, database, name, options = {}, description = ""):
        ScadaVarCalc.__init__(self, database, name, options, description)
        try:
            self.a = float(options['a'])
            self.b = float(options['b'])
        except Exception as e:
            raise Exception('Definition of variable {}, error on options \"a\" or \"b\": {}'.format(self.name, str(e)))

    def get(self):
        d = self.a * self.getInput() + self.b
        self.database.log.debug('ScadaVarLin.get({})={}'.format(self.name,str(d)))
        return d


class ScadaVarExp(ScadaVarCalc):
    """
    Management of data calculated from Y=a*X+b
    """
    def __init__(self, database, name, options = {}, description = ""):
        ScadaVarCalc.__init__(self, database, name, options, description)
        try:
            self.a = float(options['a'])
            self.b = float(options['b'])
            self.c = float(options['c'])
        except Exception as e:
            raise Exception('Definition of variable {}, error on options \"a\", \"b\" or \"c\": {}'.format(self.name, str(e)))

    def get(self):
        d = self.a * pow(max(0, self.getInput() - self.b), self.c)
        self.database.log.debug('ScadaVarExp.get({})={}'.format(self.name,str(d)))
        return d


class ScadaDevice:
    def __init__(self, sDevice, nVars, sDescription, token=""):
        self.id = sDevice
        self.n = nVars
        if token == "":
            self.token = self.generate_credentials()
        else:
            self.token = token
        self.description = sDescription

    @staticmethod
    def generate_credentials(length=20):
        if not isinstance(length, int) or length < 8:
            raise ValueError("temp password must have positive length")

        chars = "abcdefghjklmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789"
        from os import urandom
        return "".join(chars[c % len(chars)] for c in urandom(length))

    @staticmethod
    def checkDeviceID(name):
        import re
        return (re.match('^[\w-]+$', name) is not None)
