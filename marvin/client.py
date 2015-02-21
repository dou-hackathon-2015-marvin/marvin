import dbus


__all__ = ['client']


class Client(object):
    def __init__(self):
        bus = dbus.SessionBus()
        obj = bus.get_object('ua.douhack.marvin', '/ua/douhack/marvin')
        self.server = dbus.Interface(obj, 'ua.douhack.marvin')

    def echo(self, msg):
        return str(self.server.echo())

    def list_files(self):
        return map(str, list(self.server.list_files()))


client = Client()
