import requests
import time
import os
import re
import subprocess
from utils.yaml_utils import Yaml
from utils.cosmetics import cprint
from utils.panel_utils import FileInstallException

CONFIG = Yaml(os.getcwd() + "/configs/config.yml")
CONFIG.loadConfig()

RUNNING = Yaml(os.getcwd() + "/configs/running.yml")
RUNNING.loadConfig()

def download(link, name=None, return_json=False, no_download=False):
    '''
    Downloads a file form the internet using the basic-installer.sh script
    More details about this script in the file itself
    '''

    wd = chdir(CONFIG.get("downloadloc"))
    data = requests.get(link)

    if not no_download:
        if name == None:
            name = link.split('/')[-1] 
        
        with open(name, 'wb') as f:
            f.write(data.content)
        os.chdir(wd)

    if data.status_code == 404:
        raise FileInstallException(link, data.status_code, data.reason)

    if return_json:
        return data.status_code, data.json()
    
    return data.status_code


def chdir(dir):
    '''
    A better version of os.chdir
    '''
    wd = os.getcwd()
    if not os.path.isdir(dir):
        os.mkdir(dir)
        print(f'created directory at {dir}')
        os.chdir(dir)
    else:
        os.chdir(dir)
    return wd


def gather_plugins() -> list:
    '''
    Gets all plugins from the plugins folder given
    they are properly registerd in the config.yml
    '''
    start = time.time()*1000
    plugins = {}
    if CONFIG.get("plugins") != None:
        for plugin in CONFIG.get("plugins"):
            name = plugin.split("-")
            plugins[name[1]] = name[0] 
    
    end = time.time()*1000
    cprint(f'&aFetched all plugins in {end-start} miliseconds')
    return plugins


def get_screen_pid(name: str):
    server = subprocess.Popen(['screen', '-ls'], stdout=subprocess.PIPE)
    stdout, _ = server.communicate()
    matches = re.search(r'(\d+).%s' % name, stdout.decode("utf-8"), re.MULTILINE)
    if matches:
        pids = matches.group()
        pid = pids.split(".")[0]
        os.kill(int(pid), 9)
        subprocess.Popen(['screen', '-wipe'])
