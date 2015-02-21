import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
import glib

# https://github.com/thp/python-eventfeed/blob/master/eventfeed.py


class MarvinDBUSService(dbus.service.Object):
    def __init__(self):
        dbus_main_loop = DBusGMainLoop(set_as_default=True)
        self.session_bus = dbus.SessionBus(dbus_main_loop)
        self.bus_name = dbus.service.BusName('ua.douhack.marvin', bus=self.session_bus)
        dbus.service.Object.__init__(self, self.bus_name, '/ua/douhack/marvin')

    @dbus.service.method('ua.douhack.marvin')
    def ping(self, str):
        print("PING RECEIVED")
        return str + ": pong"

if __name__ == "__main__":
    loop = glib.MainLoop()
    service = MarvinDBUSService()
    loop.run()
