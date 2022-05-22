# minecraft-panel

Original Bash Version - https://github.com/Reecepbcups/bash-minecraft-panel

# Setup
### Arch
```
pacman -S ufw python-pip sudo curl git screen zip \
unzip lsof jq dos2unix jre-openjdk base-devel git nano vi \
iotop atop dstat glances

# optional: redis

git clone https://github.com/Reecepbcups/minecraft-panel.git
cd minecraft-panel && python -m pip install -r requirements/requirements.txt

hostnamectl hostname MACHINENAME

git config --global user.name "NAME"
git config --global user.email "NAME@tld.com"
git config credential.helper store

# You can view all params to change with `sysctl -a`
echo "65535" > /proc/sys/fs/file-max
echo "fs.file-max = 65535" >> /etc/sysctl.conf
echo "root hard nofile 150000" >> /etc/security/limits.conf
echo "root soft nofile 150000" >> /etc/security/limits.conf
echo "* hard nofile  150000" >> /etc/security/limits.conf
echo "* soft nofile 150000" >> /etc/security/limits.conf
```

### Akash Client
```
# Install the Client (https://docs.akash.network/guides/cli/streamlined-steps/install-the-akash-client)

cd ~
AKASH_VERSION="$(curl -s "https://raw.githubusercontent.com/ovrclk/net/master/mainnet/version.txt")"
curl https://raw.githubusercontent.com/ovrclk/akash/master/godownloader.sh | sh -s -- "v$AKASH_VERSION"; sudo mv ./bin/akash /usr/local/bin

# IDK If this is needed or not, may just be a ubuntu Things
# go get golang.org/x/crypto/pbkdf2; go get golang.org/x/crypto/scrypt; go get github.com/youmark/pkcs8

akash keys add hot-wallet --recover
akash tx cert generate client --from hot-wallet --overwrite
akash tx cert publish client --from hot-wallet --gas-prices="0.025uakt" --gas="auto" --gas-adjustment=1.15 --node http://135.181.181.122:28957 --chain-id akashnet-2
# new cert is at ~/.akash/<YOUR-ADDRESS>.pem
```


### Look into if they should be added
```
build-essential nginx htop glances nodejs cpufrequtils figlet redis default-jre sysstat slurm speedometer software-properties-common

cpufreq-set -r -g performance	
timedatectl set-timezone America/Chicago
```