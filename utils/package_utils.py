
import subprocess, platform

def _installPipIfNot():
    o = subprocess.check_output(['pip', '--version'])
    print(o)

    if platform.system() == "Linux":
        distr = platform.release() # 5.17.4-arch1-1
        if "debian" in distr.lower():
            print("Installing pip with apt-get")
            subprocess.call("apt install python3-pip".split(" "))
        elif "arch" in distr.lower():
            print("Installing pip with pacman")
            subprocess.call("pacman -S python-pip".split(" "))
        else:
            print("You need to install pip manually")
            exit()
    else: 
        print("You need to install pip manually for this opperating system")
        exit()

def installPackage(package_name):
    _installPipIfNot()
    import pip
    pip.main(['install', package_name])


    # print("\n[!] Run the command 'python -m pip install -r requirements.txt' to install dependencies")
    # exit()