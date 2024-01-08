import sys
from .server.main import start as start_server
from .thread.main import start as start_thred


def start() -> None:
    if len(sys.argv) == 1:
        start_server()
    else:
        start_thred(sys.argv[1])
