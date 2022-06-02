import os
from utils.cosmetics import cprint, cinput, cfiglet
from cryptocode import encrypt, decrypt
import ast
from pick import pick
from typing import Tuple
import json

# This can be reduced with having a parent class for database_panel as well
class RedisPanel():
    def __init__(self):
        self.r = RedisServerCache()
        self.uri = ""
        self.currentServer = "" # changes with each URI change
        self.redisPanel = {
            "suri": ["Show URI\n", self.showURI],
            "ch": ["Change Active Instance", self._change_uri],
            "sh": [f"Server Shell", self.connectToServer],

            "add": ["Add a New Redis Instance\n", self.addInstance],        

            "exit": ["exit", exit],
        }
        self.run()

    def run(self): 
        cfiglet("&4", "Redis Panel", clearScreen=True)               
        while True: 
            if len(self.currentServer) > 0:
                cprint(f"\t&eCurrent connected server: {self.currentServer}\n")        
            for k, v in self.redisPanel.items():
                cprint(f"[{k}]\t {v[0]}")

            # Split it into args so we can pass through functions? This needed?
            request = cinput("\nREDIS> ")
            if request == "cp":
                from console import main
                main()
            if request not in self.redisPanel.keys():
                cprint(f"\t&c{request} not in database panel")
                continue
            self.redisPanel[request][1]() 
            cfiglet("&4", "Redis Panel", clearScreen=False)  

    def showURI(self):
        if len(self.uri) == 0:
            self._change_uri()        
        print(self.uri)

    def connectToServer(self):        
        self._set_server_uri()
        self.r.connectToServer(self.uri)

    def addInstance(self):
        self.r.newServer()

    def _set_server_uri(self):
        if len(self.uri) > 0:
            return self.uri
        self._change_uri()
        return self.uri        
    def _change_uri(self):
        server, serverName = self.r.decryptServer()
        if server == {} and serverName == "":            
            return
        self.uri = self.r.serverInfoToURI(server, debug=False)
        # self.mFuncs = MongoHelper(self.uri)
        self.currentServer = serverName



# Is used in database_panel.py as well. Need to reduce this
class RedisServerCache:
    '''
    ServerCache which handles the file, encrypting, decrypting, and URI information
    '''
    def __init__(self, file_name="cache_redisdb.json"):
        # Gets the root folder (where the readme, config.json are)
        self.location = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.FILE_NAME = f"{self.location}/{file_name}"
        # print(self.FILE_NAME)
        self.servers = self._loadServersFromJSON()  

    def _askPassword(self, text="&eEnter your password to encrypt >> "):
        return cinput(text)

    def decryptServer(self, server='') -> Tuple[dict, str]:      
        if len(server) == 0:  
            server, _ = pick(list(self.servers.keys()), 'Redis Server to Connect too: ', multiselect=False, indicator=' =>')

        cprint(f"\n&a[!] Selected server: {server}")
        
        dec_obj_str = decrypt(self.servers[server], self._askPassword("&eEnter password to unlock &f>> "))
            # print(f"{dec_obj_str}") # prints dict of all values
        # converts object to a dict from string        
        return ast.literal_eval(dec_obj_str), server

    def serverInfoToURI(self, decryptedServerInfo: dict, debug=False) -> str:
        fmt = "redis://{password}@{addr}:{port}"
        uri = fmt.format(**decryptedServerInfo)
        if debug: print(uri)
        return uri

    def connectToServer(self, uri):
        os.system(f"redis-cli -u {uri}")

    def printServers(self):
        print(', '.join(self.servers.keys()))

    def newServer(self):
        server_name = input("New Redis Instance Name: ") or 'myServer'
        tempObj = {
            "addr": input("Enter IP Address/URL (127.0.0.1): ") or '127.0.0.1',
            "port": input("Enter Port (6379): ") or 6379,
            # "user": input("Enter Username (''): ") or '',            
            "password": input("Enter Password: ") or 'password',
        }

        # removes http(s):// & the / at the end
        if tempObj['addr'].startswith("http"):
            tempObj['addr'] = tempObj['addr'].split("//")[-1]
        if tempObj['addr'].endswith("/"):
            tempObj['addr'] = tempObj['addr'][:-1]

        tempObj['port'] = int(tempObj['port'])

        myPass = self._askPassword()
        confirmPass = self._askPassword("Confirm Password: ")
        if myPass != confirmPass:
            print("Passwords do not match")
            self.newServer()

        enc_obj = encrypt(str(tempObj), myPass)

        self.servers[server_name] = enc_obj
        self._saveServersToJSON()

        print(f"Saved {server_name} as {enc_obj}")
    
    def _saveServersToJSON(self):
        with open(self.FILE_NAME, "w") as f:
            json.dump(self.servers, f, indent=4)

    def _loadServersFromJSON(self) -> dict:
        if not os.path.exists(self.FILE_NAME):
            with open(self.FILE_NAME, "w") as f:
                json.dump({}, f)
                return {}

        with open(self.FILE_NAME, "r") as f:
            return json.load(f)