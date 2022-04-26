# Default imports every python3 isntall has


# https://stackoverflow.com/questions/9002275/how-to-build-a-single-python-file-from-multiple-scripts

from importlib import import_module
from utils.file_utils import gather_plugins
from utils.cosmetics import cprint
from utils.panel_utils import Panel_Interface 
import native_components.server_creator as screator
import native_components.server_manager as smanager
import native_components.firewall as firewall
import time

controlPanel = {
    '1': ["Console", smanager.on_call],
    'admin': ["Admin Panel", smanager.on_call],
}

adminPanel = {
    '2': ["Server Creator", screator.on_call],
    '3': ["Firewall", firewall.on_call],
}

def main():
    plugins = gather_plugins()
    start = time.time()*1000

    curdex = len(controlPanel.keys())+1
    for key in plugins:
        temp_import = import_module("plugins."+plugins[key])
        controlPanel[str(curdex)] = [key, temp_import.on_call]
        curdex+=1
    end = time.time()*1000
    cprint(f'&aLoaded all plugins in {end-start} miliseconds')

    panel = Panel_Interface(controlPanel, "Control Panel", "&3", None, "self")
    panel.launch()

if __name__ == "__main__":
    main()
