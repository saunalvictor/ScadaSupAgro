from scada_database import ScadaDatabase, ScadaVarArd, ScadaVarLin, ScadaVarExp

from scada_misc import createLog

dPrm = {
    'DATA_LOGGER': {
        'file': 'data.log',
        'pins': '0,1',
        'freq': '0.5'
    },
    'NET_DATA_LOGGER': {
        'file': 'netdata_{}.log',
    },
    'DATABASE': {
        'file': 'scada_logger.yaml',
    }
}

class TestScadaDatabase:
    def init(self):
        # Writing data.log
        from scada_logger_test import TestScadaLogger
        tsl = TestScadaLogger()
        tsl.test_write_data()

        # Delete yaml database file
        import os
        try:
            os.remove(dPrm['DATABASE']['file'])
        except:
            pass
        scadaDB = ScadaDatabase(createLog('DEBUG'), dPrm)
        scadaDB.add(
            ScadaVarLin(scadaDB, 'Y0', {
                'input': 'A0',
                'a': 0.001,
                'b': -0.23
            }, description='Water depth on sensor #0 (m)')
        )
        scadaDB.add(
            ScadaVarExp(scadaDB, 'Q0', {
                'input': 'Y0',
                'a': 1.4,
                'b': 0.10,
                'c': 2.5
            }, description='Water discharge on sensor #0 (m3/s)')
        )

        return scadaDB

    def test_init(self):
        scadaDB = self.init()
        assert scadaDB.vars['A0'].name == "A0"

    def test_getAnalogic(self):
        scadaDB = self.init()
        d = scadaDB.get('A0')
        assert d > 0 and d < 1024

    def test_varLin(self):
        scadaDB = self.init()
        assert scadaDB.get('Y0') == scadaDB.get('A0') * 0.001 - 0.23

    def test_varExp(self):
        scadaDB = self.init()
        assert scadaDB.get('Q0') == 1.4 * pow(max(0,scadaDB.get('Y0')-0.1), 2.5)

    def test_save_and_load(self):
        scadaDB = self.init()
        scadaDB.init()
        scadaDB.load()
        self.test_varLin()

    def test_wrong_input(self):
        scadaDB = self.init()
        import pytest
        with pytest.raises(Exception):
            scadaDB.add(
                ScadaVarExp(scadaDB, 'Q1', {
                    'input': 'Y1',
                    'a': 1.4,
                    'b': 0.10,
                    'c': 2.5
                })
            )

    def test_refere_to_deleted_var(self):
        scadaDB = self.init()
        scadaDB.add(
            ScadaVarLin(scadaDB, 'Y1', {
                'input': 'A1',
                'a': 0.001,
                'b': -0.23
            }, description='Water depth on sensor #1 (m)')
        )
        scadaDB.add(
            ScadaVarExp(scadaDB, 'Q1', {
                'input': 'Y1',
                'a': 1.4,
                'b': 0.10,
                'c': 2.5
            })
        )
        scadaDB.delete('Y1')
        import pytest
        with pytest.raises(Exception):
            scadaDB.get('Q1')

    def scadaDB_addDevice(self):
        scadaDB = self.init()
        from scada_var_type import ScadaDevice
        scadaDB.addDevice(ScadaDevice("TEST_DEVICE", 1, "test_device"))
        return scadaDB

    def test_addDevice(self):
        scadaDB = self.scadaDB_addDevice()
        assert scadaDB.devices['TEST_DEVICE'].id == "TEST_DEVICE"
        assert scadaDB.devices['TEST_DEVICE'].n == 1
        assert scadaDB.devices['TEST_DEVICE'].description == "test_device"

    def test_load_save_device(self):
        scadaDB = self.scadaDB_addDevice()
        token = scadaDB.devices['TEST_DEVICE'].token
        scadaDB.init()
        scadaDB.load()
        assert scadaDB.devices['TEST_DEVICE'].id == "TEST_DEVICE"
        assert scadaDB.devices['TEST_DEVICE'].n == 1
        assert scadaDB.devices['TEST_DEVICE'].description == "test_device"
        assert scadaDB.devices['TEST_DEVICE'].token == token

    def test_varNet(self):
        scadaDB = self.init()
        # Create one device "TEST_DEVICE" and one record
        from scada_net_datalogger_test import TestNetDeviceHandler
        ndh = TestNetDeviceHandler()
        ndh.test_device_one_data()
        # Create variable
        scadaDB.load() # Modified by ndh
        from scada_var_type import ScadaVarNet
        scadaDB.add(ScadaVarNet(scadaDB, "N0", {'device': 'TEST_DEVICE', 'index': 0}, "Variable associated to first data of TEST_DEVICE"))
        assert scadaDB.get('N0') == 1.234


if __name__ == '__main__':
    method_list = [func for func in dir(TestScadaDatabase) if callable(getattr(TestScadaDatabase, func))]
    test = TestScadaDatabase()
    for func in [func for func in method_list if func[:5]=='test_']:
        getattr(test, func)()
