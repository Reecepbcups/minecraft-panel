from utils.cosmetics import color, cfiglet, cprint, color_dict, cinput
import pyfiglet, time, os
from utils.screen import is_screen_running
# from utils.file_utils import fetch_servers
from utils.file import CONFIG, chdir, download
import shutil, requests
from utils.system import get_time, getPublicIPAddress

def paper_install():
    '''
    Downloads Paper spigot or Waterfall Proxy
    '''
    PAPER_LINK = "https://papermc.io/api/v2/projects/{project}"
    PAPER_V2_API_VERSION = "https://papermc.io/api/v2/projects/{project}/versions/{version}"
    PAPER_V2_API = "https://papermc.io/api/v2/projects/{project}/versions/{version}/builds/{build}/downloads/{download}"

    project = cinput("&3Server Type [waterfall, (paper)]>> ") or "paper"
    if project not in ['waterfall', 'paper']:
        if project in ["None", "exit"]:
            return
        cprint(f"&4Invalid server type: {project}")
        paper_install()

    # make a get request to PAPER_LINK
    jsonReply = requests.get(PAPER_LINK.format(project=project)).json()
    versionGroupString = ', '.join(jsonReply['versions'])

    cprint("&a\nVersions you can use:\n" + versionGroupString)

    latest = versionGroupString.split(', ')[-1]
    version = cinput(f"&3Server Version ({latest})>> ") or latest
    if version not in versionGroupString:
        if project in ["None", "exit"]:
            return
        cprint(f"&4Invalid version: {version}. Try again...")
        paper_install()
    
    
    try: # Download the jar file
        start = time.time()
        paper_version = PAPER_V2_API_VERSION.format(project=project, version=version)
        
        _, json_response = download(paper_version, return_json=True, no_download=True) #;print(json_response)

        build = str(json_response["builds"][len(json_response["builds"])-1])

        jarName = project+"-"+version+"-"+build+".jar"
        download_url = PAPER_V2_API.format(project=project, version=version, build=build, download=jarName)
        cprint(f'&eDownloading {project}:{version}:{build} from {download_url}')
        download(download_url)
        end = time.time()
        cprint(f'&aInstalled {project}:{version}:{build} from {download_url} in {round(end-start, 3)} seconds')
        return download_url.split('/')[-1]
    except Exception as e:
        print(e)


nameToID = { # Spigot IDS from url. Uses spiget API to get
    "BungeeServerManager": 7388,
    "ServerTools": 95853,
    "Plugman": 88135,
    "Luckperms": 28140,
    "Vault": 34315,
    "ProtocolLib": 1997,
}
IDtoName = {v: k for k, v in nameToID.items()}

