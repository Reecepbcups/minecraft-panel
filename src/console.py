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
from firewall import Firewall
from server_creator import ServerCreator
from database import Database
from utils.system import checkIfRequirementsAreInstalled

import time, os

# Load this before anything else
serverGroups = CONFIG.get('servers') # 'proxy' & 'spigot'
PROXIES = serverGroups['proxy']
SERVERS = serverGroups['spigot']
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

# client = MongoClient('example.com',
                    #  username='user',
                    #  password='password',
                    #  authSource='the_database',
                    #  authMechanism='SCRAM-SHA-256')

def userAccessControl():
    # Add check here to see if UAC is enabled
    adminUsername = input("Admin Username: ")
    adminPassword = input("Admin Password: ")
    db = Database("mongodb://127.0.0.1:27017/") # bc no auth yet
    db.enableMongoDBAuthentication(adminUsername, adminPassword)
    # Then you do what it says to do in this functiuon ^

def databasePanel():
    databaseFunctions = {
        "1": ["Create DB", print],
        "2": ["Delete DB", print],
        "3": ["Show DBS", print],

        "4": ["Create User", print],
        "5": ["Delete User", print],
        "6": ["Show Users\n", print],

        "UAC": ["Enable user access control", userAccessControl],
        # find collection
    }

    # Login to database. Input Username. If so, show the user that database.
    # Confirm. Then ask for password. Put into URI

    ## Login
    user = 'myUserAdmin' #input("Username: ")

    users = CONFIG.get("Mongo-Authentication")
    if user in users:
        authSource = users[user]
    else:
        authSource = input("Authentication Database: ")

    password = 'password123' #input("Password: ")
    ip_addr = "127.0.0.1:27017" #input("Auth IP (127.0.0.1:27017): ")
    uri = f"mongodb://{user}:{password}@{ip_addr}/?authSource={authSource}"
    dbObj = Database(uri)

    databases = dbObj.listDatabases()
    print(databases)

    # print(dbObj.listUsers('test'))

    # dbObj.createNewUser('newDB', 'mynewDBUser', 'test', [])

    # cfiglet("&a", "Database Panel", clearScreen=True)
    # for k, v in databaseFunctions.items():
    #     cprint(f"[{k}]\t {v[0]}")
    # request = input("\nDATABASE> ")
    # databaseFunctions[request][1] # check if is object or is a function with (). Then do the opposite?


def adminpanel():
    # "l": ["ClearAllLogs", clear_all_logs],
    pass

def main():

    # databasePanel(); exit(0)

    from utils.screen import get_all_active_screens
    controlPanel = {        
        "1": ["Console", ServerSelector],
        "2": ["List Running Servers", get_all_active_screens],
        "3": ["StartAllServers", startAllServers],
        "port": ["Fix Broken Port\n", print],

        "ADMIN": ["&cAdmin Panel&r", adminpanel],
        "DB": ["&aDatabase Functions&r", databasePanel],
    }

    # isSpigotServerOnBungee("test")
    
    # # 'Enable Access Control' `mongodb://myDBReader:password@127.0.0.1:27017/?authSource=admin`.
    # # mongo -u myUserAdmin -p OR mongo, then 'use admin; db.auth("myUserAdmin", "password123");'
    # database = Database("mongodb://myUserAdmin:password123@127.0.0.1:27017/?authSource=admin") 
    # # database = Database("mongodb://127.0.0.1:27017/")
    # dbs = database.listDatabases()
    # print(dbs)
    # database.dropDatabase("test_db", debug=True)
    # # print(database.listDatabaseRoles("admin"))
    # print("admin db users:", database.listUsers(database_name="admin"))
    # database.enableMongoDBAuthentication()
    # # creates user on the test database, with roles to access other databases as well. This means the myTester user MUST auth with the test database in the uri
    # # mongo -u myTester -p --authenticationDatabase test OR mongo, then 'use test; db.auth("myTester", "myPassXYZ");'
    # database.createNewUser("test", "myTester", "myPassXYZ", [{'role': 'readWrite', 'db': 'test'}, {'role': 'read', 'db': 'test_db'}])
    # print("test db users:", database.listUsers(database_name="test"))
    # database.changeUsersPassword("test", "myTester")
    # database.createTestCollection(collection_name="test-s", database_name="test")
    # print("="*20)
    # # database.createNewUser("test", "testingacc", "myPassXYZ", [{'role': 'readWrite', 'db': 'test'}])
    # print("test db users:", database.listUsers(database_name="test"))
    # database.deleteUser("test", "testingacc")
    # print("test db users:", database.listUsers(database_name="test"))


    # collections = database.listCollections("admin")
    # print(collections)

    # print(Server('proxy').getInformation())
    # print(is_screen_running("test"))

    cfiglet("&3", "Control Panel", clearScreen=True)
    for k, v in controlPanel.items():
        cprint(f"[{k}]\t {v[0]}")
    request = input("\nCP> ")

    controlPanel[request][1]() # Could make args here & pass into all sub options. Then the underlying functions can use
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

    panel = Server(choices[server])
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