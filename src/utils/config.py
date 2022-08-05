# May be easier to just put all config locations in here to reduce complexity of config.yml having some & here having 1.
import json
import os
from os.path import dirname as parentDir

PATH_TO_CONFIG_FILE = "/home/reece/Desktop/minecraft-panel/config.yml"

# check if PATH_TO_CONFIG_FILE is real. If not, get current file location & get the parent directories (like: cd ../../)
if not os.path.isfile(PATH_TO_CONFIG_FILE):
    # print(f"Config file not found {PATH_TO_CONFIG_FILE}. Getting default config location")    
    path = os.path.realpath(__file__) # get current directory    
    path = os.path.dirname(path) # get parent directory (src)
    PATH_TO_CONFIG_FILE = os.path.dirname(os.path.dirname(path)) + "/config.json" # get parent directory (minecraft_panel/config.yml)
    print("PATH_TO_CONFIG_FILE=", PATH_TO_CONFIG_FILE)


FILE = f"{parentDir(parentDir(parentDir(__file__)))}/config.json"
try:
    with open(FILE) as f:
        CONFIG = json.load(f)     
        # print(f"Loaded CONFIG with {CONFIG}")
except Exception as e:
    print(f"\nError loading config.json: {e}\nMAKE SURE YOU 'cp config.json.example config.json'")
    CONFIG = {}
    exit(0)  

def saveConfig():
    with open(FILE, 'w') as f:
        json.dump(CONFIG, f, indent=4)

'''
from utils.config import CONFIG

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
