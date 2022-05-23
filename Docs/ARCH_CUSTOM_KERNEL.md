### Arch Custom Kernel
```
sudo pacman -S linux-zen linux-zen-headers

sudo nano /etc/default/grub

# Change:
GRUB_DEFAULT=saved # change from =0
GRUB_SAVEDEFAULT=true # uncomment
GRUB_DISABLE_SUBMENU=y # uncomment

sudo grub-mkconfig -o /boot/grub/grub.cfg
reboot

uname -r
```