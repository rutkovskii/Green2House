#!/bin/bash

# Run these commands before trying to run ./wifi.sh
#vi wifi.sh
#:set ff=unix
#:wq!

echo "starting wifi"
wpa_passphrase "<Your WIFI Name>" "Your Password" | sudo tee -a /etc/wpa_supplicant.conf
sudo wpa_supplicant -B -c /etc/wpa_supplicant.conf -i wlan0
sudo dhclient wlan0
echo "started wifi"

