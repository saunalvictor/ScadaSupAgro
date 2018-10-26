from scada_var_test import dPrmDL

dPrm = {
    'LOGGER': {
        'level': 'DEBUG'
    },
    'DATA_LOGGER': dPrmDL
}

from scada_server_handler import ScadaHandler
scadaHdlr = ScadaHandler(False, dPrm)

class TestScadaHandler():
    def test_get(self):
        assert int(scadaHdlr.exec('get A0').split(";")[1]) == scadaHdlr.scadaDB.getAnalogic(0)
        assert scadaHdlr.exec('get')[:5] == 'ERROR'

    def test_help(self):
        assert scadaHdlr.exec('help')

    def test_help_instruction(self):
        for k in scadaHdlr.instructionSet:
            assert scadaHdlr.exec('help %s' % k)

    def test_list(self):
        assert scadaHdlr.exec('list')

    def test_list_variable(self):
        for k in scadaHdlr.scadaDB.vars:
            assert scadaHdlr.exec('list %s' % k)
        assert scadaHdlr.exec('list TOTO')[:5] == 'ERROR'

    def test_def(self):
        assert scadaHdlr.exec('def')[:5] == 'ERROR'
        assert scadaHdlr.exec('def ard')[:5] == 'ERROR'

    def test_def_ard(self):
        assert scadaHdlr.exec('def ard A2')[:5] == 'ERROR' # pin #2 is not connected (See [DATA_LOGGER]/pins)
        assert scadaHdlr.exec('def ard A1 "toto" "Too many arguments"')[:5] == 'ERROR' # 3 Args max.
        assert scadaHdlr.exec('def ard A1 "Sensor #1')[:5] == 'ERROR' # The quote is not closed ni "Sensor #1
        assert scadaHdlr.exec('def ard A1 "Sensor #1"')[:11] == 'Variable A1' # Variable updated
        assert scadaHdlr.exec('list A1')[:12] == "Variable: A1"

    def test_def_lin(self):
        assert scadaHdlr.exec('def lin Y0 "Water level at sensor #0" A0 0.001 0.01')[:11] == 'Variable Y0' # Variable created or updated
        assert scadaHdlr.exec('def lin Y0 "Water level at sensor #0"')[:5] == 'ERROR' # not enought arguments
        assert scadaHdlr.exec('def lin Y0 "Water level at sensor #0" A0 0.001')[:5] == 'ERROR' # not enought arguments
        assert scadaHdlr.exec('def lin Y0 "Water level at sensor #0" A0 0.001 0.01 2.5')[:5] == 'ERROR' # too many arguments
        assert scadaHdlr.exec('def lin Y0 "Water level at sensor #0" A22 0.001 0.01')[:5] == 'ERROR' # input does'nt exist
        assert scadaHdlr.exec('def lin Y0 "Water level at sensor #0" A0 0.001 abcd')[:5] == 'ERROR' # Argument should be numeric

    def test_def_exp(self):
        assert scadaHdlr.exec('def exp Q0 "Discharge at sensor #0" Y0 1.4 0.1 2.5')[:11] == 'Variable Q0' # Variable created or updated

    def test_del(self):
        assert scadaHdlr.exec('def lin Y1 "Toto" A0 1 1')[:11] == 'Variable Y1' # Variable created or updated
        assert scadaHdlr.exec('del Y1') == 'Variable Y1 deleted'
        

if __name__ == '__main__':
    while scadaHdlr.bConnected:
        print(scadaHdlr.exec(input()))