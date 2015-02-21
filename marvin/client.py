import dbus
from daemon.tracking import JobStuct


__all__ = ['connect']


def connect():
    bus = dbus.SessionBus()
    obj = bus.get_object('ua.douhack.marvin', '/ua/douhack/marvin')
    client = dbus.Interface(obj, 'ua.douhack.marvin')
    return client


def job_struct_from_tuple(data):
    return JobStuct(
        id=data[0],
        path=data[1],
        total=data[2],
        sent=data[3],
        status=data[4]
    )
