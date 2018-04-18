# File: example5_prod.py
#
# Pub/Sub with JSON

import json
import random
import sys
import time

import paho.mqtt.client as mqtt

THE_BROKER = "test.mosquitto.org"
THE_TOPIC = "PMtest/jsonvalue"

mqttc=mqtt.Client()
mqttc.connect(THE_BROKER, 1883, 60)

mqttc.loop_start()

while True:
    # Getting the data
    the_time = time.strftime("%H:%M:%S")
    the_value = random.randint(1,100)
    the_msg={'Sensor': 1, 'C_F': 'C', 'Value': the_value, 'Time': the_time}

    the_msg_str = json.dumps(the_msg)

    print(the_msg_str)

    mqttc.publish(THE_TOPIC, the_msg_str)
    time.sleep(5)

mqttc.loop_stop()


