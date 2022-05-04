import requests
import os

from utils.cosmetics import cprint

from utils.config import CONFIG

# Move this to main console.py prob
# CONFIG = Yaml(os.getcwd() + "/src/config.yml")
# CONFIG.loadConfig()

def download(link, name=None, return_json=False, no_download=False):
    '''
    Downloads a file form the internet using the basic-installer.sh script
    More details about this script in the file itself
    '''

    wd = chdir(CONFIG.get("DOWNLOAD_CACHE"))
    data = requests.get(link)

    if not no_download:
        if name == None:
            name = link.split('/')[-1] 
        
        with open(name, 'wb') as f:
            f.write(data.content)
        os.chdir(wd)

    if data.status_code == 404:
        raise Exception(link, data.status_code, data.reason)

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


from utils.config import PATH_TO_CONFIG_FILE

def fetch_servers() -> list:    
    serverloc = CONFIG.get("SERVER_DIRECTORY")

    servers = []

    if not os.path.exists(serverloc):
        cprint(f'''
            &cYou don't have any servers yet create servers using 
            the server creator or change the paths in the config,yml
            your config location is: {PATH_TO_CONFIG_FILE}''')
    return os.listdir(serverloc)