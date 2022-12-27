#!/bin/bash

# Run these commands before trying to run ./wifi.sh
#vi wifi.sh
#:set ff=unix
#:wq!

echo "starting wifi"
wpa_passphrase "<Your WIFI Name>" "<Your Password>" | tee -a /etc/wpa_supplicant.conf
wpa_supplicant -B -c /etc/wpa_supplicant.conf -i wlan0
dhclient wlan0
echo "started wifi"

