#!/bin/bash
cronfile="/home/pi/jasper/setup/cron.orig"

if [[ ! -f $cronfile ]]; then
   crontab -l > $cronfile
   echo cron backup made
fi

cronwork="/home/pi/jasper/setup/cron.tmp"
cp $cronfile $cronwork

cronwork="/home/pi/jasper/setup/cron.tmp"
cp $cronfile $cronwork

sed -i 's\^@reboot /home/pi/jasper/boot/boot.sh;\#@reboot /home/pi/jasper/boot/boot.sh;\g' $cronwork
crontab $cronwork
rm $cronwork





