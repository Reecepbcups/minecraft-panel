from multiprocessing.connection import wait
import time
from wsgiref.simple_server import server_version
from utils.file_utils import CONFIG, RUNNING, chdir, get_screen_pid
from utils.cosmetics import cprint, cinput
from utils.killable_thread import thread_with_trace
from utils.panel_utils import Panel_Interface
import subprocess
import os

proxies = ["Waterfall"]

class ServerPanel():

    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)
        if RUNNING.get(self.name) == None:
            RUNNING.set(self.name, False)
        RUNNING.save()

        
        self.choices = {
            '1': ["Start", self.start_server],
            '2': ["Stop", self.stop_server],
            '3': ["Restart", self.restart_server],
            '4': ["Console", self.enter_console],
        }
        self.panel = Panel_Interface(self.choices, self.name, "&2")
    
    
    def display(self):
        self.panel.launch()
    

    def start_server(self):
        if RUNNING.get(self.name):
            cprint("&cYou can't start a server that is already running")
            self.panel.feedback.pause_panel()
            return

        wd = chdir(self.path) 
        os.system(f'screen -S {self.name} -d -m ./start.sh')
        os.chdir(wd)
        cprint("&aServer Started")
        
        RUNNING.set(self.name, True)
        RUNNING.save()

        self.panel.feedback.pause_panel()
    

    def stop_server(self):
        if not RUNNING.get(self.name):
            cprint("&cYou can't stop a server that isn't running")
            self.panel.feedback.pause_panel()
            return
        
        pid = get_screen_pid(self.name)
        subprocess.call(['screen', '-XS', f'{pid}', 'quit'])
        cprint("&4 Stopped the server")     
        RUNNING.set(self.name, False)
        RUNNING.save()   

        self.panel.feedback.pause_panel()


    def restart_server(self):
        if not RUNNING.get(self.name):
            self.stop_server()
            cprint("&cWaiting...")
            wait(5)
        self.start_server()
    

    def enter_console(self):
        console = thread_with_trace(target=self.follow)
        console.start()

        running = True
        while running:
            user_input = input()
            if user_input == "\x18":
                running = False
            elif user_input == "restart":
                running = False
                self.restart_server()
            elif user_input == "stop":
                running = False
                self.stop_server()
            else:
                self.server_input(user_input)
        
        console.kill()
        console.join(timeout=0.05)

    def server_input(self, user_input):
        subprocess.call(['screen', '-S', f'{self.name}', '-X', 'stuff', f'{user_input}\015'])


    def follow(self):
        relative_log_location = "logs/latest.log" 
        with open(f'{self.path}/{relative_log_location}') as log:
            log.seek(0, os.SEEK_END)

            while True:
                line = log.readline()
                if not line:
                    time.sleep(0.1)
                    continue
                
                cprint(line.replace("\n", ""))

        

def fetch_servers(choices: dict):
    serverloc = CONFIG.get("serverloc")
    if not os.path.exists(serverloc):
        cprint(
            f'''
            &cYou don't have any servers yet create servers using 
            the server creator or change the paths in the config.yml
            your config location is: {os.getcwd() + "/configs/config.yml"}
            ''')

    count = 1
    # serverloc servers
    for server in os.listdir(serverloc):
        choices[str(count)] = [server, ServerPanel(serverloc+"/"+server).display]
        count += 1
    
    # External Servers not in serverloc
    external_servers = CONFIG.get("external_servers")
    if external_servers is None:
        pass
    else:
        for server in external_servers:
            choices[str(count)] = [os.path.basename(server), ServerPanel(server).panel]
            count +=1


def on_call(headPanel: Panel_Interface):
    choices = {}
    fetch_servers(choices)
    panel = Panel_Interface(choices, "Server Manager", "&b", "An Example Panel")
    panel.launch()
    