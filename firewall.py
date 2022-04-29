import pyufw as ufw
import yaml
from utils.cosmetics import cinput, cprint
from utils.yaml_utils import Yaml

'''
Should read rules from config.yml



# On a server startup IF behind bungee,
#  we should automatically check if that port is backlisted from outside connections.
# Part of Server logic.
'''



def rules(): # TODO: Remove duplicates values in the rules set
    rules = ufw.get_rules()
    cprint("&4UFW Network Rules")
    cprint("&7------------------------")
    print(rules)
    for idx in rules:
        cprint("&4"+str(idx)+":"+str(rules[idx]))

    cprint("&7------------------------")

def open_port():
    while True:
        rules()
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
v = Yaml("config.yml").loadConfig() # get this from CONFIG in utils.file_utils

firewallSettings = v.get("firewall")
# print(firewallSettings)
allowOpenAccess = firewallSettings['allow-ports']
allowExternalAccess = firewallSettings['full-access-ip-connections']

def allowPortsFromConfig():
    for port in allowOpenAccess:
        ufw.add(f'allow {port}')
    ufw.add(f'allow 22') # always ensure we can SSH in.

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

enableFirewall()
rules()