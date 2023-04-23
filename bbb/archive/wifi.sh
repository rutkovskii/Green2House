#!/bin/bash

# Run these commands before trying to run ./wifi.sh
#vi wifi.sh
#:set ff=unix
#:wq!

WIFI_NAME="<Your WIFI Name>"
WIFI_PASS="<Your WIFI Password>"

echo "starting wifi"
if ping -c 1 google.com &> /dev/null
then
    echo "internet is up"

else
    wpa_passphrase $WIFI_NAME $WIFI_PASS | tee -a /etc/wpa_supplicant.conf
    wpa_supplicant -B -c /etc/wpa_supplicant.conf -i wlan0
    dhclient wlan0
    echo "started wifi"
fi


