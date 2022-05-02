
# Make an API for when a user types in CLI arguments, to do that here

from utils.cosmetics import cprint

def startAllServers(listOfArgs):
    # This is not actually used here, but useful for sub command arguments
    print("Starting all servers " + str(listOfArgs))
    pass

possibleArgs = {
    "start-all": startAllServers,
}

def _printValidUsage():
    cprint("&cCLI Usage: ")
    for arg, func in possibleArgs.items():
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