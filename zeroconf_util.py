from marvin.daemon import zeroconf_publisher

from gi.repository import GLib


if __name__ == '__main__':
    zeroconf_publisher.register_service()
    print("Published")
    loop = GLib.MainLoop()
    try:
        loop.run()
    finally:
        zeroconf_publisher.unpublish_service()
        print("Unpublished")
