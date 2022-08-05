from utils.file import CONFIG
from utils.cosmetics import cfiglet, cinput, cprint

from akash_servers import AkashConsole

def getAkashServers(print_output=False) -> dict:
    choices = {}

    servers = CONFIG['akash-servers']

    for idx, server in enumerate(servers):
        choices[str(idx)] = server
        if print_output:
            print(f"[{idx}] {server}")
    return choices



def AkashServerSelector():
    cfiglet("&b", "Akash Selector", clearScreen=True)

    while True:
        choices = getAkashServers(print_output=True)

        server = cinput("\nAkash Server Selector > ")
        if server not in choices or len(server) == 0:
            cprint("\n\n\n&cInvalid Selection")
            continue

        panel = AkashConsole(choices[server])
        panel.enter_console()