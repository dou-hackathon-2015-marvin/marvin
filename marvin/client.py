import dbus
from daemon.tracking import JobStuct


__all__ = ['connect']


def connect():
    return Client()


def struct(func):
    func_name = func.__name__

    def inner(self, *args, **kwargs):
        return to_struct(getattr(self.server, func_name)(*args, **kwargs))
    return inner


def structs(func):
    func_name = func.__name__

    def inner(self, *args, **kwargs):
        return map(to_struct, getattr(self.server, func_name)(*args, **kwargs))
    return inner


class Client(object):
    def __init__(self):
        bus = dbus.SessionBus()
        obj = bus.get_object('ua.douhack.marvin', '/ua/douhack/marvin')
        self.server = dbus.Interface(obj, 'ua.douhack.marvin')

    def __getattr__(self, item):
        getattr(self.server, item)

    @struct
    def info(self):
        pass

    @structs
    def list_sending(self):
        pass

    @structs
    def hist(self):
        pass


def to_struct(data):
    return JobStuct(
        id=data[0],
        path=data[1],
        total=data[2],
        sent=data[3],
        status=data[4]
    )
