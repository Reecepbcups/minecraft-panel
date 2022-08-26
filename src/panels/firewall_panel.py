import os
import json
from pick import pick

from utils.cosmetics import cprint, cinput, cfiglet

from utils.config import CONFIG, saveConfig
from ufw.common import UFWError

CAN_RUN_UFW=True
try:
    import pyufw as ufw
except ModuleNotFoundError as e: 
    cprint("&cUFW is not installed on this system.")
    cprint(f"&epacman -S ufw  |   sudo apt install ufw")
    cprint(f"&epip3 install pyufw  |  pip install pyufw")
    exit(1)
except UFWError as e: # prob not running as root    
    if e.value == "You need to be root to run this script":
        cprint(f"&cUFW Error: To use UFW functions, you must run as root")
        CAN_RUN_UFW=False
    else:
        cprint(f"&cUFW Error: {e.value}")
        CAN_RUN_UFW=False    

'''
To delete rules, you need to edit the config.json, then run 'sfw' to [S]et [F]ire[W]all
'''

def isEnabled() -> bool:
    return ufw.status()['status'] == "active"

def isUserRoot():
    if os.geteuid() != 0:
        print("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.")
        return False
    return True

def setFirewall():
    if isEnabled() == False:
        shouldEnable = cinput("&cFirewall is not enabled. Do you want to enable it? (22 & localhost auto allowed) ([y]/n)") or "y"
        if shouldEnable.lower().startswith("y"):
            cprint("Enabling firewall")
            ufw.enable()
        else:
            cprint("Exiting, you have to enablke the firewall before you can update it")
            return

    ufw.reset()

    # UFW does it in order of of when we add, so always ALLOW first, then DENY
    ufw.add(f"allow 22") 
    ufw.add(f"allow from 127.0.0.1")  
    for ip_addr in CONFIG['firewall']['full-access-ip-connections']:
        ufw.add(f"allow from {ip_addr}")

    for port in CONFIG['firewall']['allow-ports']:
        ufw.add(f"allow {port}")

    for blocked_port in CONFIG['firewall']['blocked-ports']:
        ufw.add(f"deny {blocked_port}")

    # print(ufw.status())

    print("Saving the config here for firewall...")        
    # print(CONFIG)
    saveConfig()


class Firewall():
    '''
    Useful for server creator to denyPort when making without interaction requirement
    '''
    def __init__(self):
        pass

    def isFirewallEnabled(self):
        return isEnabled()

    def denyPort(self, port: int):
        allowed = CONFIG['firewall']['allow-ports']
        blocked = CONFIG['firewall']['blocked-ports']
        if port in allowed:
            print(f"Port {port} was allowed before, removing now...")
            allowed.remove(port)

        if port in blocked:
            print(f"Port {port} is already blocked")
            return # already in there

        if port in [22, 25565]:
            line = "-"*20
            cprint(f"&c{line}")
            cprint(f"&c[!] Wait, are you sure you want to block {port}?")
            cprint(f"&c{line}")
            confirmationMsg = f'Yes I do confirm deny {port}'
            sure = cinput(f"&cIf so, Enter: '{confirmationMsg}'\n>> ")
            if sure != confirmationMsg:
                print(f"Not blocking {port}, phew")
                return
        
        blocked.append(port)
        setFirewall()

    def allowPort(self, port: int):
        allowed = CONFIG['firewall']['allow-ports']
        if port in allowed:
            print(f"Port {port} is already allowed")
            return # already in there
        allowed.append(port)
        setFirewall()

    def removePort(self, configSection, port: int):
        if port not in configSection:
            print(f"Port {port} is not in the config section")
            return
        configSection.remove(port)
        # print(CONFIG)
        setFirewall()

    def addFullAccess(self, ip_address: str):
        allowed = CONFIG['firewall']['full-access-ip-connections']
        if ip_address in allowed:
            print(f"Host {ip_address} is already allowed full access")
            return # already in there
        allowed.append(ip_address)
        setFirewall()
    def removeFullAccess(self, ip_address: str):
        allowed = CONFIG['firewall']['full-access-ip-connections']
        if ip_address not in allowed:
            print(f"Host {ip_address} is not allowed full access...")
            return # already in there
        allowed.remove(ip_address)
        setFirewall()

    

