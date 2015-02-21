import logging
from .local_api import start_localserver
from .internode_api import start_internode_server, stop_internode_server

def stop_callback():
    print("stop found")
    stop_internode_server()


def start():
    logging.basicConfig(level=logging.DEBUG)
    start_localserver(stop_callback=stop_callback)
    start_internode_server()


if __name__ == "__main__":
    start()
    print("OK")
