`192.168.7.2 putty`
`172.20.10.5`
`sudo iwlist wlan0 scan | grep -i ssid`
`sudo iwlist wlan0 scan`


## AUTOMATIC RECONNECTION TO WIFI (must be run in sudo)
https://unix.stackexchange.com/questions/483678/debian-connect-to-wifi-automatically-when-in-range/612173#612173


## To set SSID and Wi-Fi password:
`wpa_passphrase your-ESSID your-wifi-passphrase | sudo tee -a /etc/wpa_supplicant.conf`

`wpa_passphrase "Aleksei R" "98765432" | sudo tee -a /etc/wpa_supplicant.conf`


## To connect to Wi-Fi (must have hotspot turned on):
`sudo wpa_supplicant -B -c /etc/wpa_supplicant.conf -i wlan0`

`sudo dhclient wlan0`



`ip addr show wlan0`

## To fix RNET link already exists error:
`sudo ip addr flush dev wlan0`

#ignore
Tutorial for setting up new BB:
-Connect WiFi over USB: network and sharing -> properties -> sharing