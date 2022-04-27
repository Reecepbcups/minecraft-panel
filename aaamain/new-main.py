'''
Rewrite of features in 1 file for now based on past BASH script?
https://github.com/Reecepbcups/bash-minecraft-panel

sudo pacman -S jre-openjdk
'''

SERVER_INFO_LOCATION = '/root/minecraft-panel/server_info.yml'

from utils.cosmetics import color, cfiglet, cprint, color_dict, cinput

import pyfiglet

from utils.screen import is_screen_running
from utils.file_utils import fetch_servers

import re
def splitColors(myStr) -> list:
    # "&at&bt&ct" -> ['', '&a', 't', '&b', 't', '&c', 't']
    # _str = "&at&bt&ct"; splitColors(_str)
    return re.split("(&[a-zA-Z0-9])", myStr)

# Load this before anything else
from utils.yaml_utils import Yaml
v = Yaml(f'/root/minecraft-panel/aaamain/configs/config.yml')
config = v.loadConfig()

PROXIES = config['servers']['proxy']
SERVERS = config['servers']['spigot']       
ALL = list(PROXIES) + list(SERVERS)
# /////

'''
adminPanel = {
        "1": newServerInstance,
        "2": stopAllServers,
        # "3": "dailyRebootSetup",
        # "WEB": "webLinkShortener",
        "RESET-FIREWALL": firewallReset,
        "CHANGE-JAVA-VERSION": changeJavaVersion,
        # "KILL-ALL-JAVA": ,
        "APPLY-FIREWALL": firewallApplyRules,
    }
    databasePanel = {
        "1": createDatabase,
        "2": deleteDatabase,
        "3": showDatabases,
        "4": createNewUser,
        "5": deleteUser,
        "6": showUser,
        "exit": exit,
    }
'''

def main():

    
    
    # 'Enable Access Control' `mongodb://myDBReader:password@127.0.0.1:27017/?authSource=admin`.
    # mongo -u myUserAdmin -p OR mongo, then 'use admin; db.auth("myUserAdmin", "password123");'
    database = Database("mongodb://myUserAdmin:password123@127.0.0.1:27017/?authSource=admin") 
    # database = Database("mongodb://127.0.0.1:27017/")

    dbs = database.listDatabases()
    print(dbs)
    database.dropDatabase("test_db", debug=True)

    # print(database.listDatabaseRoles("admin"))
    print("admin db users:", database.listUsers(database_name="admin"))
    database.enableMongoDBAuthentication()

    # creates user on the test database, with roles to access other databases as well. This means the myTester user MUST auth with the test database in the uri
    # mongo -u myTester -p --authenticationDatabase test OR mongo, then 'use test; db.auth("myTester", "myPassXYZ");'
    database.createNewUser("test", "myTester", "myPassXYZ", [{'role': 'readWrite', 'db': 'test'}, {'role': 'read', 'db': 'test_db'}])
    print("test db users:", database.listUsers(database_name="test"))

    # database.changeUsersPassword("test", "myTester")

    # database.createTestCollection(collection_name="test-s", database_name="test")

    print("="*20)
    # database.createNewUser("test", "testingacc", "myPassXYZ", [{'role': 'readWrite', 'db': 'test'}])
    print("test db users:", database.listUsers(database_name="test"))
    database.deleteUser("test", "testingacc")
    print("test db users:", database.listUsers(database_name="test"))


    # collections = database.listCollections("admin")
    # print(collections)

    # clear_all_logs()
    # print(Server('proxy').getInformation())
    # print(is_screen_running("test"))
    # get_all_active_screens()

    # dummyConsole()
    # startAllServers()

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

def getServers(print_output=False) -> dict:
    choices = {}
    for idx, server in enumerate(fetch_servers()):
        choices[str(idx)] = server
        if print_output:
            print(f"[{idx}] {server}")
    return choices

def dummyConsole():
    cfiglet("&a", "Console")

    choices = getServers(print_output=True)

    server = cinput("Server Selector:")
    if server not in choices:
        cprint("&cInvalid Selection")

    panel = Server(choices[server])
    panel.enter_console()
    

from utils.file_utils import chdir

import subprocess
from utils.killable_thread import thread_with_trace

