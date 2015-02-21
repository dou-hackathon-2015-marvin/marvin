from collections import namedtuple
import logging
import threading

import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GObject, GLib
from .internode_client import InternodeClient
from . import transmit_tracking


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
    def ping_thrift(self, host, port):
        i_client = InternodeClient(host, port)
        return i_client.ping()

    @dbus.service.method('ua.douhack.marvin')
    def list_sending(self):
        return dbus.Array(transmit_tracking.get_sending_jobs(), signature=dbus.Signature('(ssnnn)'))

    @dbus.service.method('ua.douhack.marvin')
    def send_file(self, filename, target_host, target_port):
        logging.debug("send file '{}' to {}:{}".format(filename, target_host, target_port))
        return transmit_tracking.send_file(str(filename), target_host, target_port)

    @dbus.service.method('ua.douhack.marvin')
    def info(self, fid):
        return transmit_tracking.get_job(fid)

    @dbus.service.method('ua.douhack.marvin')
    def hist(self):
        s = transmit_tracking.get_jobs()
        return dbus.Array(s, signature=dbus.Signature('(ssnnn)'))

    @dbus.service.method('ua.douhack.marvin')
    def discover(self):
        return ['192.168.0.1', '192.168.0.2', '192.168.0.3', '192.168.0.4']


class GLibLoopThread(threading.Thread):
    def __init__(self, stop_callback, *args, **kwargs):
        super(GLibLoopThread, self).__init__(*args, **kwargs)
        self.stop_callback = stop_callback
        self.loop = None

    def run(self):
        logging.info("Starting DBUS Server")
        self.loop = GLib.MainLoop()
        try:
            self.loop.run()
        except KeyboardInterrupt:
            if self.stop_callback:
                self.stop_callback()
        finally:
            logging.info("Stopped GLib MainLoop")


def start_localserver(stop_callback):
    global dbus_service, glib_thread
    dbus_service = MarvinDBUSService()
    glib_thread = GLibLoopThread(stop_callback)
    glib_thread.start()
