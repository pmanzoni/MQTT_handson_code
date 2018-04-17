# file: a_simple_sub.py

from mqtt import MQTTClient
import pycom
import sys
import time

import ufun

wifi_ssid = 'LOCAL_AP'
wifi_passwd = ''
broker_addr = 'test.mosquitto.org'
dev_id = 'PMtest'

def settimeout(duration):
   pass

def on_message(topic, msg):
    print("Received msg: ", str(msg), "with topic: ", str(topic))

### if __name__ == "__main__":

ufun.connect_to_wifi(wifi_ssid, wifi_passwd)

client = MQTTClient(dev_id, broker_addr, 1883)
client.set_callback(on_message)

print ("Connecting to broker: " + broker_addr)
try:
	client.connect()
except OSError:
	print ("Cannot connect to broker: " + broker_addr)
	sys.exit()	
print ("Connected to broker: " + broker_addr)

client.subscribe('lopy/lights')

print('Waiting messages...')
while 1:
    client.check_msg()
