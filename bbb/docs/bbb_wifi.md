192.168.7.2 putty

172.20.10.5

sudo iwlist wlan0 scan | grep -i ssid

sudo iwlist wlan0 scan

# To connect to Wi-Fi (must have hotspot turned on):
### sudo wpa_supplicant -B -c /etc/wpa_supplicant.conf -i wlan0
### sudo dhclient wlan0
## don't use these, instead use nmcli
https://unix.stackexchange.com/questions/483678/debian-connect-to-wifi-automatically-when-in-range/612173#612173


ip addr show wlan0

#To fix RNET link already exists error:

sudo ip addr flush dev wlan0


################################

# installing rtl8812bu driver
### use the RTL8812BU-master github
### download folder to BBB, open and type:
make

### wait for completion, will take a while
sudo make install

sudo reboot

## When making, if the arch/armv71 Makefile error appears,
## go to /usr/src/linux/arch/ and enter:
sudo ln -s arm armv7l


