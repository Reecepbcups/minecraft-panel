from tracemalloc import start
from xmlrpc.client import Server
from utils.cosmetics import color, cfiglet, cprint, color_dict, cinput
import pyfiglet, time, os
from utils.screen import is_screen_running
# from utils.file_utils import fetch_servers
from utils.file import CONFIG, chdir, download
import shutil, requests
from utils.system import get_time, getPublicIPAddress

from server import Server

from pick import pick

def paper_install():
    '''
    Downloads Paper spigot or Waterfall Proxy
    '''
    PAPER_LINK = "https://papermc.io/api/v2/projects/{project}"
    PAPER_V2_API_VERSION = "https://papermc.io/api/v2/projects/{project}/versions/{version}"
    PAPER_V2_API = "https://papermc.io/api/v2/projects/{project}/versions/{version}/builds/{build}/downloads/{download}"

    project = cinput("&bServer Type &f[waterfall, (paper)]&b>> ") or "paper"
    if project not in ['waterfall', 'paper']:
        if project in ["None", "exit"]:
            return
        cprint(f"&4Invalid server type: {project}")
        paper_install()

    jsonReply = requests.get(PAPER_LINK.format(project=project)).json()
    versionGroupString = ', '.join(jsonReply['versions'])

    cprint("&a\nVersions you can use:\n" + versionGroupString)

    latest = versionGroupString.split(', ')[-1]
    version = cinput(f"&bServer Version &f({latest})&b>> ") or latest
    if version not in versionGroupString:
        if project in ["None", "exit"]:
            return
        cprint(f"&4Invalid version: {version}. Try again...")
        paper_install()
    
    
    try: # Download the jar file
        start = time.time()

        # Download latest build for specified version
        paper_version = PAPER_V2_API_VERSION.format(project=project, version=version)        
        _, json_response = download(paper_version, return_json=True, no_download=True) #;print(json_response)

        build = str(json_response["builds"][len(json_response["builds"])-1])
        print(f"{build}=")

        jarName = project+"-"+version+"-"+build+".jar"

        # check if file
        if os.path.isfile(CONFIG.get("DOWNLOAD_CACHE") + "/" + jarName):
            cprint(f"&aFound {jarName} in cache... Using {jarName} from there")
        else:
            download_url = PAPER_V2_API.format(project=project, version=version, build=build, download=jarName)
            cprint(f'&eDownloading {project}:{version}:{build} from {download_url}')
            download(download_url)

        end = time.time()
        cprint(f'&aInstalled {jarName} in {round(end-start, 3)} seconds')
        # return download_url.split('/')[-1]
        return jarName
    except Exception as e:
        print(e)
        return ""


nameToID = { # Spigot IDS from url. Uses spiget API to get
    "BungeeServerManager (Proxy Only)": 7388,
    "ServerTools": 95853,
    "Plugman": 88135,
    "Luckperms": 28140,
    "Vault": 34315,
    "ProtocolLib": 1997,
}
IDtoName = {v: k for k, v in nameToID.items()}

