import dbus

# http://stackp.online.fr/?p=35

SERVER_INVALID, SERVER_REGISTERING, SERVER_RUNNING, SERVER_COLLISION, SERVER_FAILURE = range(0, 5)

ENTRY_GROUP_UNCOMMITED, ENTRY_GROUP_REGISTERING, ENTRY_GROUP_ESTABLISHED, ENTRY_GROUP_COLLISION, ENTRY_GROUP_FAILURE = range(0, 5)

DOMAIN_BROWSER_BROWSE, DOMAIN_BROWSER_BROWSE_DEFAULT, DOMAIN_BROWSER_REGISTER, DOMAIN_BROWSER_REGISTER_DEFAULT, DOMAIN_BROWSER_BROWSE_LEGACY = range(0, 5)

PROTO_UNSPEC, PROTO_INET, PROTO_INET6  = -1, 0, 1

IF_UNSPEC = -1

PUBLISH_UNIQUE = 1
PUBLISH_NO_PROBE = 2
PUBLISH_NO_ANNOUNCE = 4
PUBLISH_ALLOW_MULTIPLE = 8
PUBLISH_NO_REVERSE = 16
PUBLISH_NO_COOKIE = 32
PUBLISH_UPDATE = 64
PUBLISH_USE_WIDE_AREA = 128
PUBLISH_USE_MULTICAST = 256

LOOKUP_USE_WIDE_AREA = 1
LOOKUP_USE_MULTICAST = 2
LOOKUP_NO_TXT = 4
LOOKUP_NO_ADDRESS = 8

LOOKUP_RESULT_CACHED = 1
LOOKUP_RESULT_WIDE_AREA = 2
LOOKUP_RESULT_MULTICAST = 4
LOOKUP_RESULT_LOCAL = 8
LOOKUP_RESULT_OUR_OWN = 16
LOOKUP_RESULT_STATIC = 32

SERVICE_COOKIE = "org.freedesktop.cookie"
SERVICE_COOKIE_INVALID = 0

DBUS_NAME = "org.freedesktop.Avahi"
DBUS_INTERFACE_SERVER = DBUS_NAME + ".Server"
DBUS_PATH_SERVER = "/"
DBUS_INTERFACE_ENTRY_GROUP = DBUS_NAME + ".EntryGroup"
DBUS_INTERFACE_DOMAIN_BROWSER = DBUS_NAME + ".DomainBrowser"
DBUS_INTERFACE_SERVICE_TYPE_BROWSER = DBUS_NAME + ".ServiceTypeBrowser"
DBUS_INTERFACE_SERVICE_BROWSER = DBUS_NAME + ".ServiceBrowser"
DBUS_INTERFACE_ADDRESS_RESOLVER = DBUS_NAME + ".AddressResolver"
DBUS_INTERFACE_HOST_NAME_RESOLVER = DBUS_NAME + ".HostNameResolver"
DBUS_INTERFACE_SERVICE_RESOLVER = DBUS_NAME + ".ServiceResolver"
DBUS_INTERFACE_RECORD_BROWSER = DBUS_NAME + ".RecordBrowser"




class ZeroconfService:
    def __init__(self, name, port, stype="_http._tcp",
                 domain="", host="", text=""):
        self.name = name
        self.stype = stype
        self.domain = domain
        self.host = host
        self.port = port
        self.text = text

    def publish(self):
        bus = dbus.SystemBus()
        server = dbus.Interface(
                         bus.get_object(
                                 DBUS_NAME,
                                 DBUS_PATH_SERVER),
                        DBUS_INTERFACE_SERVER)

        g = dbus.Interface(
                    bus.get_object(DBUS_NAME,
                                   server.EntryGroupNew()),
                    DBUS_INTERFACE_ENTRY_GROUP)

        g.AddService(IF_UNSPEC, PROTO_UNSPEC,dbus.UInt32(0),
                     self.name, self.stype, self.domain, self.host,
                     dbus.UInt16(self.port), self.text)

        g.Commit()
        self.group = g

    def unpublish(self):
        self.group.Reset()


zeroconf_service = ZeroconfService("Marvin", 9042, "_marvin._tcp")


def register_service():
    global zeroconf_service
    zeroconf_service.publish()


def unpublish_service():
    global zeroconf_service
    zeroconf_service.unpuslish()
