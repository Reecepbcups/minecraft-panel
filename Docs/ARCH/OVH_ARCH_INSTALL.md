

> #### [Direct Download of Anarchy Installer](https://osdn.net/frs/redir.php?m=nchc&f=%2Fstorage%2Fg%2Fa%2Fan%2Fanarchy%2Fanarchy-1.3.4-x86_64.iso)

> #### [Get the sha256 hash from the release page](https://gitlab.com/anarchyinstaller/installer/-/releases)
<br>

This is solely just to wipe the drive, prob a better way to do it

when system fails to boot, open IPMI (over browser).
Top right media selection, load anarchy linux iso. then start media. (it will just show as 1KB)

Reset the server (IPMI menu, top, under "power" button on the left). 
Then press F10 or F11, select cdrom in the boot menu (may be CDROM0). 

Once loads, click "update anarchy" & config the installer. 

```
English, en us,
Skip Updating Mirrors
en_US UTF-8
America
Chicago
Format Drives both as ext4 (not doing manual)
Anarchy Server TLS
name server
set the password
```

(THIS MAY BE REQUIRED IF YOU UPDATE MIROR LIST)
```
It then runs pacman -Sy, but there is a chance this fails.
If it fails, you need to hit okay & the arch CLI loads
run:
pacman -Sy archlinux-keyring.

Then run the cmd: anarchy
follow install steps again.
```

on complete, click the reboot option & nothing else.

After that login to root user via IPM.
Start SSH daemon, network-manager, and dhcpd

## starting services
```bash
systemctl start sshd.service
dhcpcd
systemctl start dhcpcd.service

# networkctl

chsh # change the shell
/usr/bin/bash

pacman -Syyu
ping www.google.com # should not work
```


## get ssh access
```bash
ssh-keygen # no password

# upload your SSH key to an unlisted pastebin
curl https://pastebin.com/raw/4A86LBvk >> ~/.ssh/authorized_keys

# ssh in now & 
source ~/.bashrc && source ~/.bash_profile

# now log out of IPMI
```


## getting host setup
```bash 
hostname NEW_HOSTNAME # if not already

echo "127.0.0.1  localhost
::1        localhost ip6-localhost ip6-loopback
ff02::1    ip6-allnodes
ff02::2    ip6-allrouters
# This host address
127.0.1.1  $HOSTNAME" >> /etc/hosts
```