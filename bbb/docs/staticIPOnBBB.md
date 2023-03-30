# Steps to Set Up Static IP on BeagleBone

1. Connect to the BeagleBone via SSH or a serial connection.

```
ssh debian@beaglebone.local
```

2. Open the /etc/network/interfaces file using a text editor:

```
$ sudo nano /etc/network/interfaces
```

3. Add the following lines to the bottom of the file to configure the static IP address:

```
auto eth0
iface eth0 inet static
    address <IP address>
    netmask <netmask>
    gateway <default gateway>
    dns-nameservers <DNS servers>
```

For example:

```
auto eth0
iface eth0 inet static
    address 192.168.6.3
    netmask 255.255.255.0
    gateway 172.20.10.1
    dns-nameservers 8.8.8.8
    dns-nameservers 8.8.4.4
```

4. Press Ctrl+X, then Y, then Enter to save the changes and exit the editor.

5. Restart the networking service to apply the changes:

```
$ sudo service networking restart
```

### Not Sure if this is needed

6. Run the following command to open the resolv.conf file:

```
$ sudo nano /etc/resolv.conf`
```

7. Add the Following:

```
nameserver <DNS server>
# if you have the 2nd DNS server, add it here
nameserver <DNS server #2>
```

# Notes

### To find the IP address of the BeagleBone

```
ifconfig
```

### To find the default gateway (Not verified | Recommended by GitHub Copilot)

```
route -n
```

### To find the DNS server (Not verified | Recommended by GitHub Copilot)

```
cat /etc/resolv.conf
```

# ChatGPT Walk Through

To give a permanent IP address to a BeagleBone, you can configure it to use a static IP address instead of obtaining one dynamically from a DHCP server. Here are the general steps:

Connect to the BeagleBone: Connect to the BeagleBone via SSH or a serial connection.

Edit the network configuration file: Open the /etc/network/interfaces file using a text editor:

```
$ sudo nano /etc/network/interfaces
```

Configure the static IP address: Add the following lines to the bottom of the file to configure the static IP address:

```
auto eth0
iface eth0 inet static
address <IP address>
netmask <netmask>
gateway <default gateway>
dns-nameservers <DNS servers>
```

Replace <IP address> with the desired static IP address, <netmask> with the netmask of the network (usually 255.255.255.0), <default gateway> with the IP address of the default gateway, and <DNS servers> with the IP addresses of one or more DNS servers (separated by spaces).

For example, if you want to give the BeagleBone a static IP address of 192.168.1.100, with netmask 255.255.255.0, default gateway 192.168.1.1, and DNS server 8.8.8.8, you would add the following lines:

```
auto eth0
iface eth0 inet static
    address 192.168.1.100
    netmask 255.255.255.0
    gateway 192.168.1.1
    dns-nameservers 8.8.8.8
```

Save and exit the file: Press Ctrl+X, then Y, then Enter to save the changes and exit the editor.

Restart the networking service: Restart the networking service to apply the changes:

```
$ sudo service networking restart
```

After completing these steps, the BeagleBone should use the static IP address you configured instead of obtaining one dynamically from a DHCP server. Note that you may need to update any other devices or services that rely on the BeagleBone's IP address to use the new static IP address.

# Possibly Helpful Resources

1. https://ofitselfso.com/Beagle/NetworkingSetupConnectingTheBeagleboneBlack.php
2. https://www.tecmint.com/set-add-static-ip-address-in-linux/
