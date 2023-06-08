import  unittest
from loadBalancer.dockerClient.dockerClient import dockerClient

class dockerClientTest(unittest.TestCase):
    def setUp(self) -> None:
        self.dockerClient = dockerClient('192.168.56.20:2375', 'loadBalancer/dockerClient/config/')

    def testCreateVideoServer(self):
        output = self.dockerClient.createService(node='3sy2t6skhgpcle5c94sou3tj0', service='videoServer')
        self.assertIsNotNone(output)
if __name__ == '__main__':
    unittest.main()