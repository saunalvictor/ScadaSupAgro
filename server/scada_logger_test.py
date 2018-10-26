import pytest
from scada_logger import scadaLogger

class TestScadaLogger():
    def test_wrong_pins_param(self):
        dPrm = {
            'DATA_LOGGER': {
                'pins': '0;1,2,3,A',
                'file': 'C:\\DocDD\\Dropbox\\CEMAGREF\\2012_ScadaSupAgro\\code\\server\\data.log'
            },
            'LOGGER': {
                'level': 'DEBUG'
            }, 
            'HARDWARE': {
                'test': '1'
            }
        }
        with pytest.raises(SystemExit):
            scadaLogger(dPrm)

