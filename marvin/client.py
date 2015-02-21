import dbus


__all__ = ['connect']


def connect():
    bus = dbus.SessionBus()
    obj = bus.get_object('ua.douhack.marvin', '/ua/douhack/marvin')
    client = dbus.Interface(obj, 'ua.douhack.marvin')
    return client
