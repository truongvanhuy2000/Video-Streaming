import docker
import yaml
from yaml.loader import SafeLoader
# Data stucture that represent video server configuration
class videoServer:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

class dockerClient:
    #serverAddr='host.docker.internal:2375'
    #configDir='loadBalancer/dockerClient/config/videoServer.yaml'
    def __init__(self, serverAddr, configDir) -> None:
        self.client = docker.DockerClient(base_url=serverAddr)
        with open(configDir) as f:
            self.config = yaml.load(f, Loader=SafeLoader)
 
    def createVideoServer(self, node: str):
        video_server = self.readVideoServerConfig()
        nodePlacement = ["node.id == {}".format(node)]
        try:
            service = self.client.services.create(image=video_server.image, 
                                              networks=video_server.networks, 
                                              env=video_server.env, 
                                              mounts=video_server.mounts,
                                              constraints=nodePlacement)
        except Exception:
            print("Cant create service")
            exit()
        service = self.client.services.get(service.id)
        # Remember to implement code to get service ip address

        # Remember to implement code to get service ip address
        return service.attrs

    def readVideoServerConfig(self):
        videoServerConfig = self.config.get('videoserver')

        image = videoServerConfig.get('image')
        networks = [].append(videoServerConfig.get('networks'))
        env = [].append(videoServerConfig.get('environment'))
        volumes = [].append(videoServerConfig.get('volumes'))
        mounts = [].append("{0}:{1}:ro".format(volumes.get('source'), volumes.get('target')))

        return videoServer(image=image, 
                           networks=networks, 
                           env=env, 
                           volumes=volumes, 
                           mounts=mounts)

        