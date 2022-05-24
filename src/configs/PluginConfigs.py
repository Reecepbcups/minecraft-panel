import random
import string

class PluginConfigs:
    def __init__(self):
        pass

    def getConfigs(self):
        return {
            "LuckPerms": self.LuckPerms, 
            "SecuredNetwork": self.SecuredNetwork,
        }
        
    def getAvailableConfigs(self) -> list:
        return list(self.getConfigs().keys())

    def run(self, name) -> str:
        if name not in self.getAvailableConfigs():
            raise Exception(f"{name} is not a valid config")
        # calls the given function for its name
        return self.getConfigs()[name]()
        

    def LuckPerms(self):
        cfgInstance = [
            '# https://luckperms.net/wiki/Configuration#environment-variables'
        ]

        cfgInstance.append(f"server: {input('Luckperms Server (global): ') or 'global'}")
        cfgInstance.append(f"use-server-uuid-cache: {input('Luckperms server uuid cache (false): ') or 'false'}")

        storageMethod = input('Luckperms Storage method ([h2],MongoDB,MariaDB,YAML,JSON): ') or 'h2'
        cfgInstance.append(f"storage-method: {storageMethod}")
        
        cfgInstance.append("sync-minutes: -1")
        cfgInstance.append("watch-files: true")
        cfgInstance.append("auto-push-updates: true")
        cfgInstance.append("push-log-entries: true")
        cfgInstance.append("broadcast-received-log-entries: true")
        cfgInstance.append("log-notify: true")

        cfgInstance.append("data:")
        if storageMethod.lower() == "mongodb":
            cfgInstance.append(f"  mongodb-collection-prefix: {input('Luckperms collection prefix (''): ') or ''}")
            cfgInstance.append(f"  mongodb-connection-uri: {input('Luckperms Mongo mongodb://uri... (''): ') or ''}")
        elif storageMethod.lower() in ['mariadb', 'mysql']:
            cfgInstance.append(f"  address: {input('Luckperms DB Address (localhost): ') or 'localhost'}")
            cfgInstance.append(f"  database: {input('Luckperms DB Name (luckperms): ') or 'luckperms'}")
            cfgInstance.append(f"  username: {input('Luckperms User (root): ') or 'root'}")
            cfgInstance.append(f"  password: {input('Luckperms Password: ') or ''}")

        msgService = input('Luckperms Message Service ([pluginmsg],sql,redis): ') or 'pluginmsg'
        cfgInstance.append(f"messaging-service: {msgService}")
        if msgService.lower() == "redis":
            cfgInstance.append(f"redis:")
            cfgInstance.append(f"  enabled: true")
            cfgInstance.append(f"  address: {input('Luckperms Redis Instance (localhost:6379): ') or 'localhost:6379'}")
            cfgInstance.append(f"  username: {input('Luckperms Redis username: ') or ''}")
            cfgInstance.append(f"  password: {input('Luckperms Redis Password: ') or ''}")

        return '\n'.join(cfgInstance)

    def SecuredNetwork(self):
        cfgInstance = [
            '# https://www.spigotmc.org/resources/securednetwork-1-7-1-18-protect-your-network-from-ip-forward-bypass-exploit.65075/reviews',            '# https://discord.com/invite/BbhADEy',
            '# - It is recommended to change this once in a while. Generate a new one using "/sn generate".'            
        ]

        option = input("SecuredNetwork. New random secret or use existing? ((new)/e): ") or 'n'
        secret = ""
        if option.startswith('n'):
            secretLen = input(f'SecuredNetwork secret length (50): ') or 50
            secret = ''.join(random.choice(string.ascii_letters + "123456789_") for i in range(int(secretLen))) 
            print(f'SecuredNetwork secret: {secret}. Ensure this is in your bungee as well')
        else:
            while secret == "":
                secret = input("SecuredNetwork, Your Secret: ") or ""
        
        cfgInstance.append(f"passphrase: {secret}")
        cfgInstance.append(f"metrics: false")
        return '\n'.join(cfgInstance)

if __name__ == "__main__":
    pc = PluginConfigs()
    # print(pc.getAllConfigs())
    
    # newC = pc.LuckPerms()
    # print(newC)

    # sNetwork = pc.SecuredNetwork()
    # print(sNetwork)