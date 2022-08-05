from panels.firewall_panel import FirewallPanel
from panels.admin_panel import AdminPanel
from panels.database_panel import DatabasePanel
from panels.redis_panel import RedisPanel

import sys
import os
from os.path import dirname as parentDir

from pick import pick

import CLI_API

from akash_servers import AkashConsole

from server import Server
from utils.config import CONFIG
from utils.cosmetics import cfiglet, cinput, cprint
from utils.file import fetch_servers
from utils.system import checkIfRequirementsAreInstalled
from utils.screen import get_all_active_screens

import console # dont from import, only reference here so no import loop

from utils.akash import AkashServerSelector

class MainPanel():
    def __init__(self, run=True):
        self.controlPanel = {        
            "1": ["Console", ServerSelector],              
            "2": ["List Running Servers", get_all_active_screens],
            "3": ["Start Server(s)", startServerPicker],
            "4": ["Stop Server(s)\n", stopServerPicker],

            "a": ["Akash Docker Connect\n", AkashServerSelector],

            "s": ["Screens\n", screenPicker],

            "ADMIN": ["&cAdmin Panel&r", AdminPanel],
            "DB": ["&aDatabase Functions&r", DatabasePanel],
            "RED": ["&4Redis Functions&r", RedisPanel],
            "FIRE": ["&4Firewall Panel&r", FirewallPanel],
        }
        if run:
            self.loop()

    def loop(self):
        while True:
            cfiglet("&3", "Control Panel", clearScreen=True)
            for k, v in self.controlPanel.items():
                cprint(f"[{k}]\t {v[0]}")
                
            request = cinput("\nCP> ")
            if request == "exit":
                cprint("&cExiting Panel"); exit(0)
                
            if request not in self.controlPanel:
                cprint("&cInvalid Selection")
                continue

            self.controlPanel[request][1]()
            pass

def getServers(print_output=False) -> dict:
    choices = {}
    for idx, server in enumerate(fetch_servers()):
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

    if len(server) > 0:
        panel = Server(choices[server])
        panel.enter_console()
    else:
        cprint("&cNo server selected")


def startServerPicker():
    if len(console.ALL) == 0:
        cinput("&cThere are no servers in the config to start. (Enter to continue...)")

    # Servers which are running AND are in our config of actual servers
    servers = pick(console.ALL, title="Select servers to start (Select: Space, Confirm: Enter)!", multiselect=True, indicator=' =>')
    started, alreadyRunning = [], []
    for server in servers:
        serverName = server[0]
        
        status = Server(serverName).start_server(debug=False)
        if status:
            started.append(serverName)
        else:
            alreadyRunning.append(serverName)  

    output = ""
    if len(started) > 0: output += f"\n&aStarted: {','.join(started)}\n"    
    if len(alreadyRunning) > 0: output += f"&eAlready Running: {','.join(alreadyRunning)}."
    if len(output) > 0: cinput(output + ", Enter to continue...")


def screenPicker():
    activeScreens = get_all_active_screens(printOutput=False)

    if len(activeScreens) == 0:
        cprint("&cNo screens are running")
        input("Enter to continue...")

    screen, _ = pick(activeScreens, title="Select Screen to connect too", indicator=' =>')
    os.system(f"screen -r {screen}")

def stopServerPicker():
    runningServers = get_all_active_screens(printOutput=False)
    actualServers = [s for s in runningServers if s in console.ALL]
    if len(actualServers) == 0:
        cprint("&cNo servers are running")
        input("Enter to continue...")

    # Servers which are running AND are in our config of actual servers    
    servers, _ = pick(actualServers, title="Select servers to stop (Select: Space, Confirm: Enter)!", multiselect=True, indicator=' =>')
    for server in servers:
        Server(server).stop_server()