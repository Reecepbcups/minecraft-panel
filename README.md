# minecraft-panel

Original - https://github.com/Reecepbcups/bash-minecraft-panel

Update to Python - https://github.com/Y2Kwastaken/mcpython-panel

Continued production for CraftEconomy's needs - here


### Look into if they should be added
```
build-essential nginx htop glances nodejs cpufrequtils figlet redis default-jre sysstat slurm speedometer software-properties-common

cpufreq-set -r -g performance	
timedatectl set-timezone America/Chicago
```

# Setup
### Arch
```
pacman -S ufw python-pip sudo curl screen zip unzip lsof dos2unix jre-openjdk

python -m pip install -r requirements.txt

Optional:
pacman -S redis iotop
```

### Ubuntu / Debian
```
sudo apt install ufw python3-pip sudo curl screen zip unzip lsof dos2unix <someJREHere>

python3 -m pip install -r requirements.txt

# Optional:
curl -sL https://deb.nodesource.com/setup_12.x | bash -
```

### Debian Things
#### Need to go through this and see what is required
```
# Java 11 - doesnt work for my 1.8 MC
echo 'deb http://ftp.debian.org/debian stretch-backports main' | sudo tee /etc/apt/sources.list.d/stretch-backports.list
sudo apt update && apt-get upgrade
sudo apt install openjdk-11-jdk
sudo apt-get install openjdk-11-jre

# Java 8 / Java8
wget -qO - https://adoptopenjdk.jfrog.io/adoptopenjdk/api/gpg/key/public | sudo apt-key add -
sudo add-apt-repository --yes https://adoptopenjdk.jfrog.io/adoptopenjdk/deb/
sudo apt-get update && sudo apt-get install adoptopenjdk-8-hotspot

# https://stackoverflow.com/questions/57031649/how-to-install-openjdk-8-jdk-on-debian-10-buster
sudo apt-add-repository 'deb http://security.debian.org/debian-security stretch/updates main'
sudo apt-get update
sudo apt-get install openjdk-8-jdk

sudo update-alternatives --config java
```