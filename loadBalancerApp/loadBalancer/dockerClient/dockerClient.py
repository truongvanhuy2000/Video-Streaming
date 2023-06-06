import docker
import yaml
from yaml.loader import SafeLoader

class dockerClient:
    def __init__(self) -> None:
        self.client = docker.DockerClient(base_url='host.docker.internal:2375')
        with open('loadBalancer/dockerClient/config/videoServer.yaml') as f:
            self.config = yaml.load(f, Loader=SafeLoader)
            print(self.config)

    def createVideoServer(self, node):
        videoServerConfig = self.config.get('videoserver')
        image = videoServerConfig.get('image')
        networks = videoServerConfig.get('networks')
        privileges = videoServerConfig.get('privileged')
        env = videoServerConfig.get('env')
        volumes = videoServerConfig.get('volumes')

        mounts = mounts = ["{0}:{1}:rw".format(volumes.get('source'), volumes.get('target'))]
        constraints = ["node == {}".format(node)]

        service = self.client.services.create(image=image, networks=networks, privileges=privileges, env=env, constraints=constraints, mounts=mounts)
        