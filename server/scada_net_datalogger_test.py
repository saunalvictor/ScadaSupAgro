from scada_server_handler_test import dPrm
dPrm['NET_DATA_LOGGER'] = {
    'tcp_port': '34060',
    'file': 'network_data_{}.log'
}

from scada_net_datalogger import NetDeviceHandler
from scada_misc import createLog
netHdlr = NetDeviceHandler(dPrm, createLog('DEBUG'))

class TestNetDeviceHandler():
    def test_device_not_registered(self):
        assert netHdlr.get('/fake_device/9999')[:5] == 'ERROR'

    def test_device_one_data(self):
        from scada_var_type import ScadaDevice
        netHdlr.scadaDB.addDevice(ScadaDevice("TEST_DEVICE", 1, "Test device","test_token"))
        assert netHdlr.get('/test_token/1.234')[:15] == '1 data recorded'


if __name__ == '__main__':
    method_list = [func for func in dir(TestNetDeviceHandler) if callable(getattr(TestNetDeviceHandler, func))]
    test = TestNetDeviceHandler()
    for func in [func for func in method_list if func[:5]=='test_']:
        getattr(test, func)()