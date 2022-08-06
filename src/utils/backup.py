from dataclasses import fields
from utils.file import CONFIG
from utils.cosmetics import cfiglet, cinput, cprint
from pick import pick

from utils.system import getStorageAmount, getRamUsage

from datetime import datetime
import zipfile
import pysftp
import re
import os

def getBackupConfig(print_output=False) -> dict:
    backup_data = CONFIG['backups']
    return backup_data

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
TIME_FORMAT = '%b-%d-%Y_%I-%M-%S%p'

class Backup:
    '''
    Create a class which can zip files & ignore files if they match any given regex expression.
    It should take in the ROOT_PATH to start to compile. THen loop through all sub directories and files
    '''

    def __init__(self, debug=False, showIgnored=True, showSuccess=True):
        self.current_time = datetime.now().strftime(TIME_FORMAT)
        self.showIgnored = showIgnored
        self.showSuccess = showSuccess

    # check if backups is in config
        if not 'backups' in CONFIG:
            cprint("&cNo backup section in config, grab example from 'config.json.example'")
            exit(0)

        self.root_paths = CONFIG['backups']['parent-paths']
        self.backup_path = CONFIG['backups']['save-location']
        self.max_local_backups = CONFIG['backups']['max-local-backups']

        # make directory if it doesn't exist
        if not os.path.exists(self.backup_path):
            os.makedirs(self.backup_path)

        self.discord_webook = CONFIG['backups']['discord-webhook']
        self.debug = debug
        self.save_relative = CONFIG['backups']['save-relative']
        
        self.server_name = CONFIG['backups']['server-name']
        self.zipfilename = f"{self.server_name}_{self.current_time}.zip"
        self.backup_file_name = os.path.join(self.backup_path, self.zipfilename)
        

    def zip_files(self):
        self.zip_file = zipfile.ZipFile(self.backup_file_name, "w", compression=zipfile.ZIP_DEFLATED)

        for root_path in self.root_paths:            
            if not os.path.isdir(root_path):
                cprint(f"&c{root_path} is not a directory, ignoring...")
                continue

            ignore_regex = CONFIG['backups']['parent-paths'][root_path]
            print(root_path, ignore_regex)            

            for root, dirs, files in os.walk(root_path):        
                for file in files:
                    abs_path = os.path.join(root, file)
                    relative_filename = str(abs_path).replace(root_path, "")
                    # print('"' + abs_path + '",'); continue

                    if not any(re.search(regex, abs_path) for regex in ignore_regex):
                        if self.save_relative:
                            self.zip_file.write(abs_path, arcname=relative_filename) # saves just from the rooth path onwards
                        else:
                            self.zip_file.write(os.path.join(root, file)) # saves them as teh full abs path      
                        if self.debug and self.showSuccess:
                            cprint(f"&a{relative_filename}")                  
                    else:
                        if self.debug and self.showIgnored: 
                            cprint(f"&c{relative_filename} is being ignored")
        self.zip_file.close()

        # Remove oldest backup so we don't store too many
        list_of_backups = os.listdir(self.backup_path)  
        full_paths = [f"{os.path.join(self.backup_path, x)}" for x in list_of_backups]
        if len(list_of_backups) > self.max_local_backups:
            oldest_file = min(full_paths, key=os.path.getctime)
            os.remove(oldest_file)
            cprint(f"&cRemoved {oldest_file} as it was the oldest backup")

        # if there is a discord webhook, then send a notification.
        if len(self.discord_webook) > 0:
            fileSizeMB = round(os.path.getsize(self.backup_file_name) / 1024 / 1024, 4)
            size, used, free, storagePercent = getStorageAmount()
            totalRam, usedRam, percentUsed = getRamUsage()
            values = {
                "Backup Size (MB)": [str(fileSizeMB), True],
                "Backup Size (GB)": [str(round(fileSizeMB / 1024, 4)), True],
                "Filename": [self.zipfilename, False],              
                "Storage": [f"Total: {size} - Free: {free} - Used: {used} ({storagePercent})", False],
                "RAM": [f"Total: {totalRam} - UsedRam: {usedRam} ({round(float(percentUsed), 2)}%)", False],
            }

            time_passed = datetime.now() - datetime.strptime(self.current_time, TIME_FORMAT)
            self.discord_notification(
                url=self.discord_webook, 
                title=f"Minecraft Panel - Backup - {self.server_name}",
                description=f"Backup of {self.server_name} completed successfully in {time_passed} seconds",
                color="11ff44",
                values=values
            )


        if CONFIG['backups']['hetzner-sftp']['enabled']:
            try:
                self.send_file_to_sftp_server()
            except Exception as e:
                print("Error sending backup to Hetzner SFTP server", e)
                return

    # Requires a Hetzner Storage Box (sftp, $3/Month for 1TB)    
    def send_file_to_sftp_server(self):  
        hetzner = CONFIG['backups']['hetzner-sftp']
        REMOTE_BACKUP_DIR = hetzner['remote-dir']

        print("Uploading backup to Hetzner SFTP server...")
        with pysftp.Connection(
            hetzner['server-url'], 
            username=hetzner['username'], 
            password=hetzner['password']
        ) as sftp:
            # .cd, .listdir("path"), .get, .put, .makedirs, .rmdir

            # check that REMOTE_BACKUP_DIR exists, if not make it
            if not sftp.exists(REMOTE_BACKUP_DIR):
                sftp.makedirs(REMOTE_BACKUP_DIR)

            abs_path=os.path.join(REMOTE_BACKUP_DIR, os.path.basename(self.backup_file_name))            
            sftp.put(self.backup_file_name, remotepath=abs_path)
        print("Upload to Hetzner finished!")


    def discord_notification(self, url="", title="", description="", color="ffffff", values={}):
        from discord_webhook import DiscordWebhook, DiscordEmbed
        webhook = DiscordWebhook(url=url)
        # create embed object for webhook

        # get time passed since self.current_time
        

        embed = DiscordEmbed(
            title=title, 
            description=description, 
            color=color
        )   
        # # set thumbnail
        embed.set_thumbnail(
            url='https://media.istockphoto.com/vectors/digital-signage-pixel-icon-tech-element-vector-logo-icon-illustrator-vector-id1164466990?k=20&m=1164466990&s=612x612&w=0&h=K5Zp0dtbjKWQS9CdOO53O09EKphYnxZTqDHppSMZ8Rk='
        )
        
        embed.set_footer(text='Embed Footer Text')
        embed.set_timestamp()
        

        # # add fields to embed
        # embed.add_embed_field(name='File Size', value='Lorem ipsum')

        for k, v in values.items():
            # print(k, v)
            embed.add_embed_field(name=k, value=v[0], inline=v[1])

        webhook.add_embed(embed)

        response = webhook.execute()


class BackupRun:
    def __init__(self):
        b = Backup(debug=True)
        b.zip_files()

# TODO: Make it like this in the MongoDB class?
class BackupGUI:
    def __init__(self):
        options = {
            f"Backup Server": self.backup,
            f"Setup Crontab": self.crontab,
        }

        selected, _ = pick(list(options.keys()), "Select which you would like to do:", indicator=' =>', multiselect=False)
        print(selected)
        options[selected]()

    def backup(self):
        b = Backup(debug=True)
        b.zip_files()
        cinput("&aBackup complete!\n&fEnter to continue...")

    def crontab(self):
        # get current file path
        # current_path = os.path.dirname(os.path.realpath(__file__))
        from console import console_file
        cinput(
        f"""
        &f# Backup every day at midnight
        &a0 0 * * * python3 {console_file} backup
        """
        )