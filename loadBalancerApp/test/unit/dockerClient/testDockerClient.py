import  unittest
from loadBalancer.dockerClient.dockerClient import dockerClient

class dockerClientTest(unittest.TestCase):
    def setUp(self) -> None:
        self.dockerClient = dockerClient('192.168.56.20:2375', 'test/unit/dockerClient/config/videoServer.yaml')

    def testCreateVideoServer(self):
        with self.assertRaises(Exception):
            output = self.dockerClient.createVideoServer('helusms5yiiqyk4elmni8ox4a')

if __name__ == '__main__':
    unittest.main()