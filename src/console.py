'''
Rewrite of features in 1 file for now based on past BASH script?
https://github.com/Reecepbcups/bash-minecraft-panel

sudo pacman -S jre-openjdk

Ensure just to edit PATH_TO_CONFIG_FILE from here
'''

# from utils.yaml import Yaml
# PATH_TO_CONFIG_FILE = "/root/minecraft-panel/config.yml"
# CONFIG = Yaml(PATH_TO_CONFIG_FILE).loadConfig()

from utils.config import CONFIG

from utils.cosmetics import cfiglet, cprint, cinput
# from utils.file_utils import chdir
# from utils_killable_thread import thread_with_trace
# from utils_screen import is_screen_running
from utils.file import fetch_servers

# from utils_yaml import Yaml
# from utils_file import CONFIG

from server import Server
# from firewall import Firewall
# from server_creator import ServerCreator
# from database import Database
from utils.system import checkIfRequirementsAreInstalled

from akash_servers import AkashConsole

import time, os

# Load this before anything else
serverGroups = CONFIG.get('servers') # 'proxy' & 'spigot'
PROXIES = serverGroups['proxy']
SERVERS = serverGroups['spigot']
ALL = list(PROXIES) + list(SERVERS)
# /////


from utils.screen import get_all_active_screens
from panels.database_panel import DatabasePanel
from panels.admin_panel import AdminPanel

def main():
    # databasePanel(); exit(0)

    controlPanel = {        
        "1": ["Console", ServerSelector],              
        "2": ["List Running Servers", get_all_active_screens],
        "3": ["StartAllServers\n", startAllServers],

        "a": ["Akash Docker Connect\n", AkashServerSelector],

        "ADMIN": ["&cAdmin Panel&r", AdminPanel],
        "DB": ["&aDatabase Functions&r", DatabasePanel],
    }

    # isSpigotServerOnBungee("test")
    
    # print(Server('proxy').getInformation())
    # print(is_screen_running("test"))

    cfiglet("&3", "Control Panel", clearScreen=True)
    for k, v in controlPanel.items():
        cprint(f"[{k}]\t {v[0]}")
        
    request = cinput("\nCP> ")
    if request == "exit":
        cprint("&cExiting Panel"); exit(0)

    controlPanel[request][1]()
    pass

def getServers(print_output=False) -> dict:
    choices = {}
    for idx, server in enumerate(fetch_servers()):
        choices[str(idx)] = server
        if print_output:
            print(f"[{idx}] {server}")
    return choices

def getAkashServers(print_output=False) -> dict:
    choices = {}

    servers = CONFIG.get('akash-servers')

    for idx, server in enumerate(servers):
        choices[str(idx)] = server
        if print_output:
            print(f"[{idx}] {server}")
    return choices

def ServerSelector():
    cfiglet("&a", "Console", clearScreen=True)

    choices = getServers(print_output=True)

    server = cinput("\nServer Selector > ")
    if server not in choices:
        cprint("&cInvalid Selection")

    panel = Server(choices[server])
    panel.enter_console()

def AkashServerSelector():
    cfiglet("&b", "Akash Selector", clearScreen=True)

    choices = getAkashServers(print_output=True)

    server = cinput("\nAkash Server Selector > ")
    if server not in choices:
        cprint("&cInvalid Selection")

    panel = AkashConsole(choices[server])
    panel.enter_console()


def DockerSelector():
    from akash_servers import DockerConsole
    import pick
    '''
    cd paper-docker-build
    docker build . -t test-server
    docker rm mc2
    docker run -d -it -p 25565:25565 --name mc2 -e OPS=reecepbcups -e MOTD="My Docker Server" -e EULA=TRUE -e VERSION=1.18.2 test-server:latest
    # Ensure the port for rcon is enabled too
    '''
    cfiglet("&a", "C-Docker", clearScreen=True)

    # I guess we add host here & run docker ps to see running stuff?
    # This possible with akash or?
    dockers = {"mc2": ["65.21.197.51", 2375]}

    for d in dockers:
        print(f"[{d}] {dockers[d][0]}:{dockers[d][1]}")
    print()

    server = cinput("\nDocker Selector > ")
    if server not in dockers:
        cprint("&cInvalid Selection")

    host = dockers[server][0]
    port = dockers[server][1]
    panel = DockerConsole(host, port, server)
    panel.enter_console()


