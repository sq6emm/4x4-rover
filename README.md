Simple project to controll Rover Robot. Web with cam and API.

## Installation instructions
# Prepare SD card

`curl https://downloads.raspberrypi.org/raspios_lite_armhf/images/raspios_lite_armhf-2020-12-04/2020-12-02-raspios-buster-armhf-lite.zip --output 2020-12-02-raspios-buster-armhf-lite.zip`

`unzip 2020-12-02-raspios-buster-armhf-lite.zip`

`dd if=2020-12-02-raspios-buster-armhf-lite.img of=/dev/sdb` (write to SD card)

touch /boot/ssh

cat >> /boot/config.txt
start_x=1
gpu_mem=128
disable_camera_led=1
dtoverlay=disable-bt
gpio=18,19,20,21=op,dl
gpio=4,17,22,27=op,dl

cat > /etc/wpa_supplicant/wpa_supplicant.conf


/etc/rc.local
echo "Disabling wlan0 power_save"
/sbin/iw wlan0 set power_save off

echo "wariatuncio-dev" > /etc/hostname
echo "127.0.2.1 wariatuncio-dev" >> /etc/hosts

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
