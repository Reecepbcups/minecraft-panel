
# Make an API for when a user types in CLI arguments, to do that here

from os.path import dirname as parentDir

from server import Server
from utils.cosmetics import cprint
from utils.backup import Backup


def startAllServers(listOfArgs):
    # This is not actually used here, but useful for sub command arguments
    print("Starting all servers " + str(listOfArgs))
    pass

from utils.config import CONFIG


def path(empyList):
    # print(f"{CONFIG['PANEL_DIRECTORY']}")
    print(parentDir(parentDir(__file__)))

def showLogs(args):
    serverName, numOfLines = args[0], int(args[1])
    s = Server(serverName)
    s.showLogOnce(numOfLines)

possibleArgs = {
    "start-all": startAllServers,
    "path": path,
    "show-logs": showLogs,
    "backup": Backup,
}

def _printValidUsage():
    cprint("&cCLI Usage: ")
    for arg in possibleArgs.keys():
        cprint(f"&fconsole {arg}")
    print()

def call(args) -> bool:
    '''
    Calls and does the requested action in teh CLI. True if done without error.
    '''
    # print("System arguments found! Using API call")

    mainArg = args[0]
    args = args[1:]

    if mainArg not in possibleArgs:
        cprint(f"&c\nInvalid Argument {mainArg}")
        _printValidUsage()
        return False

    # Call the function
    possibleArgs[mainArg](args)
    return True
