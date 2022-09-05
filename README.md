# Minecraft-Panel
Original Bash Version - https://github.com/Reecepbcups/bash-minecraft-panel

<br/>

# Setup Machine
### Initial Setup
- [Hetzner Recommended Arch](https://www.hetzner.com/dedicated-rootserver/matrix-ax)
- **[Arch From Scratch Install Guide (OVH)](Docs/ARCH/OVH_ARCH_INSTALL.md)
### Post Installation & Connections
```bash
pacman -S ufw python-pip sudo curl git screen zip cron \
unzip lsof jq dos2unix jre-openjdk base-devel git nano vi \
iotop atop dstat glances maven cpio pahole htop btop go-pie redis

# Start cronjob
systemctl enable cronie
systemctl start cronie

# Install Redis
systemctl start redis
nano /etc/redis/redis.conf
>> # find requirepass  & set as you want
>> # comment out "bind 127.0.0.1 -::1" line
systemctl restart redis

# If you need to listen to key events:
# nano /etc/redis/redis.conf
# notify-keyspace-events "KEA"

# optional: nginx glances nodejs figlet sysstat slurm speedometer

git clone https://github.com/Reecepbcups/minecraft-panel.git
cd minecraft-panel
python -m pip install -r requirements/requirements.txt
# Then update minecraft-panel/config.yml to your values
# Update src/utils/config.py PATH_TO_CONFIG_FILE for custom config location

# First run it will prompt you to source the bashrc file for the console alias
python src/console.py

# git config --global user.name "Reece"
# git config --global user.email "Reece@gmail.com"
# git config credential.helper store

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

Arch:
> ### [Performance Kernel](Docs/ARCH/PERFORMANCE_KERNEL.md)
> ### [MongoDB Install](Docs/ARCH/MONGODB.md)

Akash:
> ### [Akash Client Install](Docs/AKASH/AKASH_CLIENT_INSTALL.md)
> ### [Akash Misc Commands](Docs/AKASH/AKASH_COMMANDS.md)


Other:
> ### [Stress Testing Minecraft](Docs/STRESS_TEST_MC.md)
