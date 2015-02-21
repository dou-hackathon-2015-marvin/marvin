import os
import dbus
from gi.repository import Nautilus, GObject


class ColumnExtension(GObject.GObject, Nautilus.MenuProvider):
    def __init__(self):
        pass

    def send_file(self, menu, file, target):
        filename = file.get_name()
        os.system('notify-send "Sending {} to {}"'.format(filename, target))

        bus = dbus.SessionBus()
        obj = bus.get_object('ua.douhack.marvin', '/ua/douhack/marvin')
        server = dbus.Interface(obj, 'ua.douhack.marvin')

        server.send_file(filename, target)
        print('Sending file:', filename)

    def get_file_items(self, window, files):
        ips = ['192.168.0.1', '192.168.0.2', '192.168.0.2']
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
            ip_item.connect('activate', self.send_file, files[0], ip)
            submenu.append_item(ip_item)

        return [item]
