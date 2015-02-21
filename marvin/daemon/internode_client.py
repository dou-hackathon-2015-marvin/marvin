import os
import sys

sys.path.append(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'thrift/gen-py'))


from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

class InternodeClient(object):
    pass
