from utils.killable_thread import thread_with_trace

from utils.cosmetics import cprint

from utils.config import CONFIG

from utils.system import os_command, run_os_command

RPC_NODE = "http://135.181.181.122:28957"
WALLET_NAME = "hot-wallet"

class AkashConsole():
    def __init__(self, server):

        akashServers = CONFIG.get('akash-servers')

        if server not in akashServers:
            print("Server not found...")
            return

        self.data = akashServers[server]
        self.dseq = self.data["dseq"]
        self.provider = self.data["provider"]
        self.owner = self.data["owner"]

        self.s = f"akash provider lease-logs --dseq {self.dseq} --follow --tail 10 --provider {self.provider} --from {WALLET_NAME} --node {RPC_NODE}"
        self.c = f"akash provider lease-shell --dseq {self.dseq} --provider {self.provider} --from {WALLET_NAME} --node {RPC_NODE} --tty -- web mc-send-to-console {{COMMAND}}"

    def enter_console(self):
        try:
            console = thread_with_trace(target=self.follow)
            console.start()

            while True:
                user_input = input()
                if user_input == "\x18": # ctrl + c
                    console.kill()
                    break
                elif user_input == "exit": # brings you to main() after console killed
                    console.kill()
                    break
                else:
                    self.console_cmd(user_input)
        except KeyboardInterrupt:
            pass

    def follow(self):
        # Gives a stream of values as needed
        try:
            for line in os_command(self.s, print_output=False):
                line = line.split("] [", 1) # removes akash prefix
                if len(line) > 1:
                    line = line[1]
                    print("[" + str(line[1::]))
        except OSError as e:
            cprint("&cConsole Closing... " + e)
        except KeyboardInterrupt as e:
            cprint("&cConsole Closing... " + e)

    def console_cmd(self, command):
        run_os_command(self.c.replace("{COMMAND}", command), print_output=True)