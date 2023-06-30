from WebServer.Transportation.Protocol.abstractProtocol import abstractProtocol
from WebServer.common.logger import _LOGGER
from http import client


class httpProtocol(abstractProtocol):
    def __init__(self, host:str, port:int) -> None:

        if not isinstance(host, str):
            raise TypeError(f"Must provide a bool, not a {type(host)}")
        
        self.client = client.HTTPConnection(host, port, timeout=5)

    def request(self, route, data:str):
        if not isinstance(data, str):
            raise TypeError(f"Must provide a bool, not a {type(data)}")
        
        headers = {
            'Content-Type': 'application/json'
        }
        payload = data
        method = 'POST'
        url = route

        self.client.request(method=method, headers=headers, url=url, body=payload)
        try:
            response = self.client.getresponse()
            if response.status == 200:
                _LOGGER.debug("Request successfully")
            else:
                _LOGGER.error(f"Request error: {response.status}")
                return None
            
            content = response.read()
            return content
        
        except client.HTTPException:
            _LOGGER.error("Probably a timeout")
        finally:
            self.close()

        return None

    def close(self):
        self.client.close()