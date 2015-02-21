import os
import sys

import logging
from localapi import start_localserver


sys.path.append(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '../thrift/gen-py'))

from Marvin.MarvinService import Client


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    start_localserver()
    print("some code here")
