from utils.cosmetics import cfiglet, cprint, cinput


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

            'new': ["Create New Instance\n", ServerCreator],

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