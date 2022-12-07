#!/bin/bash

echo "starting wifi"
wpa_passphrase "Aleksei R" "98765432" | sudo tee -a /etc/wpa_supplicant.conf
sudo wpa_supplicant -B -c /etc/wpa_supplicant.conf -i wlan0
sudo dhclient wlan0
echo "started wifi"