class FirewallPanel():
    def __init__(self):
        if isUserRoot() == False:
            cinput("You must be root to use the firewall feature!\nEnter to continue...")
            # exit(1)
            return

        self.fSettings = CONFIG["firewall"]
        print(self.fSettings)

        self.firewallPanel = {
            'sfw': ["Set Firewall\n", setFirewall],   

            'ap': ["Allow Port", self.addAllowPort],   
            'bp': ["Block Port\n", self.addBlockedPort], 
            'rp': ["Remove Port from config\n", self.removePort], 

            'aah': ["Add allowed Host", self.addAllowedHost],   
            'rah': ["Remove allowed Host\n", self.removeAllowedHost],   

            'r': ["Rules", self.printRules],         
            'c': ["Config", self.printFirewallConfig],         

            "exit": ["exit", exit],
        }

        self.run()

    def run(self): 
        cfiglet("&e", "Firewall Panel", clearScreen=True)        
        cprint(f"Is Firewall Enabled: {isEnabled()}")

        while True:      
            for k, v in self.firewallPanel.items():
                cprint(f"[{k}]\t {v[0]}")

            # Split it into args so we can pass through functions? This needed?
            request = cinput("\nFW> ")
            if request == "cp":
                import panels.main_panel as main_panel
                main_panel.MainPanel()
            if request not in self.firewallPanel.keys():
                cprint(f"\t&c{request} not in firewall panel")
                continue
            self.firewallPanel[request][1]() 
            cfiglet("&e", "Firewall Panel", clearScreen=False) 
            cprint(f"Is Firewall Enabled: {isEnabled()}\n")

    def getRulesList(self) -> list:
        rules = ufw.get_rules()
        ipv4Rules = []
        for idx in rules:
            rule = rules[idx]
            if rule not in ipv4Rules:
                ipv4Rules.append(rule)
        return ipv4Rules

    def getRulesEnumerated(self) -> dict:
        return ufw.get_rules()

    def printRules(self) -> None:
        os.system("ufw status numbered")
        cinput("\nPress enter to continue...")

    def printFirewallConfig(self):
        for k in CONFIG["firewall"].keys():
            print(f"\n{k}:\n  {CONFIG['firewall'][k]}")
        cinput("\nPress enter to continue...")

    def removePort(self):
        options = ['allow-ports', 'blocked-ports']
        selection = pick(options, "Which section:", indicator=' =>', multiselect=False)
        keySelection = selection[0]
        key = CONFIG['firewall'][keySelection]

        selected = pick(key, "Remove which?", indicator=' =>', multiselect=False)
        portToRemove = selected[0]
        submit = cinput(f"Confirm you want to remove {portToRemove} port from {keySelection} ([y]/n): ") or 'y'
        if submit.lower() == 'y':
            Firewall().removePort(key, portToRemove)
        else:
            print("Passing...")


    def addAllowPort(self):
        port = int(cinput("Port to allow to anyone: "))
        Firewall().allowPort(port)
    def addBlockedPort(self):
        port = int(cinput("Port to block: "))
        Firewall().denyPort(port)

    def addAllowedHost(self):
        host = cinput("Host to allow to full backend PORT access too: ")
        Firewall().addFullAccess(host)
    def removeAllowedHost(self):
        # host = cinput("Host to remove from all backend port access: ")
        options = CONFIG['firewall']['full-access-ip-connections']
        selected = pick(options, "Remove allowed host:", indicator=' =>', multiselect=False)
        host = selected[0]
        y = cinput(f"Confirm you want to remove {host} ([y]/n)") or 'y'
        if y.lower().startswith('y'):
            Firewall().removeFullAccess(host)
        else:
            cprint("Passing...")
    


if __name__ == "__main__":
    pass