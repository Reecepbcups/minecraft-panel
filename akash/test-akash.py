# python3 -m pip install mcrcon
from mcrcon import MCRcon

'''
# Install the Client
cd ~/Downloads; AKASH_VERSION="$(curl -s "https://raw.githubusercontent.com/ovrclk/net/master/mainnet/version.txt")"; curl https://raw.githubusercontent.com/ovrclk/akash/master/godownloader.sh | sh -s -- "v$AKASH_VERSION"; sudo mv ./bin/akash /usr/local/bin

# not sure this is needed
go get golang.org/x/crypto/pbkdf2; go get golang.org/x/crypto/scrypt; go get github.com/youmark/pkcs8

akash keys add hot-wallet --recover
akash tx cert generate client --from hot-wallet --overwrite
akash tx cert publish client --from hot-wallet --gas-prices="0.025uakt" --gas="auto" --gas-adjustment=1.15 --node http://135.181.181.122:28957 --chain-id akashnet-2

# new cert is at ~/.akash/<YOUR-ADDRESS>.pem
'''

'''
akash q deployment list --log_format json --state active --node http://135.181.181.122:28957

akash q deployment get --dseq 5751573 --owner akash1rpv97xasy7px29ccdhy93ar6aj0t8a6895d4n3 --node http://135.181.181.122:28957

# idk what this is
akash q deployment group get --dseq 5751573 --owner akash1rpv97xasy7px29ccdhy93ar6aj0t8a6895d4n3 --node http://135.181.181.122:28957



akash provider lease-logs --dseq 5751573 --follow --tail 10 --provider akash1r7y2msa9drwjss5umza854he5vwr2czunye9de --from hot-wallet --node http://135.181.181.122:28957
akash provider lease-shell --dseq 5751573 --provider akash1r7y2msa9drwjss5umza854he5vwr2czunye9de --node http://135.181.181.122:28957 --from hot-wallet --tty --stdin -- web /bin/sh

akash provider lease-shell --dseq 5751573 --provider akash1r7y2msa9drwjss5umza854he5vwr2czunye9de --node http://135.181.181.122:28957  --from hot-wallet --tty -- web ls > testls.txt

akash provider lease-shell --dseq 5751573 --provider akash1r7y2msa9drwjss5umza854he5vwr2czunye9de --node http://135.181.181.122:28957  --from hot-wallet --tty -- web rcon-cli
"akash provider lease-shell --dseq {dseq} --provider {provider} --from {WALLET_NAME} --node {RPC_NODE} --tty -- web mc-send-to-console {{COMMAND}}"
'''

RPC_NODE = "http://135.181.181.122:28957"
WALLET_NAME = "hot-wallet"

akashServers = {
    # owner always the same from the hot-wallet right? or could these be different?
    "mc-1": {
        "dseq": 5753036, # Akashalytics raw_data panel
        "owner": "akash1rpv97xasy7px29ccdhy93ar6aj0t8a6895d4n3",
        "provider": "akash1vky0uh4wayh9npd74uqesglpaxwymynnspf6a4",
        
    },
    "mc-2": {
        "dseq": 5753210, # Akashalytics raw_data panel
        "owner": "akash1rpv97xasy7px29ccdhy93ar6aj0t8a6895d4n3",
        "provider": "akash1r7y2msa9drwjss5umza854he5vwr2czunye9de",        
    }
}

print(akashServers.keys())
server = "mc-1" # server = input("Enter server name: ")
print("Connecting to server:", server)

data = akashServers[server]
dseq = data["dseq"]
provider = data["provider"]
owner = data["owner"]

s = f"akash provider lease-logs --dseq {dseq} --follow --tail 10 --provider {provider} --from {WALLET_NAME} --node {RPC_NODE}"
c = f"akash provider lease-shell --dseq {dseq} --provider {provider} --from {WALLET_NAME} --node {RPC_NODE} --tty -- web mc-send-to-console {{COMMAND}}"
print(s)
# os.system(s)



import sys, subprocess, shlex

class Popen2(subprocess.Popen):
    "Context manager for Python2"
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        if self.stdout:
            self.stdout.close()
        if self.stderr:
            self.stderr.close()
        if self.stdin:
            self.stdin.close()
        # Wait for the process to terminate, to avoid zombies.
        self.wait()


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


# ===========================================


import sys
import threading
class thread_with_trace(threading.Thread):
  def __init__(self, *args, **keywords):
    threading.Thread.__init__(self, *args, **keywords)
    self.killed = False
 
  def start(self):
    self.__run_backup = self.run
    self.run = self.__run     
    threading.Thread.start(self)
 
  def __run(self):
    sys.settrace(self.globaltrace)
    self.__run_backup()
    self.run = self.__run_backup
 
  def globaltrace(self, frame, event, arg):
    if event == 'call':
      return self.localtrace
    else:
      return None
 
  def localtrace(self, frame, event, arg):
    if self.killed:
      if event == 'line':
        raise SystemExit()
    return self.localtrace
 
  def kill(self):
    self.killed = True



class DockerConsole():
    def __init__(self, server):
        self.server = server 

    def enter_console(self): # so we can use parent enter_console function ? then just our custom follow for docker
        try:
            console = thread_with_trace(target=self.follow)
            console.start()

            while True:
                user_input = input()
                if user_input == "\x18": # ctrl + c
                    break
                elif user_input == "exit": # brings you to main() after console killed
                    break
                else:
                    self.console_cmd(user_input)
        except KeyboardInterrupt:
            pass

    def follow(self):
        # Gives a stream of values as needed
        for line in os_command(s, print_output=False):
            line = line.split("] [", 1) # removes akash prefix
            if len(line) > 1:
                line = line[1]
                print("[" + str(line[1::]))

    def console_cmd(self, command):
        run_os_command(c.replace("{COMMAND}", command), print_output=True)


d = DockerConsole("mc-1")
d.enter_console()
