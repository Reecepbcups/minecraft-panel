'''
Rewrite of features in 1 file for now based on past BASH script?
https://github.com/Reecepbcups/bash-minecraft-panel

sudo pacman -S jre-openjdk

Ensure just to edit PATH_TO_CONFIG_FILE from here
'''

import os
import sys

import CLI_API

from os.path import dirname as parentDir
from pick import pick

import panels.main_panel as main_panel

from server import Server
from utils.config import CONFIG
from utils.cosmetics import cfiglet, cinput, cprint
from utils.file import fetch_servers
from utils.screen import get_all_active_screens
from utils.system import checkIfRequirementsAreInstalled

# Load this before anything else
serverGroups = CONFIG['servers'] # 'proxy' & 'spigot'
PROXIES = serverGroups['proxy']
SERVERS = serverGroups['spigot']
ALL = list(PROXIES) + list(SERVERS)
#
# Get the users linux home directory
#
homeDir = os.path.expanduser('~')
profile = os.path.join(homeDir, '.bash_profile')
bashrc = os.path.join(homeDir, '.bashrc')
screenfile = os.path.join(homeDir, '.screenrc')


def main():
    # isSpigotServerOnBungee("test")
    # print(Server('proxy').getInformation())
    # print(is_screen_running("test"))
    main_panel.MainPanel()
    pass

    
    






# ------
# below could probably move into their own UTIL Files / panel sections

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

def isSpigotServerOnBungee(server_name) -> bool: # do in server object
    check = Server(server_name).values['bungeecord']
	# if so, return 1 - UFW will block port from outside world, but ensure localhost can access it. Or do I do this in firewallBungeeServer?
    return True if check == 1 else False


def fixPort():
    # could do this when server is started / first input? check if log contains the PORT issue
    pass

def serverReboot(server_name):
    pass


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

    # gets the root folder of this program
    panelDir = parentDir(parentDir(__file__)); # print(f"{thisDirectory=}")
    alias = f"\nalias console='python {panelDir}/src/console.py'\n"
    sudoAlias = f"alias sconsole='sudo python {panelDir}/src/console.py'\n"

    if alias in open(profile, 'r').read():
        return True # Already added to file

    with open(bashrc, 'a') as bf: # sources .bashrc to run the .profile values
        bf.write(f"source {profile}")

    with open(profile, 'a') as bashprofile:
        bashprofile.write(alias)
        bashprofile.write(sudoAlias) # `sudo console` then works too, TODO this does not work yet
        print(f"Added alias 'console' to {profile}.")
        cprint(f"&c{'='*20}\n\t\tRun the following command in your terminal:\n\n\n\t\tsource {profile} && source {bashrc}\n\n\nThen you can run 'console' and 'sconsole'" + "="*20)
    return False



__version__ = "1.0.0"
def getVersion() -> str:
    return __version__



if __name__ == "__main__":

    # Ensures Java & pip are installed
    if(checkIfRequirementsAreInstalled() == False):
        exit(1)

    # Ensure 'console' points to this console file location. If not it adds it.
    if(addConsoleAliasToBashProfileIfNotThereAlready() == False):
        exit(1)
    
    # check if there are any system arguments, if so, calls the section here or the API
    if len(sys.argv) > 1:   
        m = main_panel.MainPanel(run=False)
        if sys.argv[1] in m.controlPanel:
            # Calls the section directly from our CP
            m.controlPanel[sys.argv[1]][1]()
        else:
            CLI_API.call(list(sys.argv)[1::])
        exit(0)
        
    # Call the main console fo the user if the above are good
    main()
