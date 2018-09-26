from datetime import datetime
import sys

def printlog(s, bMilliseconds = False, sep = ": "):
    """
    Print message with date and time and flush the console
    @see https://www.turnkeylinux.org/blog/unix-buffering
    """
    if bMilliseconds:
        sDateTime = datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f")[:-3]
    else:
        sDateTime = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    print(sDateTime + sep + s)

    sys.stdout.flush()
