from utils.cosmetics import cprint, cinput


from server_creator import ServerCreator    

class AdminPanel:
    '''
    This class is the user panel which wraps Database class.
    This is for user input & should wrap those functions
    '''
    def __init__(self):
        self.adminFunctions = {
            # "l": ["ClearAllLogs", clear_all_logs],
            # "port": ["Fix Broken Port\n", print],

            'new': ["Create New Instance", ServerCreator]

            # "UAC": ["Enable user access control", userAccessControl],
        }

        while True:
            # cfiglet("&3", "Control Panel", clearScreen=True)
            for k, v in self.adminFunctions.items():
                cprint(f"[{k}]\t {v[0]}")

            # Split it into args so we can pass through functions? This needed?
            request = input("\nADMIN> ")
            self.adminFunctions[request][1]() 