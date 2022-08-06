import os
import shlex
import subprocess
import sys

import requests

from utils.cosmetics import cprint


def getPublicIPAddress():
    r = requests.get('https://api.ipify.org')
    return r.text

def checkIfRequirementsAreInstalled() -> bool:
    # check if pip is installed
    pip_check = bool(subprocess.run([sys.executable, "-m", "pip"], stdout=subprocess.DEVNULL))
    if pip_check == False:
        cprint("&c[!] Pip is not installed. Please install it with: &e`sudo python3 -m pip install --upgrade pip`")
        return False

    # check if java is installed
    # java_check = bool(subprocess.run(["java", "-version"], stdout=subprocess.PIPE))
    # if java_check == False:
    #     cprint("&c[!] Java Runtime is not installed. Please install it with: &e`sudo apt install default-jre`")
    #     return False

    return True

import datetime


def get_time() -> str:
    now = datetime.datetime.now()
    return f"{now.hour}-{now.minute}-{now.second}"

def getStorageAmount():
    storage = os.popen("""df -h / | grep /""").read().strip().split()
    size = storage[1]
    used = storage[2]
    free = storage[3]
    percentUsed = storage[4]
    print(f"{size=} {used=} {free=} {percentUsed=}")
    return size, used, free, percentUsed

def getRamUsage():
    totalRam = os.popen("""free -h | grep Mem | awk '{print $2}'""").read().strip()
    usedRam = os.popen("""free -h | grep Mem | awk '{print $3}'""").read().strip()

    percentUsed = os.popen("""free -m | grep Mem | awk '{print (($3/$2)*100)}'""").read().strip()
    print(f"System is using {percentUsed}% of TOTAL RAM ({usedRam}/{totalRam})")
    return totalRam, usedRam, percentUsed

def getCurrentHostname():
    return os.popen("hostname").read().strip()

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



# === os commands

def os_command(command, print_output=True, shell=False):
    """
    Run an OS command (utility function) and returns a generator
    with each line of the stdout.

    In case of error, the sterr is forwarded through the exception.

    For the arguments, see run_os_command.
    If you are not sur between os_command and run_os_command,
    then the second is likely for you.
    """
    ENCODING = 'UTF-8'
    if isinstance(command, str):
        # if a string, split into a list:
        command = shlex.split(command)
    # we need a proper context manager for Python 2:
    if sys.version_info < (3,2):
        Popen = Popen2
    else:
        Popen = subprocess.Popen
    # Process:
    with Popen(command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    shell=shell) as process:
        while True:
            line = process.stdout.readline().rstrip()
            if not line:
                # check error:
                process.poll()
                errno = process.returncode
                if errno:
                    # get the error message:
                    stderr_msg = str(process.stderr.read(), ENCODING)
                    errmsg = "Call of '%s' failed with error %s\n%s" % \
                                            (command, errno, stderr_msg)
                    raise OSError(errno, errmsg)
                break
            # Python 3: converto to unicode:
            if sys.version_info > (3,0):
                line = str(line, ENCODING)
            if print_output:
                print(line)
            yield line

def run_os_command(command, print_output=True, shell=False):
    """
    Execute a command, printing as you go (unless you want to suppress it)

    Arguments:
    ----------
        command: eithr a string, a list containing each element of the command
            e.g. ['ls', '-l']
        print_output: print the results as the command executes
            (default: True)
        shell: call the shell; this activates globbing, etc.
            (default: False, as this is safer)

    Returns:
    --------
        A string containing the stdout
    """
    r = list(os_command(command, print_output=print_output, shell=shell))
    return "\n".join(r)


def os_get(command, shell=False):
    """
    Execute a command as a function

    Arguments:
    ----------
        command: a list containing each element of the command
            e.g. ['ls', '-l']
        shell: call the shell; this activates globbing, etc.
            (default: False)

    Returns:
    --------
        A string containing the output
    """
    return run_os_command(command, print_output=False, shell=shell)
