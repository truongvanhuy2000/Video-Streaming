from videoServer.transportation import protocolProvider
import os
import socket

import multiprocessing


_PROCESS_COUNT = multiprocessing.cpu_count()
_PORT_ = 9876

def startSocket():
    """Find and reserve a port for all subprocesses to use."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    if sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT) == 0:
        raise RuntimeError("Failed to set SO_REUSEPORT.")
    sock.bind(('', _PORT_))
    print(f"The server is listening on address: {sock.getsockname()[0]}:{sock.getsockname()[1]}")
    return sock.getsockname()[1]

def run():
    protocolType = os.getenv('TRANSPORT_METHOD')
    if protocolType == None:
        print("No env variable for protocol type")
        exit()
    port = startSocket()
    bind_address = '0.0.0.0:{}'.format(port)

    workers = []
    for _ in range(_PROCESS_COUNT):
        protocolServer = protocolProvider.getProtocol(protocolType)
        worker = multiprocessing.Process(target=protocolServer.serve,
                                            args=(bind_address,))
        worker.start()
        workers.append(worker)
    for worker in workers:
        worker.join()
