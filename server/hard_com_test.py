from hard_com import HardCom
from scada_misc import createLog

dPrmHard = {
    "test": "1",
    "test_maxval": "100",
    "nb_pins": "12"
}

hc = HardCom(createLog('DEBUG'), dPrmHard)

class TestHardCom():
    def test_get(self):
        assert len(hc.get([0,1,2,3]))==4

    def test_out_of_range0(self):
        assert "ERROR" not in hc.get([0,1,2,3])

    def test_out_of_range(self):
        assert "ERROR" in hc.get([12,13])

    def test_type_error(self):
        assert "ERROR" in hc.get("1")
