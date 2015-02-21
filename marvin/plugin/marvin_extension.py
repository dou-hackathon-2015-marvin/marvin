from gi.repository import Nautilus, GObject

class ColumnExtension(GObject.GObject, Nautilus.MenuProvider):
    def __init__(self):
        pass

    def send_files(self, menu, files):
        print('Send files:', [f.get_name() for f in files])

    def get_file_items(self, window, files):
        item = Nautilus.MenuItem(
            name='MarvinExtension::Send_files',
            label='Send to...',
            tip='Send file via network'
        )
        item.connect('activate', self.send_files, files)

        return [item]