ssh debian@beaglebone.local
scp dht20v2.py debian@beaglebone.local:/home/debian/greenhouse

`wpa_passphrase "Aleksei R" 98765432 | sudo tee -a /etc/wpa_supplicant/wpa_supplicant.conf`