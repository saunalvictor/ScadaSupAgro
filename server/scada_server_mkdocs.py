from scada_server_handler import ScadaHandler
from scada_misc import getIniParameters

sHelp = """# SCADA server protocol

## List of available instructions

"""

sh = ScadaHandler(False, getIniParameters("scada.ini"))

sHelp += "\n".join(['- '+line for line in sh.instrHelp([""]).splitlines()[:-1]])+"\n"

for k,v in sh.instructionSet.items():
    sHelp +=(
        "\n"
        "## Instruction " + k + "\n"
        "\n"
    )
    sHelp += sh.getFunctionDoc(v, True, "\n")

with open("../docs/server/protocol.md", "w") as text_file:
    text_file.write(sHelp)

