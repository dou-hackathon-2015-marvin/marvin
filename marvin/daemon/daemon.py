import logging
from localapi import start_localclient

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    start_localclient()

    print("some code here")
