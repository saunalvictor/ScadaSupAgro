from scada_var_test import dPrm

dPrm['LOGGER']={'level': 'DEBUG'}

class TestScadaHandler():
    @staticmethod
    def init():
        # Delete yaml database file
        import os
        try:
            os.remove(dPrm['DATABASE']['file'])
        except:
            pass
        from scada_server_handler import ScadaHandler
        return ScadaHandler(False, dPrm)

    def test_get(self):
        scadaHdlr = self.init()
        assert int(scadaHdlr.exec('get A0').split(";")[1]) == scadaHdlr.scadaDB.getAnalogic(0)
        assert scadaHdlr.exec('get')[:5] == 'ERROR'

    def test_help(self):
        scadaHdlr = self.init()
        assert scadaHdlr.exec('help')

    def test_help_instruction(self):
        scadaHdlr = self.init()
        for k in scadaHdlr.instructionSet:
            assert scadaHdlr.exec('help %s' % k)

    def test_list(self):
        scadaHdlr = self.init()
        assert scadaHdlr.exec('list')

    def test_list_variable(self):
        scadaHdlr = self.init()
        for k in scadaHdlr.scadaDB.vars:
            assert scadaHdlr.exec('list %s' % k)
        assert scadaHdlr.exec('list TOTO')[:5] == 'ERROR'

    def test_def(self):
        scadaHdlr = self.init()
        assert scadaHdlr.exec('def')[:5] == 'ERROR'
        assert scadaHdlr.exec('def ard')[:5] == 'ERROR'

    def test_def_ard(self):
        scadaHdlr = self.init()
        assert scadaHdlr.exec('def ard A2')[:5] == 'ERROR' # pin #2 is not connected (See [DATA_LOGGER]/pins)
        assert scadaHdlr.exec('def ard A1 "toto" "Too many arguments"')[:5] == 'ERROR' # 3 Args max.
        assert scadaHdlr.exec('def ard A1 "Sensor #1')[:5] == 'ERROR' # The quote is not closed ni "Sensor #1
        assert scadaHdlr.exec('def ard A1 "Sensor #1"')[:11] == 'Variable A1' # Variable updated
        assert scadaHdlr.exec('list A1')[:12] == "Variable: A1"

    def test_def_lin(self):
        scadaHdlr = self.init()
        assert scadaHdlr.exec('def lin Y0 "Water level at sensor #0" A0 0.001 0.01')[:11] == 'Variable Y0' # Variable created or updated
        assert scadaHdlr.exec('def lin Y0 "Water level at sensor #0"')[:5] == 'ERROR' # not enought arguments
        assert scadaHdlr.exec('def lin Y0 "Water level at sensor #0" A0 0.001')[:5] == 'ERROR' # not enought arguments
        assert scadaHdlr.exec('def lin Y0 "Water level at sensor #0" A0 0.001 0.01 2.5')[:5] == 'ERROR' # too many arguments
        assert scadaHdlr.exec('def lin Y0 "Water level at sensor #0" A22 0.001 0.01')[:5] == 'ERROR' # input does'nt exist
        assert scadaHdlr.exec('def lin Y0 "Water level at sensor #0" A0 0.001 abcd')[:5] == 'ERROR' # Argument should be numeric

    def test_def_exp(self):
        scadaHdlr = self.init()
        scadaHdlr.exec('def lin Y0 "Water level at sensor #0" A0 0.001 0.01')
        assert scadaHdlr.exec('def exp Q0 "Discharge at sensor #0" Y0 1.4 0.1 2.5')[:11] == 'Variable Q0' # Variable created or updated

    def test_del(self):
        scadaHdlr = self.init()
        assert scadaHdlr.exec('def lin Y1 "Toto" A0 1 1')[:11] == 'Variable Y1' # Variable created or updated
        assert scadaHdlr.exec('del Y1') == 'Variable Y1 deleted'
        assert scadaHdlr.exec('del Y1')[:5] == 'ERROR'

    def test_net(self):
        scadaHdlr = self.init()
        assert scadaHdlr.exec('net too many many arguments')[:5] == 'ERROR'
        assert scadaHdlr.exec('net Two Argument')[:5] == 'ERROR'
        assert scadaHdlr.exec('net Not#Alphanumeric 1')[:5] == 'ERROR'
        assert scadaHdlr.exec('net DEVICE_TOTO Description NotNumeric')[:5] == 'ERROR'
        assert scadaHdlr.exec('net DEVICE_TOTO Description 0')[:5] == 'ERROR' # Number of variables <=0
        assert scadaHdlr.exec('net TEST_DEVICE "Device description" 1') == "Device TEST_DEVICE created"

    def test_del_device(self):
        scadaHdlr = self.init()
        scadaHdlr.exec('net TEST_DEVICE "Device description" 1')
        assert scadaHdlr.exec('del TEST_DEVICE') == 'Device TEST_DEVICE deleted'

    def test_def_net(self):
        scadaHdlr = self.init()
        scadaHdlr.exec('net TEST_DEVICE "Device description" 1')
        assert scadaHdlr.exec('def net not_enough_arguments')[:5] == 'ERROR'
        assert scadaHdlr.exec('def net')[:5] == 'ERROR'
        assert scadaHdlr.exec('def net N0 "Description of the first data of the device" FAKE_DEVICE 0')[:5] == "ERROR"
        assert scadaHdlr.exec('def net N0 "Description of the first data of the device" TEST_DEVICE 0')[:11] == "Variable N0"

    def test_get_net(self):
        scadaHdlr = self.init()
        scadaHdlr.exec('net TEST_DEVICE "Device description" 1')
        scadaHdlr.exec('def net N0 "Description of the first data of the device" TEST_DEVICE 0')
        scadaHdlr.exec('get N0')[-5:] == "1.234"

if __name__ == '__main__':
    scadaHdlr = TestScadaHandler.init()
    while scadaHdlr.bConnected:
        print(scadaHdlr.exec(input()))
