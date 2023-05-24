import json

class persistentData:
    def __init__(self, dir) -> None:
        self.fileDir = dir

    def isEmpty(self) -> bool:
        try:
            with open(self.fileDir, 'r') as file:
                data = json.load(file)
                if not data:
                    print("The JSON file is empty.")
                    return True
                else:
                    print("The JSON file is not empty.")
                    return False
        except:
            return True
        
    def readData(self, name):
        with open(self.fileDir, 'r') as file:
            data = json.load(file)
            if name in data:
                return data[name]
            
            if name == 'model':
                return 'generic'
            elif name == 'view':
                return 2
        
    def writeData(self, data):
        with open(self.fileDir, 'w') as file:
            json.dump(data, file)