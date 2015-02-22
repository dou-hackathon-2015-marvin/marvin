from . import zeroconf_publisher
import os
import sys

sys.path.append(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '../thrift/gen-py'))


import logging
import threading

from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from thrift.transport import TSocket, TTransport

from Marvin import MarvinService

from .receive_tracking import initiate_transfer, append_chunk, finish_sending


class MarvinThriftHandler(object):
    def say_hello(self):
        return "saying hello"

    def say_echo(self, s):
        return s

    def send_file_request(self, filename, job_id, size):
        logging.info("SEND FILE REQUEST [{}] {}".format(job_id, filename))
        initiate_transfer(job_id, filename, size)
        return True

    def send_chunk(self, job_id, chunk):
        logging.info("DATA CHUNK RECEIVED FOR {}".format(job_id))
        append_chunk(job_id, chunk)

    def finish_sending(self, job_id):
        logging.info("FINISHED RECEIVING {}".format(job_id))
        finish_sending(job_id)


class ThriftServiceThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(ThriftServiceThread, self).__init__(*args, **kwargs)
        self.server = None

    def run(self):
        handler = MarvinThriftHandler()
        processor = MarvinService.Processor(handler)

        transport = TSocket.TServerSocket(port=9042)
        transport_factory = TTransport.TBufferedTransportFactory()
        protocol_factory = TBinaryProtocol.TBinaryProtocolFactory()

        self.server = TServer.TThreadedServer(processor, transport, transport_factory, protocol_factory)

        logging.info('Starting Thrift server...')
        try:
            self.server.serve()
        except KeyboardInterrupt:
            pass
        finally:
            logging.info("Stopped")


def start_internode_server():
    global service
    service = ThriftServiceThread()
    service.start()


def stop_internode_server():
    service.server.stop()
