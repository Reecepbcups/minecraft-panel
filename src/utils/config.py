# May be easier to just put all config locations in here to reduce complexity of config.yml having some & here having 1.

PATH_TO_CONFIG_FILE = "/root/minecraft-panel/config.yml"

from utils.yaml import Yaml
CONFIG = Yaml(PATH_TO_CONFIG_FILE).loadConfig()