class ServerCreator():
    # move inputs into console.py
    # cprint("&bServer Installer! (Press enter to accept the default value)")

    def __init__(self):
        cfiglet("&a", "Server Creator", clearScreen=True)

        servers_dir = CONFIG.get("SERVER_DIRECTORY")
        SERVER_NAME, server_path = self.createServerFolder(servers_dir)
        self.server_path = server_path

        # Add config check where if serverloc is not found, it will ask the user for the location of servers & make config
        
        JAR_NAME = self.downloadPaper()
        RAM = cinput("&bRam amount: &f[500M/(4G) etc...] &b>> ") or "4G"

        allow_end = cinput("&bAllow end? &f[(true)/false] &b>> ") or "true" 
        allow_nether = cinput("&bAllow Nether &f[(true)/false]&b>> ") or "true"            
        max_players = cinput("&bMax Players &f(100) &b>> ") or "100"
        view_distance = cinput("&bView Distance &f(8)&b>> ") or "8"
        advancements = cinput("&bEnable Advancements &f[(true)/false]&b>> ") or "true"

        isBehindBungee = cinput("&bBehind Bungee? &f[(true)/false] &b>> ") or "true" 
        port = int(cinput("&bPort: &f(25565) &b>> ") or 25565)

        self.createStartFile(RAM, JAR_NAME)

        # spigot.yml
        with open(server_path+"/spigot.yml", "a") as file:                   
            file.write(f"""settings:\n  bungeecord: {isBehindBungee}\n  restart-on-crash: false\nadvancements:\n    disable-saving: {advancements}""")

        with open(server_path+"/bukkit.yml", "a") as bukkitFile:
            bukkitFile.write(f"""settings:\n  allow-end: {allow_end}""")

        # server.properties
        with open(server_path+"/server.properties", "a") as file:
            # Add check to ensure port can not be set if another one uses it
            file.write(f"server-port={str(port)}\n")
            file.write(f"allow-nether={allow_nether}\n")
            file.write(f"max-players={max_players}\n")
            file.write(f"view-distance={view_distance}\n")

            if isBehindBungee != "true": # standalone server, secure it                
                file.write("online-mode=true\n")
                file.write("network-compression-threshold=256\n")
            else:
                file.write("online-mode=false\n")
                file.write("network-compression-threshold=-1\n")

        os.chdir(server_path)
        os.mkdir("logs"); os.mkdir("plugins")

        # ask if we should add to global config.yml? default yes

        # Ask user if they want to preisntall some plugins
        installPlugins = cinput("&bInstall common plugins? [(yes)/no]> ") or 'yes'
        if installPlugins.lower().startswith('y'):
            self.installPluginsToServer()

        # Send command to hook into proxy
        if isBehindBungee == "true":
            cprint(f"&aAdd {SERVER_NAME} to the BungeeCord proxy with the command:")
            cprint(f"&a'svm server add {SERVER_NAME} 127.0.0.1:{port}'")
        else:
            cprint(f"&aYour server is now live at: 127.0.0.1:{port} OR {getPublicIPAddress()}:{port}")
        cprint(f"&aServer created at {server_path=}")

        doStart = cinput("&bStart server now? [yes/(no)] &b>> ") or "yes"
        s = Server(SERVER_NAME)
        if doStart.lower().startswith('y'):
            s.start_server()

            connect_console = cinput("&bConnect to console of server? [yes/(no)] &b>> ") or "no"
            if connect_console.lower().startswith('y'):
                s.enter_console()

    def createServerFolder(self, servers_dir) -> str:
        defaultName = "myServer-" + get_time()
        SERVER_NAME = cinput(f"&bServer Name &f({defaultName})&b>> ") or defaultName
        if not os.path.exists(servers_dir):
            os.mkdir(servers_dir)
        
        server_path = f'{servers_dir}/{SERVER_NAME}'

        if os.path.exists(server_path):
            cprint(f"&cThis is already a server {server_path=}.\n&aUsing default name {defaultName}")
            SERVER_NAME = defaultName
            server_path = f'{servers_dir}/{SERVER_NAME}'
            
        os.mkdir(server_path)
        return SERVER_NAME, server_path

    def downloadPaper(self) -> str:
        jarName = paper_install() # print(jarName); exit()

        # Moves file from the cache folder -> the server parent folder
        downloadCache = str(CONFIG.get("DOWNLOAD_CACHE"))
        file_path = f'{downloadCache}/{jarName}'
        shutil.copyfile(file_path,f"{self.server_path}/{jarName}")
        return jarName

    def createStartFile(self, RAM, JAR_NAME):
        # Start file creation.
        startFile = f'''#!/bin/sh\n# Reecepbcups - start.sh script for servers. EULA Auto Accepted.\n\nMEM_HEAP="{RAM}"\nJAR_FILE="{JAR_NAME}"\n'''
        # If RAM usage is >12GB, optomized java arguments are used
        if 'g' in RAM.lower() and int(''.join(filter(str.isdigit, RAM))) > 12: # remove all letters from RAM, so its only the #    
            startFile += 'JAVA_ARGS="-Dfile.encoding=utf-8 -XX:+UnlockExperimentalVMOptions -XX:G1NewSizePercent=40 -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:-OmitStackTraceInFastThrow -XX:+AlwaysPreTouch  -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=50 -XX:G1HeapRegionSize=16M -XX:G1ReservePercent=15 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=8 -XX:InitiatingHeapOccupancyPercent=20 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=true -Daikars.new.flags=true -Dcom.mojang.eula.agree=true"'
        else:
            startFile += 'JAVA_ARGS="-Dfile.encoding=utf-8 -Dcom.mojang.eula.agree=true"'

        startFile += f'''\n\nwhile true; do\n\tjava -Xms$MEM_HEAP -Xmx$MEM_HEAP $JAVA_ARGS -jar $JAR_FILE nogui\n\techo "Restarting server in 5 seconds"\n\tsleep 4\n\techo "Restarting..."\n\tsleep 1\ndone'''

        # write startFile to test.sh
        with open(self.server_path+'/start.sh', 'w') as file:
            file.write(startFile)
            # print("start.sh file made")
        os.system(f"chmod +x {self.server_path}/start.sh")
        



    def installPluginsToServer(self):
        title = 'Please choose which plugins you want to download (press SPACE to select, ENTER to continue): '
        options = list(nameToID.keys())
        selected = pick(options, title, indicator=' =>', multiselect=True, min_selection_count=0)
        for name, idx in selected:
            pluginID = nameToID[name]
            cprint(f"&aDownloading {name} ({pluginID})")
            downloadResourceFromSpigot(pluginID, f"{self.server_path}/plugins")




# import requests
def downloadResourceFromSpigot(resourceID, folderPath=os.getcwd(), debug=False):
    url = f"https://api.spiget.org/v2/resources/{resourceID}/download"

    response = requests.get(url)

    pluginName = IDtoName[resourceID]
    jarName = f"{folderPath}/{pluginName}.jar"

    with open(jarName, "wb") as jar:
        jar.write(response.content)

    if debug: print(f"Downloaded {pluginName} to {jarName}")

if __name__ == "__main__":
    # TEst dwnload
    downloadResourceFromSpigot(95853)

def writeToDefaultConfig():
    luckpermsConfig = f"""
    Put values here which are in the luckperms config, then you can easily make them.
    Ensure when the server starts with these values predefined it works as expected.
    Database, username, password, server type, etc.
    """

