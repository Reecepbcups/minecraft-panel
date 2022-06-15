import os
from pickle import FALSE
import shutil
import time
# from xmlrpc.client import Server

import requests
from pick import pick

from panels.firewall_panel import FirewallPanel, Firewall
from server import Server
from utils.config import CONFIG, saveConfig
from utils.cosmetics import cfiglet, cinput, color_dict, cprint
from utils.file import download
from utils.system import get_time, getPublicIPAddress


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

    versionGroups= list(jsonReply['versions'])
    versionGroups.reverse() # so 1.18.2 is on top

    selected = pick(versionGroups, "Pick the version you want to use (Enter to select)", indicator=' =>', multiselect=False)
    version = selected[0]
    
    
    try: # Download the jar file
        start = time.time()

        # Download latest build for specified version
        paper_version = PAPER_V2_API_VERSION.format(project=project, version=version)        
        _, json_response = download(paper_version, return_json=True, no_download=True) #;print(json_response)

        build = str(json_response["builds"][len(json_response["builds"])-1])
        print(f"{build}=")

        jarName = project+"-"+version+"-"+build+".jar"

        # check if file
        if os.path.isfile(CONFIG["DOWNLOAD_CACHE"] + "/" + jarName):
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

# TODO
nameToID = { # Spigot IDS from url. Uses spiget API to get
    # ENSURE TO HAVE 'proxy' in plugins which are only for the proxy
    "BungeeServerManager (proxy)": 7388,
    "BungeePluginManager (proxy)": 7288,

    "SecuredNetwork (proxy & spigot)": 65075,
    "Vault": 34315,
    "ProtocolLib": 1997,

    "ServerTools": 95853, 
    "Luckperms": 28140,           
    "Plugman": 88135,    
        
    "placeholderapi": 6245,
    "Spark": 57242,
    "dynmap": 274,
    "fast-async-worldedit": 13932,
}
IDtoName = {v: k for k, v in nameToID.items()}

# PluginIDs which require others to function
dependencies = {
    65075: [1997], # SecuredNetwork, protocollib
    95853: [34315], # STools, Vault
    28140: [34315], # LPerms, Vault
}
import random as r

