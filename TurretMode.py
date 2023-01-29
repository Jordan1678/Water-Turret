class TurretMode:
    pass


# This file Shouldn't Even Exist
Mode = "Off"


def mode(*args):
    global Mode
    try:
        Mode = args[0]
    except:
        return Mode


def set_mode(NewMode):
    mode(NewMode)


def get_mode():
    return mode()
