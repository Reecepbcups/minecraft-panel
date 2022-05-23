from utils.cosmetics import cfiglet, cprint, cinput


from server_creator import ServerCreator    

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
'''

import os
def _saveENVPairs(pairs: dict):
    print(pairs)
    home = os.path.expanduser("~") + "/.bashrc"

    for k, v in pairs.items():
        print("Setting ENV Variable in bashrc: " + f"export {k}={v}")    
        with open(home, "a") as f:
            f.write(f"export {k}={v}\n")

    cprint(f"\n\n&c[!] RUN: &asource {home}")
    exit()

def setENVVariable():
    pairs = {}

    cprint("&cAdd as many key,value pairs as you want.")
    cprint("&f- Type 'exit' to stop & save to file")
    cprint("&f- Type 'show' to show all pairs")
    while True:
        cprint("-"*25)
        key = cinput("&f\nEnter the ENV Variable &ekey &f> ")
        value = cinput("&fEnter the ENV Variable &evalue &f> ")
        if key == "exit" or value == "exit":
            _saveENVPairs(pairs)
        elif key == "show" or value == "show":
            print(pairs)
        else:
            pairs[key] = value
    

class AdminPanel:
    '''
    This class is the user panel which wraps Database class.
    This is for user input & should wrap those functions
    '''
    def __init__(self):
        self.adminFunctions = {
            # "l": ["ClearAllLogs", clear_all_logs],
            # "port": ["Fix Broken Port\n", print],

            'new': ["Create New Instance\n", ServerCreator],

            'firewall': ["Firewall\n", print], # firewall panel with options to use the class

            'web-short': ["Link Shortener\n", print],

            'env': ["OS ENV Variables\n", setENVVariable],

            "cp": ["Main Menu", print],
            "exit": ["Exit", exit]

            # "UAC": ["Enable user access control", userAccessControl],
        }

        cfiglet("&c", "Admin Panel", clearScreen=True)

        while True:
            # cfiglet("&3", "Control Panel", clearScreen=True)
            for k, v in self.adminFunctions.items():
                cprint(f"[{k}]\t {v[0]}")

            # Split it into args so we can pass through functions? This needed?
            request = cinput("\nADMIN> ")
            if request == "cp":
                from console import main
                main()
            self.adminFunctions[request][1]() 