from loadBalancer.dockerClient.dockerClient import dockerClient
from loadBalancer.common import logger

import queue
import itertools
import threading
import socket
import selectors
import os
import types

_PORT_ = 7654
connectionQueue = queue.Queue(maxsize = 100)

class Node():
    def __init__(self, nodeId, ) -> None:
        self.nodeId = nodeId
        self.serviceCount = 0
        self.serviceList = {}

    def addNewService(self, client, service):
        self.serviceCount += 1
        self.serviceList[client] = service

    def removeService(self, client):
        try:
            service = self.serviceList.pop(client)
        except KeyError:
            logger._LOGGER.error("No item like this exist")
            return
        self.serviceCount -= 1
        return service

class loadBalancer():
    def __init__(self) -> None:
        self.docker_client = dockerClient(serverAddr=os.getenv('DOCKER_DAEMON'), configDir='loadBalancer/dockerClient/config/')
        self.connectionHash = {}
        self.nodeList = []
        
        for nodeId in self.docker_client.getNodeList():
            node = Node(nodeId)
            self.nodeList.append(node)

        self.iter = itertools.cycle(self.nodeList)

    def __addNewConnection(self, connection):
        # searching for appropriate node
        node = self.__balancingAlgorithm(os.getenv('BALANCING_ALGORITHM'))
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
        serviceName = node.removeService(connection)
        self.docker_client.removeService(serviceName)
        self.connectionHash.pop(connection)
        connection.close()

    def __balancingAlgorithm(self, algorithm) -> Node:
        chosenOne = None
        match algorithm:
            case "basic":
                chosenOne = self.__basicBalancingAlgorithm()
                pass
            case "roundRobin":
                chosenOne = self.__roundRobinAlgorithm()
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
    
    def balancing(self):
        logger._LOGGER.info("Balancer is working")
        while True:
            sock, request = connectionQueue.get(block=True)
            if request == "CONNECT":
                logger._LOGGER.info(f"{sock.getsockname()} send CONNECT request")
                serviceName = self.__addNewConnection(sock)
                sock.send(serviceName.encode())

            elif request == "CLOSE":
                logger._LOGGER.info(f"{sock.getsockname()} send CLOSE request")
                self.__removeConnection(sock)

    
class tcpCommunication():
    def __init__(self) -> None:
        self.sel = selectors.DefaultSelector()
        pass

    def tcpCommunication(self):
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', _PORT_))
            logger._LOGGER.info(f"TCP Thread is listening on {_PORT_}")
            s.listen()
            s.setblocking(False)
            # Registers the socket to be monitored with sel.select() 
            self.sel.register(s, selectors.EVENT_READ, data=None)
            while True:
                events = self.sel.select(timeout=None)
                for key, mask in events:
                    if key.data is None:
                        self.__acceptConnection(key.fileobj)
                    else:
                        self.__serveConnection(key, mask)

    def __acceptConnection(self, sock:socket.socket):
        conn, addr = sock.accept()

        logger._LOGGER.info(f"Accepted connection from {addr}")
        
        conn.setblocking(False)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = b""
        self.sel.register(conn, events, data=data)

    def __serveConnection(self, key, mask):
        sock = key.fileobj
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024).decode()  # Should be ready to read
            if recv_data:
                connectionQueue.put((sock, recv_data))
                if recv_data == "CLOSE":
                    self.sel.unregister(sock)

def serve():
    tcpThread = threading.Thread(name="TCP Connection Thread", target=tcpCommunication().tcpCommunication)
    balanceThread = threading.Thread(name="Balancing Act", target=loadBalancer().balancing)

    tcpThread.start()
    balanceThread.start()

    tcpThread.join()
    balanceThread.join()