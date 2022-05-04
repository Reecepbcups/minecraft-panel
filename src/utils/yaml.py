import yaml

def getYaml(self):
    with open(self.path, 'r') as file:
        return yaml.safe_load(file)

class Yaml():
    '''
    A Yaml class to do Yaml things

    pathToConfig = self.path + "/config.yml"
    proxyConfig = Yaml(pathToConfig).loadConfig().getConfig()
    for key in proxyConfig.keys():
        self.values[key] = proxyConfig[key]
    '''


    def __init__(self, path):
        self.path: str = path
        self.config = None # This yaml object
 
    def loadConfig(self): # returns self object
        with open(self.path, 'r') as file:
            self.config = yaml.safe_load(file)
            if self.config == None:
                self.config = {}
            return self

    def getConfig(self):
        return self.config
    
    def set(self, key, value):
        self.config[key] = value
    
    def get(self, key):
        if key in self.config:
            return self.config[key]
        
        print(f"{key} not found in config from: {self.path}")
        return []

    def keys(self):
        return self.config.keys()

    def save(self):
        with open(self.path, 'w') as file:
            yaml.dump(self.config, file, sort_keys=False)


