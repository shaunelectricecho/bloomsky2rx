# bloomsky2rx
## Using a Raspberry Pi as a weather data and image server to replace the bloomsky.com server for a Bloomsky Sky2 device. 

Recently (Apr 2022) I purchased an expensive Bloomsky Sky2 device but it won't fully register and their tech support has vanished.

### Set up the Rasberry Pi as a Wireless Access Point ###
Firstly I set up the Pi as a wireless access point using these directions;
https://pimylifeup.com/raspberry-pi-wireless-access-point/

Using a WiPi USB dongle on a Pi 2B running Raspian buster and so removed the line 'driver=nl80211' from the hostapd.conf file.
Also wherever the instructions use the term **wlan0** replaced it with **wlx00c141000b99** gleamed from running the ifconfig command on the Pi.

### Attach a Bloomsky Sky 2 device to the Pi WAP ###
Used the Bloomsky phone app to attach the Sky2 to the new Pi wlan (right up to the point where it says 'name already exists loser'). You may need to finish up by short-press the Sky2 wifi button to stop it flashing. If you need to start again then long-press it for about 10 seconds.

If you have ethernet internet wired to your Pi then you can monitor the Sky 2 chatter with the bloomsky server (I did that a lot!) (and imagined how nice it would be if you could log into your sky2 dashboard and see your data and images) I used Wireshark and tcpdump to do the monitoring.

### Some Pi housekeeping ###
I needed to shut down the apache server on my Pi for access to port 80: **sudo systemctl stop apache2**

Then redirected the URL 'bskybackend.bloomsky.com' to the Pi's WAP inet address (as per ifconfig) in **sudo nano /etc/hosts** by adding the line: **192.168.220.1	bskybackend.bloomsky.com**

Then restarted the dnsmasq service: **sudo service dnsmasq restart**

### Run The Script ###
I've butchered the code/ideas from these three sources:
- https://github.com/slowmotionprojects/icestupa/blob/master/bloomsky_offline_hack/
- https://www.andrewmohawk.com/2020/01/28/picking-apart-an-iot-camera-bloomsky/
- http://www.py4e.com/code3/urljpeg.py

Being a simple person I liked the structure of the code in urljpeg.py many will disagree.

Run the code thusly: **sudo python3 ./sky2rx.py 192.168.220.1**

The site long/lats are hard coded for the sun up/down times so you'll need to change to yours. Basically the script sends the Sky 2 device the local sunrise, sunset and current times in the 200 response so that it only sends photos during the day.

