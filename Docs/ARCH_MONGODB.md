## Install via docker
```
pacman -S docker
sudo systemctl start docker
sudo systemctl enable docker
docker run -d -p 27017:27017 -v data:/data/db mongo
```

## Install via AUR
```
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