def changeJavaVersion():
    # sudo archlinux-java
    # sudo update-alternatives --config java
    # sudo update-java-alternatives -s $(sudo update-java-alternatives -l | grep 8 | cut -d " " -f1) || echo '.'
    pass


def startAllServers(): 
    for server in ALL:
        Server(server).start_server()         

def stopAllServers():
    for server in ALL:
        Server(server).stop_server() 

def clear_all_logs(printOutput=False):
    for server in ALL:
        if printOutput: print(f"Clearing {server}'s logs")
        Server(server).clear_logs()

def console(server_name):
    if server_name in ALL:
        Server(server_name).enter_console()
    else:
        cprint("&cServer not found")

def isSpigotServerOnBungee(server_name): # do in server object
    check = Server(server_name).values['bungeecord']
	# if so, return 1 - UFW will block port from outside world, but ensure localhost can access it. Or do I do this in firewallBungeeServer?
    return check


def firewallBungeeServer(server_name):
    port = Server(server_name).values['server-port']
    if port == "25565":
        v = cinput("&e[!] Caution, are you sure you want to close port 25565 from connections? This is usually the proxy (y/n)")
        if v.lower() not in ['y', 'yes']:
            return False
    # ufw enable firewall for port here
    return True


def fixPort():
    # could do this when server is started / first input? check if log contains the PORT issue
    pass

# == Firewall ==
def firewallReset(): # accept all 
    pass
def firewallBlockPort(server_name):
    # check if isServerOnBungee, get port, close to outside connections
    pass
def firewallApplyRules():
    # ensure port 22 is open here always
    pass

def serverReboot(server_name):
    pass

# get the users linux home directory
homeDir = os.path.expanduser('~')
profile = os.path.join(homeDir, '.bashrc')
screenfile = os.path.join(homeDir, '.screenrc')


# Add to system utils in future?
def addConsoleAliasToBashProfileIfNotThereAlready() -> bool:
    # ensure profile file is there. Returns False if `console` being run would not run it

    if not os.path.exists(profile):
        cprint(f"&c[!] File {profile} not found.. creating")
        open(profile, 'x') # creates file

    # allows scrolling in screen
    if not os.path.exists(screenfile):
        open(screenfile, 'x')
    if "termcapinfo xterm* ti@:te@" not in open(screenfile, 'r').read():
        with open(screenfile, 'a') as sf:
            sf.write("termcapinfo xterm* ti@:te@")

    panelDir = CONFIG.get("PANEL_DIRECTORY"); # print(f"{thisDirectory=}")
    alias = f"alias console='python {panelDir}/src/console.py'\n"
    # .bashrc | checks if you have an alias for a given command and runs the aliased command instead of the literal one with sudo in that case
    sudoAlias = """sudo() { if alias "$1" &> /dev/null ; then $(type "$1" | sed -E 's/^.*`(.*).$/\1/') "${@:2}" ; else command sudo $@ ; fi }\n"""

    if alias in open(profile, 'r').read():        
        # cprint(f"&cConsole already added. If you need to source: &e`source {profile}`")
        return True

    with open(profile, 'a') as bashprofile:
        bashprofile.write(alias)
        bashprofile.write(sudoAlias) # `sudo console` then works too
        print(f"Added alias 'console' to {profile}.")
        cprint(f"&c{'='*20}\n\t\tRun the following command in your terminal:\n\n\n\t\tsource {profile}\n\n\n" + "="*20)
    return False



__version__ = "1.0.0"
def getVersion() -> str:
    return __version__

import sys
from CLI import call

if __name__ == "__main__":

    # Ensures Java & pip are installed
    if(checkIfRequirementsAreInstalled() == False):
        exit(1)

    # Ensure 'console' points to this console file location. If not it adds it.
    if(addConsoleAliasToBashProfileIfNotThereAlready() == False):
        exit(1)
    
    # check if there are any system arguments
    if len(sys.argv) > 1:        
        call(list(sys.argv)[1::])
        exit(0) # true or false we also return so no main call is done
        
    # Call the main console fo the user if the above are good
    main()