class ServerCreator():
    # move inputs into console.py
    # cprint("&bServer Installer! (Press enter to accept the default value)")

    def __init__(self):
        cfiglet("&a", "Server Creator", clearScreen=True)

        servers_dir = CONFIG["SERVER_DIRECTORY"]
        SERVER_NAME, server_path = self.createServerFolder(servers_dir)
        self.server_path = server_path

        # Add config check where if serverloc is not found, it will ask the user for the location of servers & make config
        
        JAR_NAME = self.downloadPaper()        
        

        self.isASpigotServer = False
        if 'paper' in JAR_NAME.lower():
            self.isASpigotServer = True

            rNum = r.randint(30_000, 35_000)
            port = int(cinput(f"&bPort: &f({rNum}) &b>> ") or rNum)
            RAM = cinput("&bRam amount: &f[500M/(4G)] &b>> ") or "4G"
            self.createStartFile(RAM, JAR_NAME)

            allow_end = cinput("&bAllow end? &f[(true)/false] &b>> ") or "true" 
            allow_nether = cinput("&bAllow Nether &f[(true)/false]&b>> ") or "true"            
            max_players = cinput("&bMax Players &f(100) &b>> ") or "100"
            view_distance = cinput("&bView Distance &f(8)&b>> ") or "8"
            advancements = cinput("&bEnable Advancements &f[true/(false)]&b>> ") or "false"
            isBehindBungee = cinput("&bBehind Bungee? &f[(true)/false] &b>> ") or "true"
            # add cprint here to show svm command to run on server?

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
        else:
            port = cinput(f"&bPort: &f(25565) &b>> ") or "25565"
            RAM = cinput("&bRam amount: &f[500M/(1G)] &b>> ") or "1G"
            self.createStartFile(RAM, JAR_NAME)

            open(f"{server_path}/waterfall.yml", "a").close()
            player_limit = cinput("&bPlayer Limit &f(1000) &b>> ") or "1000"
            connection_throttle = cinput("&bconnection_throttle (ms) &f(4000) &b>> ") or "4000"
            remote_ping_timeout = cinput("&bremote_ping_timeout (ms) &f(5000) &b>> ") or "5000"
            server_connect_timeout = cinput("&bserver_connect_timeout (ms) &f(5000) &b>> ") or "5000"
            connection_throttle_limit = cinput("&bconnection_throttle_limit &f(5) &b>> ") or "5"
            network_compression_threshold = cinput("&bnetwork_compression_threshold &f(256) &b>> ") or "256"
            ip_forward = cinput("&bip_forward &f(true) &b>> ") or "true"

            # TODO make a list in the future?
            serverPriority = cinput("&bServer Priority &7[like a hub] &f(lobby) &b>> ") or "lobby"

            serverPriorityAddr = cinput("&bServer Priority Address &f(127.0.0.1:30000) &b>> ") or "127.0.0.1:30000"

            with open(f"{server_path}/config.yml", "a") as conf:                
                conf.write(f"player_limit: {player_limit}\n")
                conf.write(f"remote_ping_timeout: {remote_ping_timeout}\n")
                conf.write(f"connection_throttle: {connection_throttle}\n")
                conf.write(f"server_connect_timeout: {server_connect_timeout}\n")
                conf.write(f"connection_throttle_limit: {connection_throttle_limit}\n")
                conf.write(f"network_compression_threshold: {network_compression_threshold}\n")
                conf.write(f"ip_forward: {ip_forward}\n")
                
                conf.write(f"""listeners:
- host: 0.0.0.0:{port}
  motd: '&bBungeee server from server_creator'
  max_players: {player_limit}
  force_default_server: false
  tab_size: 60
  forced_hosts:
    pvp.md-5.net: pvp
  tab_list: GLOBAL_PING
  bind_local_address: true
  ping_passthrough: false
  query_enabled: false
  query_port: 25577
  proxy_protocol: false
  priorities:
  - {serverPriority}""")
                conf.write(f"""\nservers:
  {serverPriority}:
    motd: ''
    address: {serverPriorityAddr}
    restricted: false""")

        os.chdir(server_path)
        os.mkdir("logs"); os.mkdir("plugins")

        # ask if we should add to global config.yml? default yes
        add_to_config = cinput("&bAdd to global config.yml? &f[(true)/false] &b>> ") or "true"
        if add_to_config == "true":
            serverGroups = CONFIG["servers"]
            
            serverType = 'proxy'
            if 'paper' in JAR_NAME.lower():
                serverType = 'spigot'
            
            SERVERS = serverGroups[serverType]
            if SERVER_NAME not in SERVERS: # Adds server to config if not there
                SERVERS.append(SERVER_NAME)
                # CONFIG[f"servers.{serverType}", SERVERS)
                CONFIG['servers'][f'{serverType}'] = SERVERS
                saveConfig()

        # Ask user if they want to preisntall some plugins
        installPlugins = cinput("\n&bInstall common plugins? &f[(yes)/no] &b>> ") or 'yes'
        if installPlugins.lower().startswith('y'):
            print()
            self.installPluginsToServer(self.isASpigotServer)

        cprint(f"&aServer created at {server_path=}")
        # Send command to hook into proxy
        if 'paper' in JAR_NAME.lower() and isBehindBungee == "true":
            if input("Enable Firewall for this server? ([y]/n)").startswith('y'):
                print("Is firewall enabled", Firewall().isFirewallEnabled())
                Firewall().denyPort(port)
                cprint(f"\n&cFirewall has been denied port to {port}")
                

            cprint(f"\n&cAdd {SERVER_NAME} to the BungeeCord proxy with the command:")
            cprint(f"&c'svm add {SERVER_NAME} 127.0.0.1:{port}'")
        else:
            cprint(f"&aYour server is now live at: 127.0.0.1:{port} OR {getPublicIPAddress()}:{port}")
            cprint(f"&cSince this is a proxy, you may need to tweak config.yml so the lobby server does not point to 25565.")
        

        doStart = cinput("\n&bStart server now? &f[yes/(no)] &b>> ") or "yes"
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
        downloadCache = str(CONFIG["DOWNLOAD_CACHE"])
        file_path = f'{downloadCache}/{jarName}'
        shutil.copyfile(file_path, f"{self.server_path}/{jarName}")
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
    
    def installPluginsToServer(self, isSpigot=True):
        title = 'Please choose which plugins you want to download (press SPACE to select, ENTER to continue): '

        options = []
        for pluginName in list(nameToID.keys()):
            print(pluginName, 'proxy' in pluginName, isSpigot)
            if isSpigot == False:
                if 'proxy' in pluginName:
                    options.append(pluginName)
            else:
                # if its a proxy plugin AND spigot (securedNetwork)
                if 'proxy' in pluginName and 'spigot' in pluginName:
                    options.append(pluginName)
                # else if it is not a proxy plugin
                elif 'proxy' not in pluginName:
                    options.append(pluginName)            
        
        selected = pick(options, title, indicator=' =>', multiselect=True, min_selection_count=0)
        for name, idx in selected:                       
            pluginID = nameToID[name]            
            cprint(f"&aDownloading {name.split(' ', 1)[0]} ({pluginID})")
            downloadResourceFromSpigot(pluginID, f"{self.server_path}/plugins")

            if pluginID in dependencies:
                print("This plugin has dependecies, installing")
                for dep in dependencies[pluginID]:
                    cprint(f"&aDownloading dependency: {dep}")
                    downloadResourceFromSpigot(dep, f"{self.server_path}/plugins")

        option = cinput("&a[!] &fWould you like to pre-install some configuration settings? &f([y]/n)") or 'y'
        if option.lower().startswith('y'):
            self.setupBareBonesConfigurations()
        
    def setupBareBonesConfigurations(self):
        from configs.PluginConfigs import PluginConfigs
        pc = PluginConfigs()
        title = 'Select which configurations you want to setup (press SPACE to select, ENTER to continue): '
        selected = pick(pc.getAvailableConfigs(), title, indicator=' =>', multiselect=True, min_selection_count=0)
        for plugin, idx in selected:
            pluginPath = f"{self.server_path}/plugins/{plugin}/config.yml"
            cfiglet('&a', f"{plugin} config.yml")
            cprint(pluginPath)
            configValuesToSave = pc.run(plugin)
            os.mkdir(f"{self.server_path}/plugins/{plugin}")
            with open(pluginPath, 'w') as file:
                file.write(configValuesToSave)
            




from tqdm import tqdm


def downloadResourceFromSpigot(resourceID, folderPath=os.getcwd(), debug=False):
    url = f"https://api.spiget.org/v2/resources/{resourceID}/download"

    response = requests.get(url, stream=True)
    total = int(response.headers.get('content-length', 0))

    pluginName = IDtoName[resourceID].split(' ', 1)[0]
    jarName = f"{folderPath}/{pluginName}.jar"

    # with open(jarName, "wb") as jar:
    #     jar.write(response.content)

    with open(jarName, 'wb') as file, tqdm(
            desc=pluginName,
            total=total,
            unit='MiB',
            unit_scale=True,
            unit_divisor=1024,
            bar_format="{l_bar}{bar:10}{r_bar}{bar:-10b}" # https://github.com/tqdm/tqdm/issues/585
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)

    if debug: 
        print(f"Downloaded {pluginName} to {jarName}")


if __name__ == "__main__":
    # downloadResourceFromSpigot(95853) # test download
    pass
