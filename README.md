Simple project to controll Rover Robot. Web with cam and API.

# Installation instructions
## Prepare SD card

### Fetch raspbian
`curl https://downloads.raspberrypi.org/raspios_lite_armhf/images/raspios_lite_armhf-2020-12-04/2020-12-02-raspios-buster-armhf-lite.zip --output 2020-12-02-raspios-buster-armhf-lite.zip`
### Unzip raspbian image
`unzip 2020-12-02-raspios-buster-armhf-lite.zip`
### Burn (yeah old style) to SD card
`dd if=2020-12-02-raspios-buster-armhf-lite.img of=/dev/sdb`

## Reconnect SD card so it will be mounted (in my case in /media/dawszy/{root,boot}fs

### Lets fetch some needed files to: /tmp/rover/

`mkdir -p /tmp/rover`

## Fetch data from git

`cd /tmp/rover`

`git clone https://github.com/sq6emm/4x4-rover.git`

`cd /tmp/rover/4x4rover/`

## Now we will modify some files...


### Enable pi camera, disable bluetooth and camera led, set defaults for used gpio pins

`cat raspbian/boot/config.txt.addon >> /media/dawszy/bootfs/config.txt`

### Enable wifi (remember to modify this file by adding your WIFI networks)

`cp raspbian/boot/wpa_supplicant.conf /media/dawszy/bootfs/`

### Enable ssh after reboot

`cp raspbian/boot/ssh /media/dawszy/bootfs/`

### Modify /media/dawszy/rootfs/etc/rc.local to disable power saving for wifi.

`vi /media/dawszy/rootfs/etc/rc.local`

add following lines before "exit 0"
```
echo "Disabling wlan0 power_save"
/sbin/iw wlan0 set power_save off
```

after first boot

systemctl disable hciuart
systemctl enable ssh

apt update
apt upgrade

apt install python3-pip python3-gpiozero git nginx-light
user pi:
pip3 install fastapi
pip3 install uvicorn
pip3 install picamera

git clone https://github.com/sq6emm/4x4-rover.git

sudo bash

cp 4x4-rover/api/rover-api.service /lib/systemd/system/
cp 4x4-rover/cam/rover-cam.service /lib/systemd/system/

systemctl daemon-reload
systemctl enable rover-api.service
systemctl enable rover-cam.service
systemctl start rover-api.service
systemctl start rover-cam.service

cp 4x4-rover/nginx/sites-available/default /etc/nginx/sites-available/default
systemctl restart nginx

NOW MAKE RPI readonly...

apt remove --purge triggerhappy cron logrotate dbus avahi-daemon triggerhappy bluez
apt autoremove

dphys-swapfile swapoff
dphys-swapfile uninstall
update-rc.d dphys-swapfile remove
