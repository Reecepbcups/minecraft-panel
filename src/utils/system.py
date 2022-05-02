import subprocess
import sys
import os

from utils.cosmetics import cprint

# from utils.config import CONFIG, CONFIG_OBJECT

def checkIfRequirementsAreInstalled() -> bool:
    # check if pip is installed
    pip_check = bool(subprocess.run([sys.executable, "-m", "pip"]))
    if pip_check == False:
        cprint("&c[!] Pip is not installed. Please install it with: &e`sudo python3 -m pip install --upgrade pip`")
        return False

    # check if java is installed
    java_check = bool(subprocess.run(["java", "-version"]))
    if java_check == False:
        cprint("&c[!] Java Runtime is not installed. Please install it with: &e`sudo apt install default-jre`")
        return False

    # Save a file to this dir, add that file to gitignore so each server has to run this first
    # Write file to server directory
    with open("./server_startup_script.py", "w") as f:
        f.write("")

    return True


def getStorageAmount():
    storage = os.popen("""df -h / | grep /""").read().strip().split()
    size = storage[1]
    used = storage[2]
    free = storage[3]
    percentUsed = storage[4]
    print(f"{size=} {used=} {free=} {percentUsed=}")
    return size, used, free

def getRamUsage():
    totalRam = os.popen("""free -h | grep Mem | awk '{print $2}'""").read().strip()
    usedRam = os.popen("""free -h | grep Mem | awk '{print $3}'""").read().strip()

    ramUsed = os.popen("""free -m | grep Mem | awk '{print (($3/$2)*100)}'""").read().strip()
    print(f"System is using {ramUsed}% of TOTAL RAM ({usedRam}/{totalRam})")
    pass

def getNetworkUsage():
    usage = os.popen("""ip -h -s link""").read()
    print(usage)

def getAllJavaPIDs():
    v = os.popen("ps aux | grep java").read()
    print(v)
    pass

def killAll():
    v = os.popen("killall -9 java").read()
    print(v)
    pass