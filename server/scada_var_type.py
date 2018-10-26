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

    def setOptions(self, options = {}):
        """
        Check, format and assign attributes for options of the variable. Raise error if necessary.
        """
        if 'input' in options:
            try:
                d = self.database.vars[options['input']]
            except KeyError as e:
                raise Exception('Definition of variable {}: {} input variable doesn\'t exist'.format(self.name, options['input']))
            self.input = options['input']
        # All others options should be of type float
        for k,v in options.items():
            if k != 'input':
                try:
                    setattr(self, k, float(v))
                except Exception as e:
                    raise Exception('Definition of variable {}: argument {}={} should be a float number'.format(self.name, k, v))

    def get(self):
        raise NotImplementedError('Subclasses must override ScadaVar::get()')

    def getInput(self):
        return self.database.get(self.input)


class ScadaVarArd(ScadaVar):
    """
    Management of Raw data
    """

    def get(self):
        d = self.database.getAnalogic(int(self.name[1:]))
        self.database.log.debug('ScadaVarRaw.get='+str(d))
        return d

class ScadaVarLin(ScadaVar):
    """
    Management of data calculated from Y=a*X+b
    """

    # def __init__(self, database, name, options, description = ""):
    #     ScadaVar.__init__(self, database, name, options, description)
    #     self.a = options['a']
    #     self.b = options['b']
    #     self.input = options['input']

    def get(self):
        d = self.a * self.getInput() + self.b
        self.database.log.debug('ScadaVarLin.get='+str(d))
        return d

class ScadaVarExp(ScadaVar):
    """
    Management of data calculated from Y=a*X+b
    """

    # def __init__(self, database, name, options, description = ""):
    #     ScadaVar.__init__(self, database, name, options, description)
    #     self.a = options['a']
    #     self.b = options['b']
    #     self.c = options['c']
    #     self.input = options['input']

    def get(self):
        d = self.a * pow(max(0, self.getInput() - self.b), self.c)
        self.database.log.debug('ScadaVarExp.get='+str(d))
        return d
