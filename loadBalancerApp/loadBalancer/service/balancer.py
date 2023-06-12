from loadBalancer.dockerClient.dockerClient import dockerClient
from loadBalancer.common import logger

import queue
import itertools
import threading
import socket
import selectors
import os

_PORT_ = int(os.getenv('PORT'))
SERVER_ADDRESS = os.getenv('DOCKER_DAEMON')
BALANCING_ALGORITHM = os.getenv('BALANCING_ALGORITHM')

if any(var is None for var in [_PORT_, SERVER_ADDRESS, BALANCING_ALGORITHM]):
    print("Missing environment variable")
    exit()

connectionQueue = queue.Queue(maxsize = 100)

class Node():
    def __init__(self, nodeId, docker_client:dockerClient) -> None:
        self.nodeId = nodeId
        self.serviceCount = 0
        self.serviceList = {}
        self.docker_client = docker_client

    def createService(self, connection):
        serviceName = self.docker_client.createService(self.nodeId, "videoServer")
        # Increment the number of service counts
        self.serviceCount += 1
        # Add that service to its corresponding connection
        self.serviceList[connection] = serviceName

        return serviceName

    def removeService(self, client):
        try:
            serviceName = self.serviceList.pop(client)
        except KeyError:
            logger._LOGGER.error("No item like this exist")
            return
        if self.serviceCount > 0:
            self.serviceCount -= 1

        self.docker_client.removeService(serviceName=serviceName)

class loadBalancer():
    def __init__(self) -> None:
        self.connectionHash = {}
        self.nodeList = []
        docker_client = dockerClient(serverAddr=SERVER_ADDRESS, configDir='loadBalancer/dockerClient/config/')

        for nodeId in docker_client.getNodeList():
            node = Node(nodeId, docker_client)
            self.nodeList.append(node)

        self.iter = itertools.cycle(self.nodeList)

    def __addNewConnection(self, connection):
        # searching for appropriate node
        node = self.__balancingAlgorithm(BALANCING_ALGORITHM)
        # put node object and connection string to a hash map
        self.connectionHash[connection] = node
        serviceName = node.createService(connection=connection)
        return serviceName
    
    def __removeConnection(self, connection):
        try:
            node = self.connectionHash[connection]
        except KeyError:
            logger._LOGGER.error("No key like this exist")
            return
        node.removeService(connection)
        self.connectionHash.pop(connection)
        # Close the socket
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

    def tcpCommunication(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', _PORT_))
            s.listen()
            s.setblocking(False)

            logger._LOGGER.info(f"TCP Thread is listening on {_PORT_}")
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