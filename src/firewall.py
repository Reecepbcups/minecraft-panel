import pyufw as ufw
import os, subprocess
from utils_cosmetics import cinput, cprint
from utils_yaml import Yaml

'''
Should read rules from config.yml

# On a server startup IF behind bungee,
#  we should automatically check if that port is backlisted from outside connections.
# Part of Server logic.
'''

from config import CONFIG

import platform
def checkIfSystemIsUbuntuOrArch() -> str:
    distr = platform.dist()[0]
    if distr in ['Ubuntu', "Debian"]:
        return "apt-get install"
    elif distr in ['Arch']:
        return "pacman -S"
    else:
        return '<package manager> install'

def isUFWinstalled() -> bool:
    try:
        subprocess.check_call(['ufw', 'status'])
    except:
        cprint("&cUFW is not installed on this system.")
        cprint(f"&e{checkIfSystemIsUbuntuOrArch()} ufw")
        exit(1)

def isUserRoot():
    if os.geteuid() != 0:
        print("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.")
        return False
    return True

class Firewall():
    def __init__(self):
        if isUserRoot() == False:
            exit(1)

        firewallSettings = CONFIG.get("firewall")
        # print(firewallSettings)
        self.openAccessPorts = firewallSettings['allow-ports']
        self.ExternalIPFullAccess = firewallSettings['full-access-ip-connections']

    def __str__(self) -> str:
        openPorts = self.openAccessPorts
        fullAccessIPs = self.ExternalIPFullAccess
        return f"Firewall; {openPorts=}; {fullAccessIPs=}"  

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

    def _port(self, port=0, hostIP="", action="allow", debug=False):
        '''
        Builds a rule for ufw.
        - Set port = -1 to allow all ports from a host
        - action should = 'allow', 'deny', 'reject', 'limit', 'route'        
        '''
        if port == -1:
            ufw.add(f"allow from {hostIP} to any")
        elif port == 0:
            cprint("No port specified")
            return

        strOutput = f"{action}ing port {port}"
        output = f"{action} {port}"

        if len(hostIP) > 0:
            strOutput = f"{action}ing {hostIP} to access port {port}"
            output = f"{action} from {hostIP} to any port {port}"

        if debug: print(strOutput)
        ufw.add(output)

    def allowPort(self, port, hostIP=""):
        self._port(port, hostIP, "allow")

    def denyPort(self, port, hostIP=""):
        self._port(port, hostIP, "deny")
 
    def deleteRule(self, rule=""):
        ufw.delete(rule)

    def allowPortsFromConfig(self, debug=False):
        if len(self.openAccessPorts) == 0:
            cprint("No ports to open from config.yml")
            return

        for port in self.openAccessPorts:
            self.allowPort(port)
            if debug:
                cprint(f"Opened port {port}")
        self.allowPort(22)

    def allowFullAccessToWhitelistedConfigAddresses(self, debug=False):
        if len(self.ExternalIPFullAccess) == 0:
            cprint("No IPs to open full access to from config.yml")
            return

        for ip in self.ExternalIPFullAccess:
            self.allowPort(-1, ip)
            if debug: cprint(f"Opened full access to {ip}")

        self.allowPort(-1, "127.0.0.1") # Default always allow 127.0.0.1 to connect to itself

    def isPortClosedCheck(port, hostIP="127.0.0.1", debug=False) -> bool:
        '''
        Checks if a port is open using telnet
        '''
        from socket import socket, create_connection
        sock = socket(socket.AF_INET, socket.SOCK_STREAM)
        result = create_connection((hostIP, port))
        if result == 0: # port is not closed
            if debug: print(f"Port {port} is open on {hostIP}")
            return False
        else:
            if debug: print(f"Port {port} is closed on {hostIP}")
            return True

    def print(self):
        print(self.__str__())  


f = Firewall()
# f.allowPort(52, "134.5.5.5")
# print(f.getRulesList())
# f.allowFullAccessToWhitelistedConfigAddresses()
f.print()
exit()

def open_port():
    while True:
        # rules()
        cprint("&4Open a port")
        cprint("&4type exit to exit")
        cprint("&7------------------------")
        port = cinput("&2Enter a port: ")
        if port.lower() == "exit":
            return
        where = cinput("&2What IP can this port be accessed from (default localhost): ")
        cprint("&7------------------------")
        if where == "all":
            ufw.add(f'allow {port}')
        else:
            ufw.add(f'allow from {where} to any port {port} proto tcp')
        ufw.add('allow 22/tcp')
        ufw.reload()

def deny_port():
    running = True
    while running:
        rules()
        cprint("&4Close a Port")
        cprint("&4type exit to exit")
        cprint("&7------------------------")
        port = cinput("&2Enter a port: ")
        if port.lower() == "exit":
            running = False
            return
        cprint("&7------------------------")
        ufw.add(f'deny {port}')
        ufw.add('allow 22/tcp') # always ensure we can ssh
        ufw.reload()

def delete_rule():
    running = True
    while running:
        rules()
        cprint("&4Delete a Rule")
        cprint("&4* -> delete all rules")
        cprint("&4exit -> exit section")
        cprint("&7------------------------")
        rule = cinput("&2Enter a rule: ")
        if rule.lower() == "exit":
            running = False
            return
        cprint("&7------------------------")
        ufw.delete(rule)
        ufw.reload()


# rules()
# open_port()

# print(ufw.show_added()) # {1: 'allow 88', 2: 'allow 22', 3: 'allow 88', 4: 'allow 22'}

# NO print(ufw.show_raw())

# print(ufw.status())
# print(ufw._get_enabled())
# ufw.delete('*')

# ufw.set_logging('full') # on, off, medium, high, full
# ufw.reset()



# Testing






def allowExternalFullAccess():
    for ip in allowExternalAccess:
        ufw.add(f'allow from {ip} to any')
    ufw.add(f'allow from 127.0.0.1 to any') # ensure localhost always has access to itself

def denyPort(host, port):
    # ensure this host is not in full-access-ip-connections, if so alert the user you cant block their ports
    if host in allowExternalAccess:
        cprint("&cYou cannot block this host's ports, as it is in the full-access-ip-connections list.")
        return
    if host == '127.0.0.1':
        cinput("You want to block localhost port? Press enter to continue if so, else ctrl+c.")

    ufw.add(f"deny from {host} to any port {port}")
    pass

def reset():
    ufw.reset()

def enableFirewall():
    ufw.enable()

# allowPortsFromConfig()
# rules()

# enableFirewall()
# rules()