from utils.cosmetics import cinput, cprint, cfiglet
from utils.panel_utils import FileInstallException, Panel_Feedback, Panel_Interface
import pyufw as ufw


feedback: Panel_Feedback = Panel_Feedback(True, True, True)


def rules():
    rules = ufw.get_rules()
    cprint("&4UFW Network Rules")
    cprint("&7------------------------")
    for k in rules:
        cprint("&4"+str(k)+":"+str(rules[k]))
    cprint("&7------------------------")


def open_port():
    running = True
    while running:
        feedback.clear()
        rules()
        cprint("&4Open a port")
        cprint("&4type exit to exit")
        cprint("&7------------------------")
        port = cinput("&2Enter a port: ")
        if port.lower() == "exit":
            running = False
            return
        where = cinput("&2What IP can this port be accessed from: ")
        cprint("&7------------------------")
        if where == "all":
            ufw.add(f'allow {port}')
        else:
            ufw.add(f'allow from {where} to any port {port} proto tcp')
        ufw.add('allow 22')
        ufw.reload()


def deny_port():
    running = True
    while running:
        feedback.clear()
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
        ufw.reload()


def delete_rule():
    running = True
    while running:
        feedback.clear()
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

choices = {
    '1': ["Enable", ufw.enable],
    '2': ["Disable", ufw.disable],
    '3': ["Open Port", open_port],
    '4': ["Deny Port", deny_port],
    '5': ["Delete Rule", delete_rule],
}


def on_call(headPanel: Panel_Interface):
    panel = Panel_Interface(choices, "Firewall", "&c", "ufw firewall manager")
    panel.launch()