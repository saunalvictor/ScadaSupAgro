import pytest
from scada_logger import ScadaLogger


class TestScadaLogger():
    def init(self):
        import os
        self.dPrm = {
            'DATA_LOGGER': {
                'file': os.path.join(os.getcwd(),'data.log'),
                'valuemin': '0',
                'freq': '0.1'
            },
            'LOGGER': {
                'level': 'DEBUG'
            },
            'HARDWARE': {
                'test': '1',
                'nb_pins': '4',
                'test_maxval': '1023'
            }
        }
        # Delete logger file
        import os
        try:
            os.remove(self.dPrm['DATA_LOGGER']['file'])
        except:
            pass

    def test_wrong_pins_param(self):
        self.init()
        self.dPrm['DATA_LOGGER']['pins'] = '0;1,2,3,A'
        with pytest.raises(SystemExit):
            sl = ScadaLogger(self.dPrm)
            sl.run()

    def test_write_data(self):
        self.init()
        self.dPrm['DATA_LOGGER']['pins'] = '0,1,2,3'
        sl = ScadaLogger(self.dPrm)
        sl.do_measurement()
        from scada_var_readers import LoggerReader
        lr = LoggerReader(self.dPrm['DATA_LOGGER']['file'])
        last_data = lr.get_last_data()
        assert len(last_data) == 4
        return last_data

    def test_write_data_minvalue(self):
        last_data = self.test_write_data()
        self.dPrm['DATA_LOGGER']['valuemin'] = '1024'
        sl = ScadaLogger(self.dPrm)
        sl.do_measurement()
        from scada_var_readers import LoggerReader
        lr = LoggerReader(self.dPrm['DATA_LOGGER']['file'])
        assert lr.get_last_data() == last_data


if __name__ == '__main__':
    method_list = [func for func in dir(TestScadaLogger) if callable(getattr(TestScadaLogger, func))]
    test = TestScadaLogger()
    for func in [func for func in method_list if func[:5]=='test_']:
        getattr(test, func)()