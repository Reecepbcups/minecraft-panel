import subprocess
import re
import os

def get_screen_pid(name: str):
    server = subprocess.Popen(['screen', '-ls'], stdout=subprocess.PIPE)
    stdout, _ = server.communicate()
    matches = re.search(r'(\d+).%s' % name, stdout.decode("utf-8"), re.MULTILINE)
    if matches:
        pids = matches.group()
        pid = pids.split(".")[0]
        os.kill(int(pid), 9)
        subprocess.Popen(['screen', '-wipe'])

def is_screen_running(name: str) -> bool:
    server = subprocess.Popen(['screen', '-ls'], stdout=subprocess.PIPE)
    stdout, _ = server.communicate()
    matches = re.search(r'(\d+).%s' % name, stdout.decode("utf-8"), re.MULTILINE)
    if matches:
        return True
    return False

def get_all_active_screens(printOutput=True) -> list:
    '''
    get a list of all running screens with subprocess
    then print them out & return the list
    '''
    server = subprocess.Popen(['screen', '-ls'], stdout=subprocess.PIPE)
    stdout, _ = server.communicate()
    matches = re.findall(r'(\d+).(.*)', stdout.decode("utf-8"), re.MULTILINE)
    server_list = []
    for match in matches[:-1]:
        # remove anything in parethasis from match[1]
        server = match[1].split("\t")[0]
        server_list.append(server)
    
    if printOutput: print(server_list)
    return server_list
    