class Server:

    def __init__(self, server_name):
        self.server_name = server_name
        self.path = f"{config['serverloc']}/{server_name}"
        self.values = {} # from properties & spigot.yml
        # self.getInformation() # populates values in a dict

    def start_server(self):
        if is_screen_running(self.server_name):
            cprint("&cYou can't start a server that is already running")
            return

        # if on bungeecord, ensure that its firewalled

        os.chdir(self.path) #; print(os.getcwd())
        v = os.system(f'screen -dmS {self.server_name} ./start.sh')
        if v != 0:
            cprint(f"&cSome error when starting server")
            return
        cprint(f"&aServer '{self.server_name}' Started")

    def stop_server(self):
        if not is_screen_running(self.server_name):
            cprint(f"&cServer {self.server_name} is not running")
            return
        
        # sigterm minecraft
        # kill $(ps h --ppid $(screen -ls | grep session_name | cut -d. -f1) -o pid)
        self.send_console_command("stop")
        cprint(f"&eServer '{self.server_name}' stopping...")
        time.sleep(5)

        # stop the screen using os.system
        v = os.system(f'screen -S {self.server_name} -X quit')
        if v != 0:
            cprint(f"&cSome error when stopping server")
            return
        cprint(f"&aServer '{self.server_name}' Stopped")

    def enter_console(self):
        cfiglet("&a", self.server_name)

        cprint(f"&f - {self.path}\n")
        cprint("&6 Console:")
        cprint("&6 -> 'start-server' &f(only if offline)")
        cprint("&6 -> 'stop-server'")
        cprint("&6 -> 'exit' &f(ctrl + x + enter)")

        cprint(f"\n&bserver-port={self.values['server-port']}")
        cprint(f"&bview-distance={self.values['view-distance']}")
        cprint(f"&bon-bungeecord={self.values['bungeecord']}")
        cprint(f"&bmax-players={self.values['max-players']}")
        cprint(f"&bMEMORY={self.values['MEM_HEAP']}")
        cprint(f"&bPID=")
        print()

        console = thread_with_trace(target=self.follow)
        console.start()

        options = {
            "start-server": [self.start_server, "continue"],
            "stop-server": [self.stop_server, "break"],
            # "restart": self.re, # start.sh will auto do this
            "stop": [self.stop_server, "break"],
        }

        try:
            while True:
                user_input = input()

                if user_input in options:
                    options[user_input][0]()
                    if options[user_input][1] == "break":
                        break
                    continue
                
                elif user_input == "\x18":
                    break

                elif user_input == "exit": # brings you to main() after console killed
                    break

                else:
                    self.send_console_command(user_input)
        except KeyboardInterrupt:
            pass
        
        console.kill()
        console.join(timeout=0.05)

        if user_input == "exit":
            main()

    def send_console_command(self, user_input):
        subprocess.call(['screen', '-S', f'{self.server_name}', '-X', 'stuff', f'{user_input}\015'])

    def follow(self):
        path = f'{self.path}/logs/latest.log'
        # check if exist
        if not os.path.exists(path):
            cprint("&cLog file not found. Creating...")
            # write to path, including any nested folders
            with open(path, 'w') as f:
                f.write("")
            
        with open(path, 'r') as log:
            log.seek(0, os.SEEK_END)
            while True:
                line = log.readline()
                if not line:
                    time.sleep(0.1)
                    continue
                
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
        proxyYML = self.path + "/waterfall.yml"        
        if os.path.exists(proxyYML):
            proxyConfig = self.path + "/config.yml"

            config = Yaml(proxyConfig).loadConfig(); #print(config)
            for key in config.keys():
                self.values[key] = config[key]

            # Retrurn early since its not a spigot server
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

        # open spigotYML & check if the bungeecord key is set
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

def clear_all_logs():
    for server in ALL:
        Server(server).clear_logs()


# == MongoDB ==
# python -m pip install pymongo dnspython (so we can use srv URI)
# sudo pacman -S --needed base-devel git nano vi

# You could also run as a docker container, prob easier... install mongo client
# sudo systemctl start docker
# docker run -d -p 27017:27017 -v data:/data/db mongo

# https://www.maketecheasier.com/use-aur-in-arch-linux/
# useradd -m software -p myPassword19191 --shell /bin/false
# usermod -aG wheel software # this is adding sudo to user
# nano /etc/sudoers # (really you should use visudo, but you'll be okay)
# uncomment the following lines: 
# # %wheel ALL=(ALL:ALL) ALL
# # %wheel ALL=(ALL:ALL) NOPASSWD: ALL
# ctrl+x, y, enter

# su software -s /bin/bash
# cd ~
# git clone https://aur.archlinux.org/mongodb-bin.git
# cd mongodb-bin
# makepkg -si

# exit # gets you back to root user
# cd /home/software/mongodb-bin/ && sudo pacman -U --noconfirm mongodb-bin-*.tar.zst
# systemctl start mongodb.service
# systemctl status mongodb # should return active
# if so:
# systemctl enable mongodb.service
# mongo



from pymongo import MongoClient
from pymongo import database
from pymongo.typings import _DocumentType

