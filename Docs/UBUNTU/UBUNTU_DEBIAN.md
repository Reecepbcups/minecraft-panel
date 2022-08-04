
### Setup
```
apt-get update
sudo apt install ufw python3-pip sudo curl screen zip unzip lsof jq dos2unix software-properties-common screen zip unzip sudo htop nano redis redis-tools
sudo apt-get upgrade

git clone https://github.com/Reecepbcups/minecraft-panel.git
cd minecraft-panel && python3 -m pip install -r requirements/requirements.txt

# Optional:
curl -sL https://deb.nodesource.com/setup_12.x | bash -

# Install java
wget https://download.java.net/java/GA/jdk17.0.2/dfd4a8d0985749f896bed50d7138ee7f/8/GPL/openjdk-17.0.2_linux-x64_bin.tar.gz
tar xvf openjdk-17.0.2_linux-x64_bin.tar.gz
sudo mv jdk-17.0.2/ /opt/jdk-17/
echo 'export JAVA_HOME=/opt/jdk-17' | sudo tee /etc/profile.d/java17.sh
echo 'export PATH=$JAVA_HOME/bin:$PATH'|sudo tee -a /etc/profile.d/java17.sh
source /etc/profile.d/java17.sh
java -version

sudo update-alternatives --config java
```


## OVERCLOCKING
```
sudo apt install cpufrequtils
cpufreq-set -r -g performance	
```