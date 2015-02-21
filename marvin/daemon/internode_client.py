import logging
import os
import sys

sys.path.append(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '../thrift/gen-py'))

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

from Marvin.MarvinService import Client


class InternodeClient(object):
    def __init__(self, host, port):
        socket = TSocket.TSocket(host, port)
        self.transport = TTransport.TBufferedTransport(socket)
        protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
        self.client = Client(protocol)
        self.transport.open()
        logging.debug("Thrift transport to {}:{} opened".format(host, port))

    def ping(self):
        return self.client.say_hello()
