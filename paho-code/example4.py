
# File: example4.py
#
# A very simple example of an MQTT producer.

import sys
import time
import random

import paho.mqtt.client as mqtt

THE_BROKER = "test.mosquitto.org"
THE_TOPIC = "PMtest/rndvalue"

mqttc=mqtt.Client()
mqttc.connect(THE_BROKER, 1883, 60)

mqttc.loop_start()

while True:
    mqttc.publish(THE_TOPIC, random.randint(0, 100))
    time.sleep(5)

mqttc.loop_stop()
