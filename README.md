# Minecraft-Panel
Original Bash Version - https://github.com/Reecepbcups/bash-minecraft-panel

<br/>

# Setup
## Arch
```
pacman -S ufw python-pip sudo curl git screen zip \
unzip lsof jq dos2unix jre-openjdk base-devel git nano vi \
iotop atop dstat glances maven cpio pahole htop btop go-pie redis

# optional: nginx glances nodejs figlet sysstat slurm speedometer

git clone https://github.com/Reecepbcups/minecraft-panel.git
cd minecraft-panel
python -m pip install -r requirements/requirements.txt
# Then update minecraft-panel/config.yml to your values
# Update src/utils/config.py PATH_TO_CONFIG_FILE for custom config location

# First run it will prompt you to source the bashrc file for the console alias
python minecraft-panel/src/console.py

hostnamectl hostname myMachineName

git config --global user.name "Reece"
git config --global user.email "Reece@gmail.com"
git config credential.helper store

# You can view all params to change with `sysctl -a`
echo "65535" > /proc/sys/fs/file-max
echo "fs.file-max = 65535" >> /etc/sysctl.conf
echo "root hard nofile 150000" >> /etc/security/limits.conf
echo "root soft nofile 150000" >> /etc/security/limits.conf
echo "* hard nofile  150000" >> /etc/security/limits.conf
echo "* soft nofile 150000" >> /etc/security/limits.conf

timedatectl set-timezone America/Chicago
```

# Other Documentation

> ## [Akash Client Install](Docs/AKASH_CLIENT_INSTALL.md)

> ## [Stress Testing Minecraft](Docs/STRESS_TEST_MC.md)

> ## [Arch Custom Kernel](Docs/ARCH_CUSTOM_KERNEL.md)

> ## [Ubuntu Overclock](Docs/OVERCLOCKING.md)
