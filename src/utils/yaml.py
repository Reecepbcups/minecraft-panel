import yaml

def getYaml(self):
    with open(self.path, 'r') as file:
        return yaml.safe_load(file)

class Yaml():

    def __init__(self, path):
        self.path: str = path
        self.config = None # This yaml object
 
    def loadConfig(self): # returns self object
        with open(self.path, 'r') as file:
            self.config = yaml.safe_load(file)
            if self.config == None:
                self.config = {}
            return self
    
    def set(self, key, value):
        self.config[key] = value
    
    def get(self, key):
        try:
            return self.config[key]
        except Exception:
            return []

    def save(self):
        with open(self.path, 'w') as file:
            yaml.dump(self.config, file, sort_keys=False)