import json
import os
import subprocess
import sys
import time
# from sh import tail

import yaml

from utils.config import CONFIG
from utils.cosmetics import cfiglet, cinput, color_dict, cprint
from utils.file import chdir
from utils.killable_thread import thread_with_trace
from utils.screen import is_screen_running


class Server:
    def __init__(self, server_name):
        self.server_name = server_name
        self.path = f"""{CONFIG["SERVER_DIRECTORY"]}/{server_name}"""
        self.values = {} # fr0m properties & spigot.yml
        self.getInformation() # populates values in a dict

    # Gets a property value. not pythonic but is needed for console
    def get(self, value: str):
        try:
            return self.values[value]
        except:
            return "ERROR: Property not found"

    def start_server(self, debug=True) -> bool:
        if is_screen_running(self.server_name):
            if debug: cprint("&cYou can't start a server that is already running")
            return False

        # if on bungeecord, ensure that its firewalled

        os.chdir(self.path) #;print(os.getcwd())
        cmd = f'screen -dmS {self.server_name} ./start.sh'
        print(cmd)

        # run command & get stdfout
        p = os.popen(cmd)
        cprint(f"&aServer '{self.server_name}' Started")        
        return True

    def stop_server(self):
        if not is_screen_running(self.server_name):
            cprint(f"&cServer {self.server_name} is not running")
            return
                        

        self.send_console_command("stop")         
        v1 = os.system(f'screen -X -S "{self.server_name}" stuff "^C"')                
        cprint(f"&eServer '{self.server_name}' stopping...")
        time.sleep(8)

        # stop the screen using os.system
        os.system(f'screen -X -S "{self.server_name}" stuff "^C"')   
        os.system(f'screen -X -S "{self.server_name}" stuff "^C"')   
        os.system(f'screen -X -S "{self.server_name}" stuff "^C"')   
        v = os.system(f'screen -X -S "{self.server_name}" quit')
        if v != 0:
            cprint(f"&cSome error when stopping server")
            return
        cprint(f"&aServer '{self.server_name}' Stopped")

    def enter_console(self):               
        statusColor = '&a' if is_screen_running(self.server_name) else '&c'

        cfiglet(statusColor, self.server_name)

        cprint(f"&f - {self.path}\n")
        cprint("&6 Console:")
        cprint("&6 -> 'start-server' &f(only if offline)")
        cprint("&6 -> 'stop-server'")
        cprint("&6 -> 'exit' &f(ctrl + x + enter)")

        output = [
            f"\n&bserver-port={self.get('server-port')}", 
            f"&bview-distance={self.get('view-distance')}",
            f"&bon-bungeecord={self.get('bungeecord')}",
            f"&bmax-players={self.get('max-players')}",
            f"&bMEMORY={self.get('MEM_HEAP')}",
            f"&bPID=",
        ]

        for property in output:
            try:
                cprint(property)
            except:
                pass        
        print()

        try: # error handling incase they 'log' to reset this
            console.kill()
        except UnboundLocalError:
            pass

        console = thread_with_trace(target=self.follow)
        console.start()

        options = {
            "start-server": [self.start_server, "start-server"],
            "stop-server": [self.stop_server, "break"],
            "log": [self.enter_console, "log"],
            # "restart": self.re, # start.sh will auto do this
            # "stop": [self.stop_server, "break"],
        }

        try:
            while True:
                user_input = cinput()

                if user_input in options:    
                    if options[user_input][1] == "start-server" or options[user_input][1] == "log":
                        console.kill() # kill console read if we start new instance (no duplicates)
                    options[user_input][0]()
                    if options[user_input][1] == "break":
                        break
                    continue
                
                elif user_input == "\x18": # ctrl + c
                    break

                elif user_input == "exit": # brings you to main() after console killed
                    break

                else:
                    self.send_console_command(user_input)
        except KeyboardInterrupt:
            pass
        
        console.kill()
        console.join(timeout=0.05)

        try:
            if user_input == "exit":
                import panels.main_panel as main_panel
                main_panel.MainPanel()
                # print("sys exit line 103 of server.py")
                # sys.exit(0)
        except:
            cprint("&eClosing...")
            pass # user control c'ed out

    def send_console_command(self, user_input):
        #\015 = new line character unicode
        subprocess.call(['screen', '-S', f'{self.server_name}', '-X', 'stuff', f'{user_input}\015'])

    def follow(self):
        path = f'{self.path}/logs/latest.log'        

        # check if exist        
        if not os.path.exists(path):
            cprint("&cLog file not found. Creating...")
            # write to path, including any nested folders
            open(path, 'x').close()                  
            
        # read the last X lines of the log file on open
        self.showLogOnce(15)

        with open(path, 'r') as log:
            log.seek(0, os.SEEK_END)            
            while True:
                line = log.readline()
                if not line:
                    time.sleep(0.1)
                    continue                
                cprint(line.replace("\n", ""))

        # for line in tail("-f", path, _iter=True):
        #     cprint(line.replace("\n", ""))            

    def showLogOnce(self, numOfLines):
        '''Shows the last X number of lines in the log file 1 time'''
        path = f'{self.path}/logs/latest.log'
        with open(path, 'r') as f:            
            for line in f.readlines()[-numOfLines:]:
                cprint(line.replace("\n", ""))

    def getInformation(self):
        startFile = self.path + "/start.sh"
        with open(startFile, 'r') as f:
            for line in f:
                if '=' not in line:
                    continue
                elif line.strip().startswith('#'):
                    continue # ignore commented lines
                pair = line.split("=", 1)
                if len(pair) > 1:
                    self.values[pair[0]] = pair[1].strip()            

        # This is a proxy, do this then return
        proxyYML = self.path + "/config.yml"        
        if os.path.exists(proxyYML):            
            # bungee config yml, is not the panels
            # proxyConfig = Y-M-L(self.path + "/config.yml").loadConfig().getConfig(); #print(proxyConfig.keys())
            # Loads yaml file file to read values from
            with open(proxyYML, 'r') as stream:
                proxyConfig = yaml.safe_load(stream)
            # print(proxyConfig)
            for key, v in proxyConfig.items():
                self.values[key] = v

            # Return early since its not a spigot server
            return self.values


        spigotYML = self.path + "/spigot.yml"        
        properties = self.path + "/server.properties"
        # paperYML = self.path + "/paper.yml"
        # open properties, get all keys & add to values dict
        with open(properties, 'r') as f:
            for line in f:
                pair = line.split("=")
                if len(pair) > 1:
                    self.values[pair[0]] = pair[1].strip()

        # open spigotYML & check if the bungeecord key is set. No need to do YAML since its just 1 value rn
        with open(spigotYML, 'r') as f:
            for line in f:
                if line.startswith("bungeecord:"):
                    self.values["bungeecord"] = line.split(":")[1].strip()
                    break

        return self.values



    def clear_logs(self, debug=False):
        location = self.path + "/logs"

        if os.path.exists(location):
            # loop through files in location
            for file in os.listdir(location):
                # delete file if it is a *.log.gz file
                if file.endswith(".log.gz"):
                    f = location + "/" + file
                    if debug: 
                        print("-", f)
                    os.remove(f)
