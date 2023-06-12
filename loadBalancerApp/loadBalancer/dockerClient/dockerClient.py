import docker
import yaml

from yaml.loader import SafeLoader
from loadBalancer.common import logger
from docker.errors import APIError

# Data stucture that represent video server configuration
class videoServer:
    def __init__(self, config, client):
        self.config = config
        self.client = client

    def __readConfig(self):
        videoServerConfig = self.config.get('videoserver')
        
        self.image = videoServerConfig.get('image')
        self.networks = videoServerConfig.get('networks')
        self.env = videoServerConfig.get('environment')

        volumes = videoServerConfig.get('volumes')[0]
        self.mounts = ["{0}:{1}:ro".format(volumes.get('source'), volumes.get('target'))]

    def replicate(self, node: str):
        self.__readConfig()

        nodePlacement = ["node.id == {}".format(node)]
        service_spec = {
            'image' : self.image, 
            'networks' : self.networks, 
            'env' : self.env, 
            'mounts' : self.mounts,
            'constraints' : nodePlacement
        }
        try:
            service = self.client.services.create(**service_spec)
            serviceObject = self.client.services.get(service.id)
            
        except Exception:
            logger._LOGGER.error("Can't perform docker service operation")
            return None, None
        return serviceObject, serviceObject.name

class dockerClient:
    #serverAddr='host.docker.internal:2375'
    #configDir='loadBalancer/dockerClient/config/videoServer.yaml'
    def __init__(self, serverAddr, configDir) -> None:
        self.client = docker.DockerClient(base_url=serverAddr)
        self.configDir = configDir
        self.serviceDict = {}
 
    def createService(self, node:str, service:str) -> str:
        with open(self.configDir + service + '.yaml') as f:
            if f is None:
                logger._LOGGER.error("Can't open file")
                return None
            config = yaml.load(f, Loader=SafeLoader)
        match service:
            case 'videoServer':
                video_service = videoServer(config, self.client)
                service, serviceName = video_service.replicate(node=node)
                if service is None and serviceName is None:
                    return None
                
        self.__saveIdentifications(name=serviceName, object=service)
        return serviceName    

    def __saveIdentifications(self, object, name:str):
        self.serviceDict[name] = object

    def removeService(self, serviceName:str) -> bool: 
        service = self.serviceDict[serviceName]
        if service is None:
            logger._LOGGER.error("Cant retrieve service from service name")
            return False
        try:
            service.remove()
        except APIError:
            logger._LOGGER.error("Cant remove this service, this is a server error")
            return False
        return True

    def getNodeList(self):
        nodeObjectList = self.client.nodes.list(filters={'role': 'worker'})
        nodeList = []

        for node in nodeObjectList:
            nodeList.append(node.id)
        return nodeList
    


