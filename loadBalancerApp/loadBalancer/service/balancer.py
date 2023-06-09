from loadBalancer.dockerClient.dockerClient import dockerClient
from loadBalancer.common import logger
from queue import Queue

import itertools
import threading
import socket
import selectors

_PORT_ = 7654

class Node:
    def __init__(self, nodeId, ) -> None:
        self.nodeId = nodeId
        self.serviceCount = 0
        self.serviceList = {}

    def addNewService(self, client, service):
        self.serviceCount += 1
        self.serviceList[client] = service

    def removeService(self, client, service):
        try:
            self.serviceList.pop(client)
        except KeyError:
            logger._LOGGER.error("No item like this exist")
            return 
        self.serviceCount -= 1

class loadBalancer:
    def __init__(self) -> None:
        self.docker_client = dockerClient(serverAddr='host.docker.internal:2375', configDir='loadBalancer/dockerClient/config/')
        self.connectionHash = {}
        self.nodeList = []
        for nodeId in self.docker_client.getNodeList():
            node = Node(nodeId)
            self.nodeList.append(node)

        self.iter = itertools.cycle(self.nodeList)
        self.connectionQueue = Queue(maxsize = 100)
        self.rlock = threading.RLock

    def __addNewConnection(self, connection):
        # searching for appropriate node
        node = self.__balancingAlgorithm("basic")
        # put node object and connection string to a hash map
        self.connectionHash[connection] = node
        serviceName = self.docker_client.createService(node.nodeId, "videoServer")
        node.addNewService(client=connection, service=serviceName)
        return serviceName
    
    def __removeConnection(self, connection):
        try:
            node = self.connectionHash[connection]
        except KeyError:
            logger._LOGGER.error("No key like this exist")
            return
        node.removeService()
        self.connectionHash.pop(connection)

    def __balancingAlgorithm(self, algorithm) -> Node:
        chosenOne = None
        match algorithm:
            case "basic":
                chosenOne = self.__basicBalancingAlgorithm(self)
                pass
            case "roundRobin":
                chosenOne = self.__roundRobinAlgorithm(self)
                pass
            case "leastConnection":
                pass
        return chosenOne
    
    def __basicBalancingAlgorithm(self):
        for node in self.nodeList:
            if node.serviceCount < 10:
                return node
    
    def __roundRobinAlgorithm(self):
        node = next(self.iter)
        return node
    def __balancing(self):
        self.rlock.acquire()
        sock, request = self.connectionQueue.get()
        self.rlock.release()

    def __tcpCommunication(self):
        sel = selectors.DefaultSelector()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', _PORT_))
            logger._LOGGER.info(f"Thread is listening on {_PORT_}")
            s.listen()
            s.setblocking(False)
            # Registers the socket to be monitored with sel.select() 
            sel.register(s, selectors.EVENT_READ)
            while True:
                events = sel.select(timeout=None)
                for key, mask in events:
                    if key.data is None:
                        self.__acceptConnection(key.fileobj, sel)
                    else:
                        self.__serveConnection(key, mask)

    def __acceptConnection(self, sock:socket.socket, sel):
        conn, addr = sock.accept()
        logger._LOGGER.info(f"Accepted connection from {addr}")
        conn.setblocking(False)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        sel.register(conn, events)

    def __serveConnection(self, key, mask):
        sock = key.fileobj
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024).decode()  # Should be ready to read
            self.rlock.acquire()
            self.connectionQueue.put((sock, recv_data))
            self.rlock.release()

    def serve(self):
        tcpThread = threading.Thread(name="TCP Connection Thread", target=self.__tcpCommunication)
        balanceThread = threading.Thread(name="Balancing Act", target=self.__balancing)

        tcpThread.start()
        balanceThread.start()

        tcpThread.join()
        balanceThread.join()