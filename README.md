# bloomsky2rx
## Using a Raspberry Pi as a weather data and image server to replace the bloomsky.com server for a Bloomsky Sky2 device. 

Recently I purchased an expensive Bloomsky Sky2 device but it won't fully register and their tech support has vanished.

Firstly I set up the Pi as a wireless access point using these directions;
https://pimylifeup.com/raspberry-pi-wireless-access-point/

I'm using a WiPi USB dongle on a pi 2B running Raspian buster and so removed the 'driver=nl80211' line from the hostapd.conf file.
Also wherever the instructions use the term **wlan0** I replaced it with **wlx00c141000b99** gleamed from running the ifconfig command on the pi.

The I used the Bloomsky phone app to attach the Sky2 to the new pi wlan (right up to the point where it says 'name already exists loser').

If you have ethernet internet wired to your pi then you can monitor the Sky 2 chatter with the bloomsky server (I did that a lot!) (and imagined how nice it would be if you could log into your sky2 dashboard and see your data and images) I used Wireshark and tcpdump to do the monitoring.

I needed to shut down the apache server on my pi for access to port 80: **sudo systemctl stop apache2**

The redirected the URL 'bskybackend.bloomsky.com' to the pi's WAP inet address in **sudo nano /etc/hosts** by adding the line: **192.168.220.1	bskybackend.bloomsky.com**

Then restarted the dnsmasq service: **sudo service dnsmasq restart**

Then I butchered the code/ideas from these three sources:
https://github.com/slowmotionprojects/icestupa/blob/master/bloomsky_offline_hack/
https://www.andrewmohawk.com/2020/01/28/picking-apart-an-iot-camera-bloomsky/
http://www.py4e.com/code3/urljpeg.py

I'm a simple person so I liked the structure of the code in urljpeg.py many will disagree.

I run my code thusly: **sudo python3 ./sky2rx.py 192.168.220.1**
