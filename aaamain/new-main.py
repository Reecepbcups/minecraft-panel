'''
Rewrite of features in 1 file for now based on past BASH script?
https://github.com/Reecepbcups/bash-minecraft-panel
'''

SERVER_INFO_LOCATION = '/root/minecraft-panel/server_info.yml'

from utils.cosmetics import color, cfiglet, cprint, color_dict, cinput

import pyfiglet

from utils.screen import is_screen_running
from utils.file_utils import fetch_servers

import re
def splitColors(myStr) -> list:
    # "&at&bt&ct" -> ['', '&a', 't', '&b', 't', '&c', 't']
    # _str = "&at&bt&ct"
    # splitColors(_str)
    return re.split("(&[a-zA-Z0-9])", myStr)

def main():

    print(is_screen_running("test"))
    # get_all_active_screens()

    dummyConsole()

    # adminPanel = {
    #     "1": newServerInstance,
    #     "2": stopAllServers,
    #     # "3": "dailyRebootSetup",
    #     # "WEB": "webLinkShortener",
    #     "RESET-FIREWALL": firewallReset,
    #     "CHANGE-JAVA-VERSION": changeJavaVersion,
    #     # "KILL-ALL-JAVA": ,
    #     "APPLY-FIREWALL": firewallApplyRules,
    # }
    # databasePanel = {
    #     "1": createDatabase,
    #     "2": deleteDatabase,
    #     "3": showDatabases,
    #     "4": createNewUser,
    #     "5": deleteUser,
    #     "6": showUser,
    #     "exit": exit,
    # }

    # controlPanel = {        
    #     "1": ["Console", dummyConsole],
    #     "2": ["List Running Servers", dummyConsole],
    # }
    # cfiglet("&3", "Control Panel")
    # for k, v in controlPanel.items():
    #     cprint(f"[{k}] {v[0]}")
    # request = input("CP> ")
    # controlPanel[request][1]()
    pass

import time, os
def tail_file(file_path):
    with open(f'{file_path}') as log:
        log.seek(0, os.SEEK_END)

        while True:
            line = log.readline()
            if not line:
                time.sleep(0.1)
                continue
            
            cprint(line.replace("\n", ""))

def getServers(print_output=False) -> dict:
    choices = {}
    for idx, server in enumerate(fetch_servers()):
        choices[str(idx)] = server
        if print_output:
            print(f"[{idx}] {server}")
    return choices

def dummyConsole():
    cfiglet("&a", "Console")
    # show all servers in list

    choices = getServers(print_output=True)

    server = input("Server Selector:")
    if server not in choices:
        cprint("&c", "Invalid Selection")

    ServerPanel(choices[server]).enter_console()
    

import subprocess
from utils.killable_thread import thread_with_trace

class ServerPanel:
    def __init__(self, server_name):
        self.server_name = server_name
        self.path = f'/root/minecraft-panel/aaamain/servers/{server_name}'

    def enter_console(self):

        cfiglet("&a", self.server_name)
        cprint("&6 Console:")
        cprint("&6 -> 'start-server' &f(only if offline)")
        cprint("&6 -> 'stop-server'")
        cprint("&6 -> 'exit'")

        cprint("&bserver-port=")
        cprint("&bMEMORY=")
        cprint("&bPID=")
        print()

        console = thread_with_trace(target=self.follow)
        console.start()

        running = True
        while running:
            user_input = input()
            if user_input == "\x18":
                running = False
            elif user_input == "restart":
                running = False
                self.restart_server()
            elif user_input == "stop":
                running = False
                self.stop_server()
            else:
                self.server_input(user_input)
        
        console.kill()
        console.join(timeout=0.05)

    def server_input(self, user_input):
        subprocess.call(['screen', '-S', f'{self.server_name}', '-X', 'stuff', f'{user_input}\015'])

    def follow(self):
        with open(f'{self.path}/logs/latest.log') as log:
            log.seek(0, os.SEEK_END)
            while True:
                line = log.readline()
                if not line:
                    time.sleep(0.1)
                    continue
                
                cprint(line.replace("\n", ""))


def sendServerCommand(server_name):
    pass

def getServerPort(server_name): # could make this get any server variable from start.sh or spigot.yml w/ enums
    pass

def startAllServers():
    pass

def stopAllServers():
    pass

def listRunningServers():
    pass



# == MongoDB ==
def createDatabase():
    pass
