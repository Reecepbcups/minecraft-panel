# Default imports every python3 isntall has
import subprocess, platform, os, time


# from importlib.util import find_spec
# from utils.package_utils import installPackage
# for package_name in ['pyfiglet', 'pyufw', 'PyYAML', 'requests']:
#     if find_spec(package_name) is None:
#         print(package_name +" is not installed. Ensure you install pip & the requirements.txt")
#         installPackage(package_name)

from importlib import import_module
from utils.file_utils import gather_plugins
from utils.cosmetics import cprint
from utils.panel_utils import Panel_Interface 
import native_components.server_creator as screator
import native_components.server_manager as smanager
import native_components.firewall as firewall


choices = {
    '1': ["Server Creator", screator.on_call],
    '2': ["Server Manager", smanager.on_call],
    '3': ["Firewall", firewall.on_call],
}

def main():
    plugins = gather_plugins()
    start = time.time()*1000

    curdex = len(choices.keys())+1
    for key in plugins:
        temp_import = import_module("plugins."+plugins[key])
        choices[str(curdex)] = [key, temp_import.on_call]
        curdex+=1
    end = time.time()*1000
    cprint(f'&aLoaded all plugins in {end-start} miliseconds')

    panel = Panel_Interface(choices, "MCAdminPanel", "&4", "A Minecraft Python Administrator panel", "self")
    panel.launch()

if __name__ == "__main__":

    # exit(0)

    main()
