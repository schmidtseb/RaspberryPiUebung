#!/bin/bash
# sudo su

# setzt neues passwort für user pi
echo "pi:raspberrypi01" | chpasswd

sed -i s/lehrkraft84/seminar01/g /etc/hostapd/hostapd.conf
sed -i s/raspberrypi84/raspberrypi01/g /etc/hostapd/hostapd.conf
sed -i s/channel\=84/channel\=1/g /etc/hostapd/hostapd.conf
sed -i s/raspberrypi84/raspberrypi01/g /etc/hostname
sed -i s/raspberrypi84/raspberrypi01/g /etc/hosts

# sudo /etc/init.d/hostname.sh
# sudo reboot
