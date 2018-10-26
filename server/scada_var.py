from scada_var_type import ScadaVarArd, ScadaVarLin, ScadaVarExp

class ScadaDatabase:
    """
    Database of ScadaVars
    """

    varClasses = {
        'ard': ScadaVarArd,
        'lin': ScadaVarLin,
        'exp': ScadaVarExp
    }

    def __init__(self, log, dPrmDL):
        self.dPrmDL = dPrmDL
        self.vars = {}
        self.log = log
        self.lastData = {'timestamp': 0, 'data': []}
        from read_data import ReadData
        self.rd = ReadData(dPrmDL['file'])
        self.load()

    def vars_to_dict(self):
        d = {}
        for k,v in self.vars.items():
            d[k] = {
                'type': v.__class__.__name__[8:].lower(), # Suffix of class name beginning by ScadaVar...
                'options': v.options,
                'description': v.description
            }
        return d

    def dict_to_vars(self, d):

        self.vars = {}

        # Sort keys for loading taking into account dependencies
        lSorted = []
        for i in range(len(d)):
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
                self.add(var)
            except KeyError as e:
                self.log.error('Scada database corrupted: '+self.dPrmDL['database'])
                self.log.error(e)

    def load(self):
        import yaml
        bOK = False
        try:
            f = open(self.dPrmDL['database'], 'r')
        except IOError as e:
            self.log.warning(str(e))
        else:
            with f:
                try:
                    d = yaml.load(f)
                    self.dict_to_vars(d)
                    bOK = True
                except yaml.YAMLError as e:
                    self.log.error(str(e))
        if not bOK:
            self.init()

    def save(self):
        import yaml
        try:
            f = open(self.dPrmDL['database'], 'w')
        except IOError as e:
            self.log.error(str(e))
        else:
            with f:
                try:
                    yaml.dump(self.vars_to_dict(), f)
                except Exception as e:
                    self.log.error(str(e))

    def init(self):
        """
        Initialise database with raw data read by the data logger
        """
        import re
        lPins = [s for s in filter(None, re.split("[,;\t ]+",self.dPrmDL['pins']))]
        for sPin in lPins:
            self.add(ScadaVarArd(self, "A"+sPin, description="Arduino data on analog pin #%s" % (sPin)))

    def add(self, scadaVar):
        self.vars[scadaVar.name] = scadaVar
        self.save()

    def delete(self, name):
        del self.vars[name]
        self.save()

    def exists(self, name):
        return name in self.vars.keys()

    def get(self, name):
        try:
            return self.vars[name].get()
        except Exception as e:
            raise

    def getValues(self, lNames):
        """
        Get values of several variables separated by comma, semicolon, space or tabulation
        @returns
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
        Returns last analogic data number [number] with reading data optimisation
        """
        import time
        if time.time() - self.lastData['timestamp'] > float(self.dPrmDL['freq']):
            lD = self.rd.get_last_data(True)
            self.lastData = {'timestamp': time.time(), 'data': lD}
        else:
            lD = self.lastData['data']
        return lD[number + 1]

