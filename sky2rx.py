#!/usr/bin/python

import socket
import time
import sys
import datetime
import pytz
from time import gmtime, strftime, localtime
from datetime import datetime
from suntime import Sun, SunTimeException
import json
import subprocess
from PIL import Image
from PIL import ImageDraw

latitude = -27.46
longitude = 153.03

sun = Sun(latitude, longitude)

response1 = """HTTP/1.1 200 OK
Allow: POST, OPTIONS
Server: Python/1.2.3
""" 
response2 = """
Content-Type: application/json;charset=utf-8
X-Frame-Options: SAMEORIGIN
Transfer-Encoding: chunked
Connection: close

62
"""

if len(sys.argv[1:]) != 1:
	print("Usage: sudo python3 ./tcp_proxy.py <device IP address>")
	sys.exit()

# setup local 
local_host = sys.argv[1]
if local_host == '0.0.0.0':
	local_host = ''
local_port = 80

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	server.bind((local_host, local_port))
except:
	print("Failed to listen on %s:%d" % (local_host, local_port))
	sys.exit()

print("Listening on %s:%d" % (local_host, local_port))
server.listen(5)

while True:
	client_socket, addr = server.accept()
	print("Received incoming connection from %s:%d" % (addr[0], addr[1]))
	print('Dowloading Sky 2 data...')

	sky2data = b""
	responded = False
	while True:
		data = client_socket.recv(5120)
		if len(data) < 1: break
		#time.sleep(0.25)
		sky2data = sky2data + data
		# Look for the end of the header (2 CRLF)
		pos = sky2data.find(b"\r\n\r\n")
		if pos and not responded:
			responded = True
			print('Sending 200 response to Sky 2...')
			dtnow = pytz.timezone('GMT').localize(datetime.utcnow())
			today_sr = str(int(sun.get_sunrise_time().timestamp()) - 86400)
			today_ss = str(int(sun.get_sunset_time().timestamp())) 
			epoch_time = str(int(time.time()))
			response_header = response1 + 'Date: %s' % dtnow.strftime('%a, %d %b %Y %H:%M:%S %Z') + response2
			response_header += '{"ResponseValue":200,"Message":0,'
			response_header += '"SunsetTime":' + today_ss + ',"TS":' + epoch_time + ',"SunriseTime":' + today_sr + "}\n0\n\n"
			client_socket.send(response_header.encode())
			print('\n' + response_header)
			print('Dowloading Sky 2 picture data...')
		
	print("Dowloading finished. Sky 2 data size: " + str(len(sky2data)))	
	client_socket.close()
	print('Closed connection to Sky 2.')
	print('Processing data, header length:', pos)
	sky2data2 = sky2data[:pos]
	# Look for the end of the JSON (1 CRLF)
	pos2 = sky2data2.find(b"\r\n")
	json_data = sky2data2[:pos2].decode()
	json_data = json_data.replace('POST /devc/skydevice/?Info=','')
	json_data = json_data.replace(' HTTP/1.1','')
	fhand = open('json.txt', "wt")
	fhand.write(json_data)
	fhand.close()
	# Saving JSON data to server
	subprocess.run(["sudo", "mv", "json.txt", "/var/www/html/sky2/"])
	print('JSON saved.')
	
	if len(sky2data) > 1000:
		# Skip past the header and save the picture data
		date_filename = strftime("%Y%m%d_%H%M:", localtime())
		date_filename = date_filename + '.jpg'
		picture = sky2data[pos+4:]
		fhand = open('latest_sky2.jpg', "wb")
		fhand.write(picture)
		fhand.close()
		# Add time etc. to image
		jd = json.loads(json_data)
		datetime_text = datetime.fromtimestamp(jd["TS"])
		img = Image.open('latest_sky2.jpg')
		I1 = ImageDraw.Draw(img)
		I1.text((15, 15), str(datetime_text), fill=(255, 0, 0))
		I1.text((15, 25), str(jd["Temperature"]) + "C", fill=(255, 0, 0))
		I1.text((15, 35), str(jd["Humidity"]) + "%", fill=(255, 0, 0))
		I1.text((15, 45), str(jd["Pressure"]) + "hPa", fill=(255, 0, 0))
		volts = str(jd["Voltage"] / 1000) + "V"
		if jd["ChargerStatus"]:
			volts = volts + "+"
		I1.text((15, 55), volts, fill=(255, 0, 0))
		img.save("latest_sky2.jpg")
		# Save to web server
		subprocess.run(["sudo", "mv", "latest_sky2.jpg", "/var/www/html/sky2/"])
		print('Picture saved.')
	else:
		print('No picture data.')
	
	print("\nListening on %s:%d" % (local_host, local_port))