def deleteDatabase():
    pass
def showDatabases():
    pass

def createNewUser():
    pass
def deleteUser():
    pass
def showUser():
    pass

def printTitle():
    # figlet
    pass

def console(server_name):
    pass

def isServerOnBungee():
    # Checks if server is on bungee with spigot bungee=true.
	# if so, return 1 - will ufw block it on startup for security
    pass

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

def newServerInstance():
    # eula true in start.sh script
    '''"#!/bin/sh
# Reecepbcups - start.sh script for servers. 
# Use the 1st JAVA_ARGS option (long) if you use more than 12GB of ram on the server instance
            
MEM_HEAP=\"${RAM}\"
JAR_FILE=\"Paper-${VERSION}.jar\"
#JAVA_ARGS=\"-Dfile.encoding=utf-8 -XX:+UnlockExperimentalVMOptions -XX:G1NewSizePercent=40 -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:-OmitStackTraceInFastThrow -XX:+AlwaysPreTouch  -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=50 -XX:G1HeapRegionSize=16M -XX:G1ReservePercent=15 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=8 -XX:InitiatingHeapOccupancyPercent=20 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=true -Daikars.new.flags=true -jar\"
JAVA_ARGS=\"-Dfile.encoding=utf-8 -jar\"
while true; do
	java -Xms\$MEM_HEAP -Xmx\$MEM_HEAP \$JAVA_ARGS \$JAR_FILE nogui
	echo \"Restarting server in 5 seconds\"
	sleep 4
	echo \"Restarting...\"
	sleep 1
done"'''

    '''
    if [ "$BUNGEE" == "y" ]; then 
            ONLINEMODE=false && NETWORKCOMPRESSION=-1
            echo "settings:
    bungeecord: true
    restart-on-crash: false
    restart-script: ./DoneByStartScript.sh" >> spigot.yml
        else
            ONLINEMODE=true && NETWORKCOMPRESSION=256
        fi
    '''
    pass

# == Debug ==
def changeJavaVersion():
    #   sudo update-alternatives --config java
    pass
 
def otherStuff():
    # kilall -9 java;
    # speedometer -l -r eth0 -t eth0 -m $(( 1024 * 1024 * 3 / 2 )) # network stats
    # free -g -l && free -t | awk 'NR == 2 {printf("\n\nCurrent Memory Utilization is : %.2f%\n\n"), $3/$2*100}' # RAM
    # iostat && df -h # storage
    pass


if __name__ == "__main__":
    # new machine setup, ensure to create server_info.sh here too + backup script
    """
    apt-get update --allow-releaseinfo-change
    echo "root ALL=(ALL) ALL" >> /etc/sudoers
	echo "sudo ALL=(ALL) ALL" >> /etc/sudoers

    echo "alias console='/root/server/Console-v*.sh'" >> /root/.bashrc
	source /root/.bashrc

    apt-get --yes --force-yes install curl software-properties-common
		curl -sL https://deb.nodesource.com/setup_12.x | bash -
		
    # Install other programs
    apt-get --yes --force-yes install build-essential sudo zip unzip lsof dos2unix nginx screen htop glances 
    apt-get --yes --force-yes install nodejs cpufrequtils figlet redis default-jre sysstat slurm speedometer
    cpufreq-set -r -g performance	
    timedatectl set-timezone America/Chicago
    
    # Java 11 - doesnt work for my 1.8 MC
    echo 'deb http://ftp.debian.org/debian stretch-backports main' | sudo tee /etc/apt/sources.list.d/stretch-backports.list
    sudo apt update && apt-get upgrade
    sudo apt install openjdk-11-jdk
    sudo apt-get install openjdk-11-jre
    
    # Java 8 / Java8
    wget -qO - https://adoptopenjdk.jfrog.io/adoptopenjdk/api/gpg/key/public | sudo apt-key add -
    sudo add-apt-repository --yes https://adoptopenjdk.jfrog.io/adoptopenjdk/deb/
    sudo apt-get update && sudo apt-get install adoptopenjdk-8-hotspot
    
    # https://stackoverflow.com/questions/57031649/how-to-install-openjdk-8-jdk-on-debian-10-buster
    sudo apt-add-repository 'deb http://security.debian.org/debian-security stretch/updates main'
    sudo apt-get update
    sudo apt-get install openjdk-8-jdk
    
    sudo update-alternatives --config java
    """
    main()