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
pacman -S ufw python-pip sudo curl screen zip unzip lsof jq dos2unix jre-openjdk

python -m pip install -r requirements.txt

Optional:
pacman -S redis iotop atop docker dstat glances
```

### Arch MongoDB Setup Guide (Since arch does not have license for mongodb)
```
python -m pip install pymongo dnspython (so we can use srv URI)
sudo pacman -S --needed base-devel git nano vi

You could also run as a docker container, prob easier... install mongo client
sudo systemctl start docker
docker run -d -p 27017:27017 -v data:/data/db mongo

https://www.maketecheasier.com/use-aur-in-arch-linux/
useradd -m software -p myPassword19191 --shell /bin/false
usermod -aG wheel software # this is adding sudo to user
nano /etc/sudoers # (really you should use visudo, but you'll be okay)
uncomment the following lines: 
# %wheel ALL=(ALL:ALL) ALL
# %wheel ALL=(ALL:ALL) NOPASSWD: ALL
ctrl+x, y, enter

su software -s /bin/bash
cd ~
git clone https://aur.archlinux.org/mongodb-bin.git
cd mongodb-bin
makepkg -si

exit # gets you back to root user
cd /home/software/mongodb-bin/ && sudo pacman -U --noconfirm mongodb-bin-*.tar.zst
systemctl start mongodb.service
systemctl status mongodb # should return active
if so:
systemctl enable mongodb.service
mongo
```


### Ubuntu / Debian
```
sudo apt install ufw python3-pip sudo curl screen zip unzip lsof jq dos2unix <someJREHere>

python3 -m pip install -r requirements.txt

# Optional:
curl -sL https://deb.nodesource.com/setup_12.x | bash -
```


### Tuning the Machine
```
# You can view all params to change with `sysctl -a`
echo "65535" > /proc/sys/fs/file-max
echo "fs.file-max = 65535" >> /etc/sysctl.conf
echo "root hard nofile 150000" >> /etc/security/limits.conf
echo "root soft nofile 150000" >> /etc/security/limits.conf
echo "* hard nofile  150000" >> /etc/security/limits.conf
echo "* soft nofile 150000" >> /etc/security/limits.conf
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