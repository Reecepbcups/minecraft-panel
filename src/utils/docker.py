"""
# This would require me to write DockerConsole, not sure this is worth it since using akash
def DockerSelector():
    '''
    cd paper-docker-build
    docker build . -t test-server
    docker rm mc2
    docker run -d -it -p 25565:25565 --name mc2 -e OPS=reecepbcups -e MOTD="My Docker Server" -e EULA=TRUE -e VERSION=1.18.2 test-server:latest
    # Ensure the port for rcon is enabled too
    '''
    cfiglet("&a", "C-Docker", clearScreen=True)

    # I guess we add host here & run docker ps to see running stuff?
    # This possible with akash or?
    dockers = {"mc2": ["65.21.197.51", 2375]}

    for d in dockers:
        print(f"[{d}] {dockers[d][0]}:{dockers[d][1]}")
    print()

    server = cinput("\nDocker Selector > ")
    if server not in dockers:
        cprint("&cInvalid Selection")

    host = dockers[server][0]
    port = dockers[server][1]
    panel = DockerConsole(host, port, server)
    panel.enter_console()
"""