# TODO: Break this up into chunks
class ServerCreator():
    # move inputs into console.py
    # cprint("&3Server Installer! (Press enter to accept the default value)")

    def __init__(self, server_name):
        SERVER_NAME = cinput("&bServer Name: ") or ("myServer-" + get_time())

        server_loc = CONFIG.get("SERVER_DIRECTORY")
        if not os.path.exists(server_loc):
            os.mkdir(server_loc)
        server_path = f'{server_loc}/{SERVER_NAME}'
        if os.path.exists(server_path):
            cprint(f"&cThis is already a server {server_path=}")
            exit(1) 

        # Add config check where if serverloc is not found, it will ask the user for the location of servers & make config
        jarName = paper_install()
        file_path = f'{CONFIG.get("DOWNLOAD_CACHE")}/{jarName}'

        os.mkdir(server_path)
        shutil.move(file_path, server_path)


        # other inputs
        RAM = cinput("&3Ram amount: [500M/(2G) etc...] >> ") or "2G"
        JAR_NAME=f"{jarName}"

        # Start file creation
        startFile = f'''#!/bin/sh
        # Reecepbcups - start.sh script for servers. EULA Auto Accepted.
                    
        MEM_HEAP="{RAM}"
        JAR_FILE="{JAR_NAME}"

        '''

        # If RAM usage is >12GB, optomized java arguments are used
        if 'g' in RAM.lower() and int(''.join(filter(str.isdigit, RAM))) > 12: # remove all letters from RAM, so its only the #    
            startFile += 'JAVA_ARGS="-Dfile.encoding=utf-8 -XX:+UnlockExperimentalVMOptions -XX:G1NewSizePercent=40 -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:-OmitStackTraceInFastThrow -XX:+AlwaysPreTouch  -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=50 -XX:G1HeapRegionSize=16M -XX:G1ReservePercent=15 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=8 -XX:InitiatingHeapOccupancyPercent=20 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=true -Daikars.new.flags=true -Dcom.mojang.eula.agree=true"'
        else:
            startFile += 'JAVA_ARGS="-Dfile.encoding=utf-8 -Dcom.mojang.eula.agree=true"'

        startFile += f'''

        while true; do
            java -Xms$MEM_HEAP -Xmx$MEM_HEAP $JAVA_ARGS -jar $JAR_FILE nogui
            echo "Restarting server in 5 seconds"
            sleep 4
            echo "Restarting..."
            sleep 1
        done'''

        # print(startFile)

        # write startFile to test.sh
        with open(server_path+'/start.sh', 'w') as file:
            file.write(startFile)
        print("start.sh file made")

        os.system(f"chmod +x {server_path}/start.sh")

        # spigot.yml
        with open(server_path+"/spigot.yml", "a") as file:
            isBehindBungee = cinput("&3Behind Bungee? [(true)/false] >> ") or "true"
            file.write(f"""settings:
            bungeecord: {isBehindBungee}
            restart-on-crash: false"""
            )

        # server.properties
        with open(server_path+"/server.properties", "a") as file:
            # Add check to ensure port can not be set if another one uses it
            port = int(cinput("&3Port: [(25565)] >> ") or 25565)
            allow_nether = cinput("&3Allow Nether [(true)/false]>> ") or "true"
            max_players = cinput("&3Max Players (200) >> ") or "200"
            view_distance = cinput("&3View Distance (8)>> ") or "8"
            file.write(f"server-port={str(port)}\n")
            file.write(f"allow-nether={allow_nether}\n")
            file.write(f"max-players={max_players}\n")
            file.write(f"view-distance={view_distance}\n")

            if isBehindBungee == "true":
                file.write("network-compression-threshold=-1")
                file.write("online-mode=false")
            else:
                file.write("online-mode=true")
                file.write("network-compression-threshold=256")

            # use-native-transport=false if you get spam for unable to access address of buffer

        cprint(f"&aServer created at {server_path=}")

        # ask if we should add to config? default yes
        # change terminal to server_path and exit
        os.chdir(server_path)
        os.mkdir("logs")
        os.mkdir("plugins")

        
        # Ask user if they want to preisntall some plugins
        installPlugins = cinput("&3Install common plugins? ( yes / (no) )> ") or 'no'
        if installPlugins.lower() == 'yes':
            self.installPluginPanel()

        # Send command to hook into proxy
        if isBehindBungee == "true":
            cprint(f"&aAdd {server_name} to the BungeeCord proxy with the command:")
            cprint(f"&a'svm server add {server_name} 127.0.0.1:{port}'")
        else:
            cprint(f"&aYour server is now live at: 127.0.0.1:{port} OR {getPublicIPAddress()}")

    def installPluginPanel(self):
        for idx, name, id in enumerate(nameToID):
            print(f"{idx+1}. {name} ({id})")




# import requests
def downloadResourceFromSpigot(resourceID, folderPath=os.getcwd()):
    url = f"https://api.spiget.org/v2/resources/{resourceID}/download"

    response = requests.get(url)

    pluginName = IDtoName[resourceID]
    jarName = f"{folderPath}/{pluginName}.jar"

    with open(jarName, "wb") as jar:
        jar.write(response.content)

    print(f"Downloaded {pluginName} to {jarName}")

if __name__ == "__main__":
    # TEst dwnload
    downloadResourceFromSpigot(95853)

def writeToDefaultConfig():
    luckpermsConfig = f"""
    Put values here which are in the luckperms config, then you can easily make them.
    Ensure when the server starts with these values predefined it works as expected.
    Database, username, password, server type, etc.
    """

