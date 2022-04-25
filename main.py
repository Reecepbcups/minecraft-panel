from importlib import import_module
from utils.file_utils import gather_plugins
from utils.cosmetics import cprint
from utils.panel_utils import Panel_Interface 
import native_components.server_creator as screator
import native_components.server_manager as smanager
import native_components.firewall as firewall
import time
import os

choices = {
    '1': ["Server Creator", screator.on_call],
    '2': ["Server Manager", smanager.on_call],
    '3': ["Firewall", firewall.on_call],
}

if __name__ == "__main__":
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
