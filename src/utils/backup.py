from dataclasses import fields
from utils.file import CONFIG
from utils.cosmetics import cfiglet, cinput, cprint
from pick import pick

from utils.system import getStorageAmount, getRamUsage, getCurrentHostname

from utils.notifications import discord_notification

from pymongo import MongoClient

from datetime import datetime
import zipfile
import pysftp
import shutil
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

        self.discord_webhook = CONFIG['backups']['discord-webhook']
        self.debug = debug
        self.save_relative = CONFIG['backups']['save-relative']
                
        self.zipfilename = f"{getCurrentHostname()}_{self.current_time}.zip"
        self.backup_file_name = os.path.join(self.backup_path, self.zipfilename)
        

    def backup_mongodb(self, mongoDBConfig):
        client = MongoClient(mongoDBConfig['backup-uri'])        
        # confirm client is connected
        if client is None:
            cprint("&cMongoDB client is not connected")
            exit(0)

        self.mongodb_abs_location = os.path.join(self.backup_path, f'mongodb_dump_{self.current_time}')
        res = os.system(f"mongodump --uri={mongoDBConfig['backup-uri']} --out {self.mongodb_abs_location}")
        if res != 0:
            cprint("&cMongoDB backup failed!")
            exit(0)

        # print(self.mongodb_abs_location)
        # exit(0)

        # Adds mongodb absolute location to the zip file to be looped through
        self.root_paths[self.mongodb_abs_location] = []
        # exit(0)


    def _delete_oldest_file_in_dir(self):
        # Remove oldest backup so we don't store too many
        list_of_backups = os.listdir(self.backup_path) 
        print(list_of_backups) 
        full_paths = [f"{os.path.join(self.backup_path, x)}" for x in list_of_backups]
        if len(list_of_backups) > self.max_local_backups:
            oldest_file = min(full_paths, key=os.path.getctime)
            os.remove(oldest_file)
            # cprint(f"&cRemoved {oldest_file} as it was the oldest backup")

    def zip_files(self):
        self.zip_file = zipfile.ZipFile(self.backup_file_name, "w", compression=zipfile.ZIP_DEFLATED)

        # use pymongo to save the backup to the database
        # https://stackoverflow.com/questions/24610484/pymongo-mongoengine-equivalent-of-mongodump ??
        mongoConfig = CONFIG['backups']['database']['mongodb']        
        if(mongoConfig['enabled']):
            self.backup_mongodb(mongoConfig)

        for root_path in self.root_paths:            
            if not os.path.isdir(root_path):
                cprint(f"\n&c{root_path} is not a directory, ignoring...")
                continue

            ignore_regex = CONFIG['backups']['parent-paths'][root_path]
            # print(root_path, ignore_regex)            

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
        
        # delete folder self.mongodb_abs_location
        if(mongoConfig['enabled']):
            if len(self.mongodb_abs_location) > 3:
                shutil.rmtree(self.mongodb_abs_location)
            else:
                print(f"Safety check hit, can't delete {self.mongodb_abs_location}")

        self._delete_oldest_file_in_dir()

        # if there is a discord webhook, then send a notification.
        if len(self.discord_webhook) > 0:
            fileSizeMB = round(os.path.getsize(self.backup_file_name) / 1024 / 1024, 4)
            size, used, free, storagePercent = getStorageAmount()
            totalRam, usedRam, percentUsed = getRamUsage()
            values = {
                "Backup Size (MB)": [str(fileSizeMB), True],
                "Backup Size (GB)": [str(round(fileSizeMB / 1024, 4)), True],                
                "Backup To Hetzner": [str(CONFIG['backups']['hetzner-sftp']['enabled']), True],
                "Storage": [f"Total: {size} - Free: {free} - Used: {used} ({storagePercent})", False],
                "RAM": [f"Total: {totalRam} - UsedRam: {usedRam} ({round(float(percentUsed), 2)}%)", False],
            }

            time_passed = (datetime.now() - datetime.strptime(self.current_time, TIME_FORMAT)).seconds

            discord_notification(
                url=self.discord_webhook, 
                title=f"Panel - Backup - {getCurrentHostname()}",
                description=f"Backup of {self.zipfilename} | ({time_passed}s)",
                color="11ff44",
                values=values,
                imageLink="https://media.istockphoto.com/vectors/digital-signage-pixel-icon-tech-element-vector-logo-icon-illustrator-vector-id1164466990?k=20&m=1164466990&s=612x612&w=0&h=K5Zp0dtbjKWQS9CdOO53O09EKphYnxZTqDHppSMZ8Rk=",
                footerText=""
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

        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        print("Uploading backup to Hetzner SFTP server...")
        with pysftp.Connection(
            hetzner['server-url'], 
            username=hetzner['username'], 
            password=hetzner['password'],
            cnopts=cnopts
        ) as sftp:
            # .cd, .listdir("path"), .get, .put, .makedirs, .rmdir

            # check that REMOTE_BACKUP_DIR exists, if not make it
            if not sftp.exists(REMOTE_BACKUP_DIR):
                sftp.makedirs(REMOTE_BACKUP_DIR)

            abs_path=os.path.join(REMOTE_BACKUP_DIR, os.path.basename(self.backup_file_name))            
            sftp.put(self.backup_file_name, remotepath=abs_path)
        print("Upload to Hetzner finished!")


       


class BackupRun:
    def __init__(self, debugBool="False"):
        debugging = False  
        if debugBool[0].lower().startswith("t"):
            debugging = True
        
        print(f"BackupRun {debugging=}")
        b = Backup(debug=debugging)
        b.zip_files()


# TODO: Make it like this in the MongoDB class?
class BackupGUI:
    def __init__(self):
        options = {
            f"Backup Server": self.backup,
            f"Setup Crontab": self.crontab,
        }

        selected, _ = pick(list(options.keys()), "Select which you would like to do:", indicator=' =>', multiselect=False)        
        options[selected]()

    def backup(self):
        BackupRun()
        cinput("&aBackup complete!\n&cEnter to continue...")

    def crontab(self):
        # get current file path
        # current_path = os.path.dirname(os.path.realpath(__file__))
        from console import console_file
        cinput(f"""\n&aEDITOR=nano crontab -e\n&f# Backup every day at midnight\n&a0 0 * * * python3 {console_file} backup false""")