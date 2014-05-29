sudo sed -i 's/options snd-pcsp/#options snd-pcsp/g' /etc/modprobe.d/alsa-base.conf
sudo sed -i 's/options snd-usb-audio/#options snd-usb-audio/g' /etc/modprobe.d/alsa-base.conf
sudo alsa force-reload
sed -i 's/hw:1,0/plughw:0,0/g' /home/pi/jasper/jasper.conf
