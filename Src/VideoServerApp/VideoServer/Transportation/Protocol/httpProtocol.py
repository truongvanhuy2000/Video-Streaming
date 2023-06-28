from VideoServer.Transportation.Protocol.abstractProtocol import abstractProtocol
from VideoServer.common.logger import _LOGGER

from http import client

import json

class httpProtocol(abstractProtocol):
    def __init__(self, host:str, port) -> None:
        self.client = client.HTTPConnection(host, port, timeout=5)

    def request(self, data):
        headers = {
            'Content-Type': 'application/json'
        }
        payload = data
        method = 'POST'
        url = ''

        self.client.request(method=method, headers=headers, url=url, body=payload)
        try:
            response = self.client.getresponse()
            if response.status == 200:
                _LOGGER.debug(f"Request successfully")
            else:
                _LOGGER.error("Request error")
                return None
            
            return json.load(response)
        except Exception as e:
            _LOGGER.warning(f"Exception occur: {e}")

        finally:
            self.close()

        return None

    def close(self):
        self.client.close()