from scada_var_type import ScadaVarArd, ScadaVarLin, ScadaVarExp, ScadaVarNet

class ScadaDatabase:
    """
    Database of ScadaVars
    """

    varClasses = {
        'ard': ScadaVarArd,
        'lin': ScadaVarLin,
        'exp': ScadaVarExp,
        'net': ScadaVarNet
    }

    def __init__(self, log, dPrm):
        self.dPrm = dPrm
        self.dPrmDL = dPrm['DATA_LOGGER']
        self.vars = {}
        self.devices = {}
        self.log = log
        self.lastData = {'timestamp': 0, 'data': []}
        import re
        self.lPins = [s for s in filter(None, re.split("[,;\t ]+",self.dPrmDL['pins']))]
        from scada_var_readers import LoggerReader
        try:
            self.rd = LoggerReader(self.dPrmDL['file'])
        except IOError as e:
            log.error('File: {}: {}'.format(self.dPrmDL['file'], str(e)))
        self.load()

    def vars_to_dict(self):
        d = {}
        for k,v in self.vars.items():
            d[k] = {
                'type': v.__class__.__name__[8:].lower(), # Suffix of class name beginning by ScadaVar...
                'options': v.options if v.options != {} else {},
                'description': v.description
            }
        return d

    def dict_to_vars(self, d):

        self.vars = {}

        # Sort keys for loading taking into account dependencies
        lSorted = []
        while len(lSorted) < len(d):
            lUnsorted = list(set(d.keys()) - set(lSorted)) # Get difference between two lists https://stackoverflow.com/a/3462160
            if len(lUnsorted) == 0:
                break
            for k in lUnsorted:
                v = d[k]
                if 'input' in v['options']:
                    if v['options']['input'] in lSorted: # Dependency already loaded, current key not already loaded
                        lSorted.append(k)
                else: # Raw without dependency
                    lSorted.append(k)


        if len(lSorted) < len(d):
            for k in d:
                if not k in lSorted:
                    raise Exception('%s input variable declared in %s doesn\'t exist' % (v['options']['input'], k))

        for k in lSorted:
            v = d[k]
            try:
                var = self.varClasses[v['type'].lower()](self, k, v['options'], v['description'])
                self.add(var, False)
            except KeyError as e:
                self.log.error('Scada database corrupted: '+self.dPrm['DATABASE']['file'])
                self.log.error(e)

    def dict_to_devices(self, d):
        from scada_var_type import ScadaDevice
        for v in d.values():
            try:
                self.addDevice(ScadaDevice(v['id'],v['n'],v['description'],v['token']), False)
            except:
                raise

    def devices_to_dict(self):
        d = {}
        for k,device in self.devices.items():
            d[k] = {
                'id': device.id,
                'description': device.description,
                'n': device.n,
                'token': device.token
            }
        return d

    def load(self):
        import yaml
        bOK = False
        try:
            f = open(self.dPrm['DATABASE']['file'], 'r')
        except IOError as e:
            self.log.warning("Reading from {}: {}".format(self.dPrm['DATABASE']['file'], str(e)))
        else:
            with f:
                try:
                    d = yaml.load(f)
                    bOK = True
                except yaml.YAMLError as e:
                    self.log.error("YAML loading {}: {}".format(self.dPrm['DATABASE']['file'], str(e)))
        if bOK:
            bOK = False
            try:
                self.dict_to_vars(d['vars'])
                self.dict_to_devices(d['devices'])
                bOK = True
            except Exception as e:
                self.log.error("Converting {} to objects: {}".format(self.dPrm['DATABASE']['file'], str(e)))
        if not bOK:
            self.init()

    def save(self):
        import yaml
        try:
            f = open(self.dPrm['DATABASE']['file'], 'w')
        except IOError as e:
            self.log.error("Saving to {}: {}".format(self.dPrm['DATABASE']['file'], str(e)))
        else:
            with f:
                try:
                    yaml.dump({
                        'vars': self.vars_to_dict(),
                        'devices': self.devices_to_dict()
                    }, f)
                except Exception as e:
                    self.log.error("Saving to YAML format {}: {}".format(self.dPrm['DATABASE']['file'], str(e)))

    def init(self):
        """
        Initialise database with raw data read by the data logger
        """
        self.vars = {}
        self.devices = {}
        
        for sPin in self.lPins:
            self.add(ScadaVarArd(self, "A"+sPin, description="Arduino data on analog pin #%s" % (sPin)), False)

    def add(self, scadaVar, bLoad = True):
        if bLoad: self.load()
        self.vars[scadaVar.name] = scadaVar
        if bLoad: self.save()

    def addDevice(self, device, bLoad = True):
        if bLoad: self.load()
        self.devices[device.id] = device
        if bLoad: self.save()

    def delete(self, name):
        self.load()
        del self.vars[name]
        self.save()

    def deleteDevice(self, deviceId):
        self.load()
        del self.devices[deviceId]
        self.save()

    def exists(self, name):
        return name in self.vars.keys()

    def get(self, name):
        try:
            return self.vars[name].get()
        except:
            raise

    def getValues(self, lNames):
        """
        Get values of several variables
        @param lNames list of variables
        """
        lD = []
        for name in lNames:
            lD.append(self.get(name))
        lsD = [str(i) for i in lD]
        lsD.insert(0, self.lastData['data'][0])
        sOut = ";".join(lsD)
        self.log.debug('ScadaDatabase.getValues(%s) => %s' % (",".join(lNames), sOut))
        return sOut

    def getAnalogic(self, number):
        """
        Return last analogic data on pin number [number] with reading data optimisation
        """
        import time
        if time.time() - self.lastData['timestamp'] > float(self.dPrmDL['freq']):
            lD = self.rd.get_last_data(True)
            self.lastData = {'timestamp': time.time(), 'data': lD}
        else:
            lD = self.lastData['data']
        return lD[self.lPins.index(str(number)) + 1]

    def getDeviceFromToken(self, token):
        """
        Return the device associated to the given token.
        Return False if the token is not found
        """
        for device in self.devices.values():
            if device.token == token:
                return device
        return False

    def getTimeStamp(self, name):
        return self.vars[name].getTimeStamp()