class Database:

    '''
    config.yml

    Mongo-Authentication: # Maybe allow the user to store uri's here?
      admin: admin
      myTester: test
    '''

    def __init__(self, uri):
        # self.CONNECTION_URI = uri   
        self.client = MongoClient(uri)

    def listDatabases(self) -> list:
        return self.client.list_database_names()

    def getDatabase(self, database_name) -> database.Database[_DocumentType]:
        return self.client[database_name]

    def dropDatabase(self, database_name, debug=False) -> bool:
        # ensure database_name exist
        if database_name in self.listDatabases():
            # removes ' incase the user actually type these too
            v = cinput(f"\n&c[!] Type 'delete {database_name}' to confirm deletion\n>>").replace("\'", "").strip()
            if(v == f"delete {database_name}"):
                self.client.drop_database(database_name)
                if debug: print(f"Dropped database: {database_name}")
                return True
            else:
                cprint("&eIncorrect Input")                
                self.dropDatabase(database_name) # Try again, incorrect input
            
        if debug: print(f"Database {database_name} not found, Can't delete...")
        return False

    # Roles
    def enableMongoDBAuthentication(self):
        # Add input here in the future
        notCreated = self.createNewUser("admin", "myUserAdmin", "password123", [{'role': 'userAdminAnyDatabase', 'db': 'admin'}, "readWriteAnyDatabase"])
        if notCreated:
            cprint("\n\n&e[!] You should now stop the mongodb (docker or service file) and start with authetication")
            cprint("&e - nano /etc/mongodb.conf")
            cprint("&e - add the following\n\nsecurity:\n\tauthorization: \"enabled\"")
            cprint("&e - systemctl restart mongodb.service && journalctl -u mongodb\n\n\n")    

    def getRoleInfo(self, database_name, role):
        # return self.getDatabase(database_name).command({
        #     'rolesInfo': {'role': role, 'db': database_name},
        #     'showPrivileges': True, 'showBuiltinRoles': True
        # })
        return ["dbAdmin", "dbOwner", "read", "readWrite", "userAdmin"]

    def authenticate(self, database_name, username, password):
        return self.getDatabase(database_name).authenticate(username, password)

    # Collections
    def listCollections(self, database_name) -> list:
        return self.client[database_name].list_collection_names()

    def getCollection(self, database_name, collection_name):
        return self.client[database_name][collection_name]

    # Users
    def createNewUser(self, database_name, username, password, roles) -> bool:
        if username in self.listUsers(database_name):
            cprint(f"&c[!] User {username} already exsist in {database_name}")
            return False

        # create a new user
        self.getDatabase(database_name).command({
            'createUser': username,
            'pwd': password,
            'roles': roles
        })
        return True

    def changeUsersPassword(self, database, user):
        if user not in self.listUsers(database):
            cprint(f"&c[!] User {user} not found in {database}")
            return False

        newPass = cinput("\n&b[!] Enter new password: ")
        status = self.getDatabase(database).command({
            'updateUser': user,
            'pwd': newPass
        })
        status = self._getDocumentStatus(status)
        output = f"&aPassword for user {user} has been changed to: {newPass}"
        if status == False:
            output = f"&cPassword change was not successfull for {user}"
        cprint(output)
        return status

    def createTestCollection(self, database_name, collection_name):
        db = self.getDatabase(database_name)

        if not collection_name in db.list_collection_names():
            db.create_collection(collection_name)

        col = db.get_collection(collection_name)
        col.insert_one({'name': 'test'})
        print(col.find_one())

    def deleteUser(self, database_name, user):        
        if user not in self.listUsers(database_name):
            cprint(f"&c[!] User {user} not found in {database_name}")
            return False

        status = self.getDatabase(database_name).command({
            'dropUser': user
        })
        return  self._getDocumentStatus(status)

    def listUsers(self, database_name):
        listing = self.getDatabase(database_name).command("usersInfo")
        users = {}
        for doc in listing['users']:
            users[doc['user']] = doc['roles']
        return users

    def _getDocumentStatus(self, _CodecDocumentType: dict):
        '''
        Take the return from .command() -> a true or false value
        '''
        for k, v in _CodecDocumentType.items():
            if k == "ok" and v == 1.0:
                print(k, v)
                return True
        return False
        


# import pymongo
# https://www.mongodb.com/languages/python
def createDatabase():
    client = MongoClient("")


    # mongo
    # show dbs; #< will now show



def console(server_name):
    if server_name in ALL:
        Server(server_name).enter_console()
    else:
        cprint("&cServer not found")

def isSpigotServerOnBungee(): # do in server object
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