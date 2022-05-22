# May be easier to just put all config locations in here to reduce complexity of config.yml having some & here having 1.
import os

PATH_TO_CONFIG_FILE = "/home/reece/Desktop/minecraft-panel/config.yml"

# check if PATH_TO_CONFIG_FILE is real. If not, get current file location & get the parent directories (like: cd ../../)
if not os.path.isfile(PATH_TO_CONFIG_FILE):
    # print(f"Config file not found {PATH_TO_CONFIG_FILE}. Getting default config location")    
    path = os.path.realpath(__file__) # get current directory    
    path = os.path.dirname(path) # get parent directory (src)
    PATH_TO_CONFIG_FILE = os.path.dirname(os.path.dirname(path)) + "/config.yml" # get parent directory (minecraft_panel/config.yml)
    print(PATH_TO_CONFIG_FILE)

from utils.yaml import Yaml
CONFIG = Yaml(PATH_TO_CONFIG_FILE).loadConfig()


'''
from utils.config import CONFIG

# ymlConfig = Yaml(PATH_TO_CONFIG_FILE)
if CONFIG.get("Mongo-Authentication") == None:
    CONFIG["Mongo-Authentication"] = {}

auth = CONFIG.get("Mongo-Authentication")
auth[username] = database_name # auth db

CONFIG.set("Mongo-Authentication", auth)
CONFIG.save()
'''


'''
# To set a value nested, do the following:
# For now it only supports down 2 sections
serverGroups = CONFIG.get("servers")
SERVERS = serverGroups['spigot']            
SERVERS.append(SERVER_NAME)
CONFIG.set("servers.spigot", SERVERS)
CONFIG.save()
'''