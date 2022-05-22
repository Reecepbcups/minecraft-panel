# minecraft-panel

Original - https://github.com/Reecepbcups/bash-minecraft-panel
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
pacman -S ufw python-pip sudo curl git screen zip unzip lsof jq dos2unix jre-openjdk base-devel git nano vi

git clone https://github.com/Reecepbcups/minecraft-panel.git
cd minecraft-panel && python -m pip install -r requirements/requirements.txt

Optional:
pacman -S redis iotop atop dstat glances
```


### Akash Setup
```
# Install the Client (https://docs.akash.network/guides/cli/streamlined-steps/install-the-akash-client)

cd ~/Downloads
AKASH_VERSION="$(curl -s "https://raw.githubusercontent.com/ovrclk/net/master/mainnet/version.txt")"
curl https://raw.githubusercontent.com/ovrclk/akash/master/godownloader.sh | sh -s -- "v$AKASH_VERSION"; sudo mv ./bin/akash /usr/local/bin

# IDK If this is needed or not, may just be a ubuntu Things
# go get golang.org/x/crypto/pbkdf2; go get golang.org/x/crypto/scrypt; go get github.com/youmark/pkcs8

akash keys add hot-wallet --recover
akash tx cert generate client --from hot-wallet --overwrite
akash tx cert publish client --from hot-wallet --gas-prices="0.025uakt" --gas="auto" --gas-adjustment=1.15 --node http://135.181.181.122:28957 --chain-id akashnet-2
# new cert is at ~/.akash/<YOUR-ADDRESS>.pem
```

### Arch MongoDB Setup Guide (Since arch does not have license for mongodb)
```
python -m pip install pymongo dnspython (so we can use srv URI)

You could also run as a docker container, prob easier... install mongo client
pacman -S docker
sudo systemctl start docker
sudo systemctl enable docker
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
sudo apt install ufw python3-pip sudo curl screen zip unzip lsof jq dos2unix software-properties-common screen zip unzip sudo htop nano

# Install java in # Debian Things section

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
# The following was done for akash

apt-get update
apt install software-properties-common screen zip unzip sudo htop nano
sudo apt-get update


wget https://download.java.net/java/GA/jdk17.0.2/dfd4a8d0985749f896bed50d7138ee7f/8/GPL/openjdk-17.0.2_linux-x64_bin.tar.gz
tar xvf openjdk-17.0.2_linux-x64_bin.tar.gz
sudo mv jdk-17.0.2/ /opt/jdk-17/
echo 'export JAVA_HOME=/opt/jdk-17' | sudo tee /etc/profile.d/java17.sh
echo 'export PATH=$JAVA_HOME/bin:$PATH'|sudo tee -a /etc/profile.d/java17.sh
source /etc/profile.d/java17.sh
java -version

sudo update-alternatives --config java
```
