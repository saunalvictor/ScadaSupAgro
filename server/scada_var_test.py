from scada_var import ScadaDatabase, ScadaVarArd, ScadaVarLin, ScadaVarExp

from scada_misc import createLog

dPrmDL = {
    'file': 'C:\\DocDD\\Dropbox\\CEMAGREF\\2012_ScadaSupAgro\\code\\server\\data.log',
    'database': 'C:\\DocDD\\Dropbox\\CEMAGREF\\2012_ScadaSupAgro\\code\\server\\scada_logger.yaml',
    'pins': '0,1',
    'freq': '0.5'
}

# Delete yaml database file
import os
try:
    os.remove(dPrmDL['database'])
except:
    pass

scadaDB = ScadaDatabase(createLog('DEBUG'), dPrmDL)
scadaDB.init()

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


class TestScadaDatabase:

    def test_init(self):
        assert scadaDB.vars['A0'].name == "A0"

    def test_getAnalogic(self):
        d = scadaDB.get('A0')
        assert d > 0 and d < 1024

    def test_varLin(self):
        assert scadaDB.get('Y0') == scadaDB.get('A0') * 0.001 - 0.23

    def test_varExp(self):
        assert scadaDB.get('Q0') == 1.4 * pow(max(0,scadaDB.get('Y0')-0.1), 2.5)

    def test_save_and_load(self):
        scadaDB.save()
        scadaDB.load()
        self.test_varLin()

    def test_wrong_input(self):
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

if __name__ == '__main__':
    scadaDB.save()
    scadaDB.load()
