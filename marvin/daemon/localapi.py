import logging
import threading

import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import Gtk, GObject, Gdk, GLib


class MarvinDBUSService(dbus.service.Object):
    def __init__(self):
        dbus_main_loop = DBusGMainLoop(set_as_default=True)
        self.session_bus = dbus.SessionBus(dbus_main_loop)
        self.bus_name = dbus.service.BusName('ua.douhack.marvin', bus=self.session_bus)
        dbus.service.Object.__init__(self, self.bus_name, '/ua/douhack/marvin')

    @dbus.service.method('ua.douhack.marvin')
    def echo(self, msg):
        return msg

    @dbus.service.method('ua.douhack.marvin')
    def list_files(self):
        return ['File Name 1', 'File Name 2']

    @dbus.service.method('ua.douhack.marvin')
    def send_file(self, filename, target):
        logging.debug("send file '{}' to {}".format(filename, target))


class GLibLoopThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(GLibLoopThread, self).__init__(*args, **kwargs)
        self.loop = None

    def run(self):
        logging.info("Starting DBUS Server")
        self.loop = GLib.MainLoop()
        try:
            self.loop.run()
        finally:
            logging.info("Stopped")


def start_localclient():
    global dbus_service, glib_thread
    dbus_service = MarvinDBUSService()
    glib_thread = GLibLoopThread()
    glib_thread.start()
