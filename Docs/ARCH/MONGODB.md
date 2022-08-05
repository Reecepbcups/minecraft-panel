# Install MongoDB Tools & Shell on Arch

> ### UPDATED GUIDE - WIP
```bash
# https://awan.com.np/how-to-install-mongodb-on-arch-linux-working/
useradd -m software -p myAccountsPassword --shell /bin/false

passwd software

su software -s /bin/bash
cd /home/software
git clone https://aur.archlinux.org/yay-git.git
cd yay-git

makepkg -si

yay -S mongodb-bin mongodb-tools-bin mongosh-bin

exit # su root
systemctl enable --now mongodb
systemctl start --now mongodb

mongosh


# create new users
use crafteconomy
db.createUser({ user: "craftdbuser", pwd: passwordPrompt(), roles: [ "readWrite" ] })

use admin
db.createUser( { user: "admin", pwd: passwordPrompt(), roles: [ "readWrite", "dbAdmin" ] })


sudo nano /etc/mongodb.conf
# update:

 - bindIp: 127.0.0.1,MACHINE_IP_HERE
# update
security:
  authorization: "enabled"
# ctrl + x, y, enter

systemctl restart mongodb


sudo cp /usr/bin/mongosh /usr/bin/mongo
```



## DEPRECATED - manual way, use yay instead
```bash

useradd -m software -p myAccountsPassword --shell /bin/false
su software -s /bin/bash
cd ~

git clone  https://aur.archlinux.org/mongodb-shell-bin.git 
git clone https://aur.archlinux.org/mongodb-tools.git

exit # need to be root here
chmod +x -R /home/software/mongodb-tools
chmod +x -R /home/software/mongodb-shell-bin

su software -s /bin/bash

cd ~
cd mongodb-tools
makepkg -s -f
cd ../mongodb-tools
makepkg -s -f

exit # need to be root again
cp /home/software/mongodb-shell-bin/pkg/mongodb-shell-bin/usr/bin/mongo /usr/bin/
cp /home/software/mongodb-tools/pkg/mongodb-tools/usr/bin/* /usr/bin/
```





## DEPRECATED - Install via AUR
```bash
# https://www.maketecheasier.com/use-aur-in-arch-linux/
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
makepkg -s

exit # gets you back to root user
cd /home/software/mongodb-bin/ && sudo pacman -U --noconfirm mongodb-bin-*.tar.zst\\

sudo mkdir -p /data/db
sudo nano /etc/mongodb.conf #(update path to /data/db)
grep mongo /etc/passwd # (get the mongodb user id & group)
sudo chown -R 970:970 /data/db # (where 966 is the group)

sudo chown -R mongodb:mongodb /var/lib/mongodb # or /data/db
sudo chown mongodb:mongodb /tmp/mongodb-27017.sock


systemctl start mongodb.service && systemctl status mongodb # should return active

# if so:
systemctl enable mongodb.service
mongo
```

## Install MongoDB Server via docker
### best option to run is with Akash persistant storage
[Akash SDL](../akash/mongodb-deploy.yml)
```bash
pacman -S docker
sudo systemctl start docker
sudo systemctl enable docker
docker run -d -p 27017:27017 -v data:/data/db mongo
```
