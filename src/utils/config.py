PATH_TO_CONFIG_FILE = "/root/minecraft-panel/config.yml"

from utils.yaml import Yaml
CONFIG = Yaml(PATH_TO_CONFIG_FILE).loadConfig()