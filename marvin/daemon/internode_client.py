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

    def send_file_request(self, path, job_id, size):
        return self.client.send_file_request(path, job_id, size)

    def send_chunk(self, job_id, chunk):
        return self.client.send_chunk(job_id, chunk)

    def finish_sending(self, job_id):
        return self.client.finish_sending(job_id)
