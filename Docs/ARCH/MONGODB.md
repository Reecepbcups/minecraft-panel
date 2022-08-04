# Install MongoDB Tools & Shell on Arch

> ### UPDATED GUIDE - WIP
```bash
This is 4.4.6, we need >5.0.0


# https://awan.com.np/how-to-install-mongodb-on-arch-linux-working/
useradd -m software -p myAccountsPassword --shell /bin/false

passwd software

su software -s /bin/bash
git clone https://aur.archlinux.org/yay-git.git
cd yay-git

makepkg -si

yay -S mongodb-bin

exit # su root

systemctl enable --now mongodb
systemctl start --now mongodb

mongo


sudo nano /etc/mongodb.conf
# update:
 - bindIp: 127.0.0.1,0.0.0.0

# update
security:
  authorization: "enabled"
```




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





## Install via AUR
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
sudo chown -R 966:966 /data/db # (where 966 is the group)

systemctl start mongodb.service
systemctl status mongodb # should return active

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
