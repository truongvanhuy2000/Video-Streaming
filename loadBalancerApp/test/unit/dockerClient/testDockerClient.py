import  unittest
from loadBalancer.dockerClient.dockerClient import dockerClient
import logging
import sys


class dockerClientTest(unittest.TestCase):
    def setUp(self) -> None:
        self.dockerClient = dockerClient('192.168.56.20:2375', 'loadBalancer/dockerClient/config/')

    def testCreateVideoServer(self):
        output = self.dockerClient.createService(node='3sy2t6skhgpcle5c94sou3tj0', service='videoServer')
        self.assertIsNotNone(output)

    def testDeleteVideoServer(self):
        service = self.dockerClient.createService(node='3sy2t6skhgpcle5c94sou3tj0', service='videoServer')
        output = self.dockerClient.removeService(service)
        
        self.assertTrue(output, "this is suppose to be true")
    
    def testNodeList(self):
        nodeList = self.dockerClient.getNodeList()
        self.assertEqual(len(nodeList), 3)
    
    
if __name__ == '__main__':
    unittest.main()