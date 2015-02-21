import os
import dbus
from gi.repository import Nautilus, GObject


class MarvinExtension(GObject.GObject, Nautilus.MenuProvider):
    def __init__(self):
        bus = dbus.SessionBus()
        obj = bus.get_object('ua.douhack.marvin', '/ua/douhack/marvin')
        self.marvin = dbus.Interface(obj, 'ua.douhack.marvin')

    def send_file(self, menu, file, target):
        filename = file.get_uri()
        os.system('notify-send "Sending {} to {}"'.format(filename, target))

        self.marvin.send_file(filename.replace("file://", ""), target, 9042)
        print('Sending file:', filename)

    def get_file_items(self, window, files):
        if len(files) > 1:
            return
        file = files[0]
        ips = self.marvin.discover()
        submenu = Nautilus.Menu()
        item = Nautilus.MenuItem(
            name='MarvinExtension::Send_files',
            label='Send file',
            tip='Send file via network'
        )
        item.set_submenu(submenu)
        for i, ip in enumerate(ips):
            ip_item = Nautilus.MenuItem(name='MarvinExtension::Send{}'.format(i),
                                        label=ip)
            ip_item.connect('activate', self.send_file, file, ip)
            submenu.append_item(ip_item)

        return [item]
