import docker
import yaml
from yaml.loader import SafeLoader
import logging

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
        print(service_spec)
        try:
            service = self.client.services.create(**service_spec)
            serviceAttr = self.client.services.get(service.id)
        except Exception:
            logging.error("Can't perform docker service operation")
            exit()
        return serviceAttr.name

class dockerClient:
    #serverAddr='host.docker.internal:2375'
    #configDir='loadBalancer/dockerClient/config/videoServer.yaml'
    def __init__(self, serverAddr, configDir) -> None:
        self.client = docker.DockerClient(base_url=serverAddr)
        self.configDir = configDir
 
    def createService(self, node:str, service:str):
        with open(self.configDir + service + '.yaml') as f:
            if f is None:
                logging.error("Can't open file")
                return None
            config = yaml.load(f, Loader=SafeLoader)
        match service:
            case 'videoServer':
                video_service = videoServer(config, self.client)
                return video_service.replicate(node=node)


