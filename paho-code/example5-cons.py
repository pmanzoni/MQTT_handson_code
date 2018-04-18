# File: example5_cons.py
#
# Pub/Sub with JSON

import json
import sys
import time

import paho.mqtt.client as mqtt

THE_BROKER = "test.mosquitto.org"
THE_TOPIC = "PMtest/jsonvalue"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

    themsg = json.loads(str(msg.payload))

    print("Sensor "+str(themsg['Sensor'])+" got value "+
    	str(themsg['Value'])+" "+themsg['C_F']+
    	" at time "+str(themsg['Time']))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(THE_BROKER, 1883, 60)
client.subscribe(THE_TOPIC)

client.loop_forever()

