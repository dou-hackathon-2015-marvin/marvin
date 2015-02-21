import logging
from threading import Thread

import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
import glib


class MarvinDBUSService(dbus.service.Object):
    def __init__(self):
        dbus_main_loop = DBusGMainLoop(set_as_default=True)
        self.session_bus = dbus.SessionBus(dbus_main_loop)
        self.bus_name = dbus.service.BusName('ua.douhack.marvin', bus=self.session_bus)
        dbus.service.Object.__init__(self, self.bus_name, '/ua/douhack/marvin')

    @dbus.service.method('ua.douhack.marvin')
    def echo(self, msg):
        return msg


class DBUSThread(Thread):
    def __init__(self, *args, **kwargs):
        super(DBUSThread, self).__init__(*args, **kwargs)
        self.service = MarvinDBUSService()
        self.loop = None

    def run(self):
        logging.info("Starting DBUS Server")
        self.loop = glib.MainLoop()
        self.loop.run()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    dbus_thread = DBUSThread()
    dbus_thread.start()
    print("some code here")
