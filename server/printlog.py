def printlog(s, bMicro = False, sep = ": "):
    """
    Print message with date and time and flush the console
    @see https://www.turnkeylinux.org/blog/unix-buffering
    """
    from datetime import datetime
    import sys
    if bMicro: 
        sMicro = ",%f"
    else:
        sMicro = ""
    print(datetime.now().strftime("%Y/%m/%d %H:%M:%S" + sMicro) + sep + s)
    sys.stdout.flush()
