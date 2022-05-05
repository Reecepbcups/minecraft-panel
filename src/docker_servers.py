import docker
from utils.killable_thread import thread_with_trace
import os

class DockerConsole():
    '''
    For remote access, configure your Docker daemon to use a tcp socket (such as -H tcp://0.0.0.0:2375) and attach from another machine:
    docker -H $HOST:2375 attach mc
    '''
    def __init__(self, host, port, server):
        self.host = host
        self.port = port
        self.server = server # running --name

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
        os.environ["DOCKER_HOST"] = f"tcp://{self.host}:{self.port}"
        client = docker.from_env()        
        container = client.containers.get(self.server) 

        line = []
        for letter in container.logs(stream=True, follow=True, stdout=True, tail=25, stderr=True):            
            if letter == b'\n':
                print(b''.join(line).decode('utf-8')); line = []
                continue
            elif letter == b'\r':
                continue

            line.append(letter)

    def console_cmd(self, command):
        # or do we disable rcon & mc-send-to-console?
        # https://github.com/itzg/docker-minecraft-server#interacting-with-the-server
        # https://gist.github.com/styblope/dc55e0ad2a9848f2cc3307d4819d819f &/ https://docs.docker.com/engine/security/protect-access/
        # ^ enable tcp to do a docker exec -H tcp://HOST:2375
        output =  os.popen(f"docker -H tcp://{self.host}:{self.port} exec -i {self.server} rcon-cli {command}").read().strip()
        print(output)