import pytest
from scada_gateway import ScadaGateway
from scada_logger_test import TestScadaLogger

class TestScadaGateway():

    def init(self, dPrm = None):
        # Arduino data logger initialisation
        self.slt = TestScadaLogger()
        last_data = self.slt.test_write_data()
        self.dPrm = self.slt.dPrm
        self.dPrm['GATEWAY'] =  {
            'frequency': '1',
            'url': 'http://scada.dorch.fr/api/v1/ArNz7sAmfzcN2ZjcmKfT/telemetry',
            'update_var': '1'
        }
        self.dPrm['DATABASE'] = {
            'file': 'scada_logger.yaml',
            'log_level': 'INFO'
        }
        if dPrm != None: self.dPrm.update(dPrm)
        # Delete yaml database file
        import os
        try:
            os.remove(self.dPrm['DATABASE']['file'])
        except:
            pass
        self.sg = ScadaGateway(self.dPrm)
        return last_data

    def dataLogToDic(self, last_data):
        d = {}
        keys = self.sg.update_vars()
        for key in keys:
            if(key[0] == 'A'):
                d[key] = last_data[int(key[1:])]
        return d

    def test_wrong_parameter_frequency(self):
        with pytest.raises(SystemExit):
            self.init({'GATEWAY': {'frequency': '1A'}})

    def test_missing_parameter_update_var(self):
        with pytest.raises(SystemExit):
            self.init({
                'GATEWAY': {
                    'frequency': '1',
                    'url': 'http://scada.dorch.fr/api/v1/test/telemetry',
                }
            })
            self.sg.run()


    def test_send_arduino_data(self):
        dLog = self.dataLogToDic(self.init())
        self.sg.dLastDateTime = {key:"" for key in self.sg.lVars}
        dSent = self.sg.do_send()
        assert dLog == dSent

    def test_send_arduino_2_data(self):
        self.test_send_arduino_data()
        dLog = self.dataLogToDic(self.slt.test_write_data())
        from time import sleep
        sleep(float(self.dPrm['GATEWAY']['frequency']))
        dSent = self.sg.do_send()
        assert dLog == dSent

    def test_send_2times_same_data(self):
        self.test_send_arduino_data()
        dSent = self.sg.do_send()
        assert dSent == {}



if __name__ == '__main__':
    method_list = [func for func in dir(TestScadaGateway) if callable(getattr(TestScadaGateway, func))]
    test = TestScadaGateway()
    test.init()
    for func in [func for func in method_list if func[:5]=='test_']:
        test.sg.log.info("******************  START TEST {} ******************".format(func))
        getattr(test, func)()