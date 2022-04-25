from utils.cosmetics import cinput, cprint, cfiglet
from utils.panel_utils import FileInstallException, Panel_Feedback, Panel_Interface
from utils.file_utils import CONFIG, chdir, download
import time
import shutil
import os

PAPER_V2_API_VERSION = "https://papermc.io/api/v2/projects/{project}/versions/{version}"
PAPER_V2_API = "https://papermc.io/api/v2/projects/{project}/versions/{version}/builds/{build}/downloads/{download}"


def paper_install(feedback: Panel_Feedback):
    project = cinput("&3Server Type [waterfall, paper]>> ")
    version = cinput("&3Server Version >> ")
    
    try:
        start = time.time()
        _, json_response = download(PAPER_V2_API_VERSION.format(project=project, version=version)
            ,return_json=True, no_download=True)

        build = str(json_response["builds"][len(json_response["builds"])-1])

        download_url = PAPER_V2_API.format(project=project, version=version, build=build, download=project+"-"+version+"-"+build+".jar")
        cprint(f'&aInstalling {project}:{version}:{build} from {download_url}')
        download(download_url)
        end = time.time()
        cprint(f'&aInstalled {project}:{version}:{build} from {download_url} in {end-start} seconds')
        return download_url.split('/')[-1]
    except FileInstallException as fie:
        feedback.print_stack_trace(fie)


def on_call(headPanel: Panel_Interface):
    cfiglet("&5", "Server Creator")
    cprint("&8Type \"exit\" for Server Name exit")
    server_name = cinput("&3Server Name >> ")
    if server_name.lower() == "exit":
        return
    file_path = f'{CONFIG.get("downloadloc")}/{paper_install(headPanel.feedback)}'
    server_path = f'{CONFIG.get("serverloc")}/{server_name}'

    if not os.path.exists(CONFIG.get("serverloc")):
        os.mkdir(CONFIG.get("serverloc"))
    
    if os.path.exists(server_path):
        cprint("&4This is already a server")
        return
    
    os.mkdir(server_path)
    
    shutil.move(file_path, server_path)

    # Auto EULA Yes
    with open(server_path+"/eula.txt", 'w') as file:
        file.write("eula=true")
    
    # server.properties
    with open(server_path+"/server.properties", "a") as file:
        port = cinput("&3Port >> ")     
        allow_nether = cinput("&3Allow Nether [true/false]>> ")
        max_players = cinput("&3Max Players >> ")
        view_distance = cinput("&3View Distance >> ")
        file.write("server-port="+port+"\n")
        file.write("allow-nether="+allow_nether+"\n")
        file.write("max-players="+max_players+"\n")
        file.write("view-distance="+view_distance+"\n")

    # start script
    with open(server_path+"/start.sh", "a") as file:
        file.write("#!/bin/bash\n")
        simple = bool(cinput("&3Do you want simple setup [true/false] >> "))
        if simple:
            ram = cinput("&3Ram Ammount (MB) >> ")
            file.write(f'java -jar -Xmx{ram}M {os.path.basename(file_path)}')
        else:
            startup_arguments = cinput("Start Args >> ")
            file.write(startup_arguments)
    os.system("chmod +x start.sh")
    
    # spigot.yml
    with open(server_path+"/spigot.yml", "a") as file:
        bungeecord = cinput("&3Bungee [true/false] >> ")
        file.write("bungeecord: "+bungeecord+"\n")