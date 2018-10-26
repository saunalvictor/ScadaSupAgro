import socketserver

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):

        from scada_misc import getIniParameters
        scada = ScadaHandler(self, getIniParameters("scada.ini"))

        while scada.bConnected:
            sRecv = ""
            while sRecv == "":
                # self.request is the TCP socket connected to the client
                self.data = self.request.recv(1024)
                if not self.data:
                    scada.bConnected = False
                    break
                self.data = self.data.strip()
                sRecv = str(self.data, "ISO-8859-1")
            if not scada.bConnected: break
            scada.exec(sRecv)
        scada.log.info("Connection ended with %s" % self.client_address[0])


class ScadaHandler:
    def __init__(self, tcpHandler, dPrm):
        self.tcpHandler = tcpHandler
        self.bConnected = True
        self.bTest = (tcpHandler == False)
        self.instructionSet = {
            'CLOSE': self.instrClose,
            'DEF': self.instrDef,
            'DEL': self.instrDel,
            'GET': self.instrGet,
            'HELP': self.instrHelp,
            'LIST': self.instrList
        }
        from scada_misc import createLog
        self.dPrm = dPrm
        self.log = createLog(self.dPrm['LOGGER']['level'])

        from scada_var import ScadaDatabase
        self.scadaDB = ScadaDatabase(self.log, self.dPrm['DATA_LOGGER'])

        self.send(self.open())

    def open(self):
        return "\r\n".join([
            "************************************************************************",
            "* SupAgro SCADA server v2018                                           *",
            "* UMR G-EAU, Irstea, SupAgro, David Dorchies, david.dorchies@irstea.fr *",
            "************************************************************************",
            "",
            "Connection opened. Please type an instruction or HELP for getting the list of available instructions."
        ])

    def send(self, sSend):
        import socket
        sSend = sSend + "\r\n"
        try:
            if not self.bTest: self.tcpHandler.request.sendall(sSend.encode("ISO-8859-1"))
            self.log.debug("Data sent : "+sSend.strip())
        except socket.error as e:
            self.log.error("Socket {} {}".format(e.errno, e.strerror))
            self.bConnected = False

    def exec(self, sRecv):
        from scada_misc import scadaParse
        lRecv = scadaParse(sRecv) # Parsing with wide choice of separators
        sInstruction = lRecv[0].upper()

        if not sInstruction in self.instructionSet.keys():
            sSend = "ERROR: Instruction '{}' not handled by the server. Type HELP to get the list of available instructions.".format(lRecv[0])
        else:
            bOK = True
            if sInstruction == "DEF":
                try:
                    import shlex
                    lRecv = shlex.split(sRecv) # Command line parsing for DEF instruction
                except ValueError as e:
                    sSend = 'ERROR: ' + str(e)
                    bOK =False
            if bOK: sSend = self.instructionSet[sInstruction](lRecv)

        self.send(sSend)
        return sSend

    def instrGet(self, lRecv):
        """
        Return list of data from the scada logger with record date in UTC and data values separated by semi-colon

        Usage: GET var1,var2

        Example: 'GET R0,R1' returns '2018-10-22 11:50:53,092;58'
        """
        if len(lRecv) > 1:
            try:
                return self.scadaDB.getValues(lRecv[1:])
            except Exception as e:
                return "ERROR: Unknown variable " + str(e)
        else:
            return "ERROR: Instruction GET needs at least one parameter. Type HELP GET for help."

    def instrDef(self, lRecv):
        """
        Create or update a variable in the SCADA database

        Usage: DEF variable type description [options]

        with:
            - type: type of the variable ('ard' for Arduino analog, 'lin' for linear transformation, 'exp' for exponential transformation)
            - variable: the name of the variable to create/update
            - description: a description of the variable (use quotes for more than one word)
            - options: depends on the type of variable to define (see below)

        Description of variable types:
            - Arduino analog: 'ard'
                There is no option to provide.
                Example: DEF A0 "Analog input for sensor #0" ard
            - Linear transformation: 'lin'
                Use an input variable X and apply a linear transformation with the equation Y = a * X + b
                The 'options' argument contains 3 arguments in this order:
                    - input variable: the variable used for the calculation
                    - coefficient a: the slope of the linear equation
                    - coefficient b: intercpet of the linear equation
                Example: DEF Y0 "Water depth at sensor #0" lin A0 0.001 -0.002
            - Exponential transformation: 'exp'
                Use an input variable X and apply this equation Y = a * (X - b) ^ c
                The 'options' argument contains 4 arguments in this order:
                    - input variable: the variable used for the calculation
                    - coefficient a
                    - coefficient b
                    - coefficient c
                Example for getting the discharge using King's triangular weir equation with a sill elevation of 10 cm:
                    DEF Q0 "Discharge at sensor #0" exp Y0 1.4 0.1 2.5
        """
        if len(lRecv) < 3:
            return "ERROR: Instruction DEF needs at least 2 parameters. Type HELP DEF for help."
        sType = lRecv[1].lower()
        if not sType in self.scadaDB.varClasses:
            return "ERROR: type should be one of %s" % ", ".join(self.scadaDB.varClasses.keys())

        if lRecv[2] in self.scadaDB.vars:
            sOperation = "updated"
        else:
            sOperation = "created"
        func = getattr(self, "defType_%s" % sType)
        sOut = func(lRecv[2:])
        if sOut == True:
            return 'Variable {0} {1}. Type \'LIST {0}\' for viewing details, type \'GET {0}\' for getting real time data!'.format(lRecv[2], sOperation)
        else:
            return sOut

    def defType_ard(self, lArgs):
        """
        Define or update Arduino variable
        """
        from scada_misc import scadaParse
        lAvailables = ['A'+s for s in scadaParse(self.dPrm['DATA_LOGGER']['pins'])]
        if not lArgs[0] in lAvailables:
            return 'ERROR: the variable name should be one of [%s]' % ", ".join(lAvailables)
        if len(lArgs) > 2:
            return 'ERROR: 2 or 3 arguments are expected'
        if len(lArgs) == 2:
            sDescription = lArgs[1]
        else:
            sDescription = "Arduino data on analog pin #%s".format(lArgs[0][1:])
        from scada_var_type import ScadaVarArd
        try:
            self.scadaDB.add(ScadaVarArd(self.scadaDB, lArgs[0], description=sDescription))
        except Exception as e:
            return 'ERROR: ' + str(e)
        return True

    def defType_lin(self, lArgs):
        """
        Define or update linear transformation variable
        """
        if len(lArgs) != 5:
            return 'ERROR: 6 arguments are expected'
        from scada_var_type import ScadaVarLin
        try:
            self.scadaDB.add(ScadaVarLin(self.scadaDB, lArgs[0], description=lArgs[1], options={'input': lArgs[2], 'a': lArgs[3], 'b': lArgs[4]}))
        except Exception as e:
            return 'ERROR: ' + str(e)
        return True

    def defType_exp(self, lArgs):
        """
        Define or update linear transformation variable
        """
        if len(lArgs) != 6:
            return 'ERROR: 7 arguments are expected'
        from scada_var_type import ScadaVarExp
        try:
            self.scadaDB.add(ScadaVarExp(self.scadaDB, lArgs[0], description=lArgs[1], options={'input': lArgs[2], 'a': lArgs[3], 'b': lArgs[4], 'c': lArgs[5]}))
        except Exception as e:
            return 'ERROR: ' + str(e)
        return True

    def instrDel(self, lRecv):
        """
        Delete a variable from the database

        Usage : DEL variable
        """

        if len(lRecv)!=2:
            return "ERROR: Instruction DEL needs 1 parameter. Type HELP DEF for help."

        sVar = lRecv[1]
        if not sVar in self.scadaDB.vars.keys() :
            return "ERROR: Variable '{}' doesn\'t exist. Type LIST to get the list of existing variables.".format(sVar)
        else:
            self.scadaDB.delete(sVar)
            return "Variable {} deleted".format(sVar)


    def instrList(self, lRecv):
        """
        List available variables on the SCADA database
        """
        if len(lRecv)==1:
            l = ["%s: %s" % (s, self.scadaDB.vars[s].description) for s in self.scadaDB.vars.keys()]
            return "\r\n".join(l)
        else:
            sVar = lRecv[1]
            if not self.scadaDB.exists(sVar) :
                return "ERROR: Variable '{}' doesn\'t exist. Type LIST to get the list of existing variables.".format(sVar)
            else:
                l = ["%s: %s" % (k, str(v)) for k,v in self.scadaDB.vars[sVar].options.items()]
                l.insert(0,"Type: "+self.scadaDB.vars[sVar].__class__.__name__[8:]) # [8:] for skeeping ScadaVar in the beginning of class name
                l.insert(0,"Description: "+self.scadaDB.vars[sVar].description)
                l.insert(0, "Variable: "+sVar)
                return "\r\n".join(l)

    def instrHelp(self, lRecv):
        """
        Display help on the available instructions
        """
        if len(lRecv)==1:
            l = [k + ": " + self.getFunctionDoc(v) for k,v in self.instructionSet.items()]
            l.append("Type 'HELP instruction' for more detail.")
            return "\r\n".join(l)
        else:
            sInstruction = lRecv[1].upper()
            if not sInstruction in self.instructionSet.keys():
                return "ERROR: Instruction '{}' not handled by the server. Type HELP to get the list of available instructions.".format(sInstruction)
            else:
                return self.getFunctionDoc(self.instructionSet[sInstruction], True)

    def instrClose(self, lRecv):
        """
        Gracefully close the socket connection with the server
        """
        self.bConnected = False
        return "Connection closed by the user"

    @staticmethod
    def getFunctionDoc(func, bFull = False):
        from scada_misc import scadaParse
        l = func.__doc__.splitlines()
        if l[0].strip() == "": del l[0]
        indent = len(l[0]) - len(l[0].lstrip(' '))
        if bFull:
            return "\r\n".join([s[indent:] for s in l])
        else:
            return l[0].strip()

    @staticmethod
    def generate_credentials(length=20):
        if not isinstance(length, int) or length < 8:
            raise ValueError("temp password must have positive length")

        chars = "abcdefghjklmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789"
        from os import urandom
        return "".join(chars[ord(c) % len(chars)] for c in urandom(length))