# An hands-on introduction to MQTT 

This lab is organized so that you can have an hands-on experience with MQTT and learn how to "publish" and "subscribe" to data. To this end you will use:
1. your own broker
1. a "sandbox" broker
1. the **ThingSpeak** platform
2. the **Ubidots** platform

You will learn how to:
* install and configure an MQTT broker
* interchange data using MQTT
* use MQTT to feed data to cloud based IoT platforms

## Hardware

> All devices in the lab must share the same WLAN.

Each group will use a computer and a LoPy connected via USB through either an extension board or a PySense board. The various elements are supposed to be connected as indicated in the figure below.
![The connections](https://i.imgur.com/h5D9umj.jpg)



# Installing the MQTT broker

> ***You can install a broker either in you computer or, if you have one available, in a Raspberry Pi.***

### Installation steps:
For our experiments we will use [**Mosquitto**](https://mosquitto.org/), which is part of the [Eclipse Foundation](http://www.eclipse.org/) and is an [iot.eclipse.org](https://projects.eclipse.org/projects/technology.mosquitto) project. The manual page can be found here [`man page`](https://mosquitto.org/man/mosquitto-8.html).

Installation indications can be found here: https://mosquitto.org/download/ 

* Linux distros like Debian/UBUNTU/Raspian already have Mosquitto in their repositories... so it's enough with:
```shell=bash
sudo apt-get update
sudo apt-get install mosquitto mosquitto-clients
```

* with *Ubuntu MATE* maybe you'll need to add this before:
`sudo apt-add-repository ppa:mosquitto-dev/mosquitto-ppa` 

* with Macs, Mosquitto can be installed from the homebrew project. See  http://brew.sh/ and then use “brew install mosquitto”


### Managing the broker


#### ... with Debian/UBUNTU/Raspian
To start and stop its execution use:
```shell=bash
sudo /etc/init.d/mosquitto start/stop
```
if necessary, to avoid that it restarts automatically, do: `sudo stop mosquitto`

To run the broker execute:
```shell=bash
sudo mosquitto –v
```
> note: "-v" stands for "verbose mode" and can be useful at the beginning to see what is going on in the broker. Can be convenient to use a dedicated terminal for the broker to execute in, if the "-v" option is used.

To check if the broker is running you can use the command:
```shell=bash
sudo netstat -tanlp | grep 1883
```
> note: "-tanlp" stands for: tcp, all, numeric, listening, program

alternatively use:
```shell=bash
ps -ef | grep mosquitto
```


#### ... with Mac OS
To start and stop its execution use:
```shell=bash
/usr/local/sbin/mosquitto -v
```
> note: "-v" stands for "verbose mode" and can be useful at the beginning to see what is going on in the broker. Can be convenient to use a dedicated terminal for the broker to execute in, if the "-v" option is used.

or:
```shell=bash
/usr/local/sbin/mosquitto -c /usr/local/etc/mosquitto/mosquitto.conf
```
or:

```shell=bash
brew services start/stop mosquitto
```

To check if the broker is running you can use the command:
```shell=bash
sudo lsof -i -n -P | grep 1883
```

or:
```shell=bash
ps -ef | grep mosquitto
```



## Clients for testing
The broker comes with a couple of useful commands to quickly publish and subscribe to some topic. Their basic syntax is the following. 
```shell
mosquitto_sub -h HOSTNAME -t TOPIC
mosquitto_pub -h HOSTNAME -t TOPIC -m MSG
```
More information can be found:
* https://mosquitto.org/man/mosquitto_sub-1.html
* https://mosquitto.org/man/mosquitto_pub-1.html

---
---

# Block 1: some basic example.

## Set-up
Open three terminals (e.g., `xterm`) in your computer, more or less like this:
![](https://i.imgur.com/KOcNjwz.jpg=400x400)
The biggest terminal will be used to see the execution of the broker, the two smaller terminals will be used to execute the publisher and the subscriber, respectively.


> If the broker is not running locally in your computer but for example in a Raspberry Pi, connect **each terminal to it** via `ssh -X`.


Now, run the broker with the `-v` flag in the bigger terminal.

## Exercises

Let's start with a easy one. In one of the small terminals write:
```shell
mosquitto_sub -t i/LOVE/Python
```
the broker terminal should show something like:

![](https://i.imgur.com/5nMOywi.png)

the broker registered the subscription request of the new client. Now in the other small terminal, execute:
```shell
mosquitto_pub -t i/LOVE/Python -m "Very well!"
```
in the broker terminal, after the new registration messages, you'll also see something like:

![](https://i.imgur.com/s7zROiH.png)

meaning that the broker received the published message and that it forwarded it to the subscribed client. In the terminal where `mosquitto_sub` is executing you'll see the actual message appear.

Try now: 
```shell
mosquitto_pub -t i/love/python -m "Not so well!"
```
**What happened? Are topics case-sensitive?**

Another useful option of `mosquitto_pub` is the following:
```shell
mosquitto_pub -t i/LOVE/Python -l
```
it sends messages read from stdin, splitting separate lines into separate messages. Note that blank lines won't be sent. Give it a try ... you basically obtained a MQTT based **"unidirectional chat"** channel... 

### QoS (Quality of Service):
Adding the `-q` option, for example to the `mosquitto_pub` you'll see the extra message that are now interchanged with the broker. For example, doing:
```shell
mosquitto_pub -t i/LOVE/Python -q 2 -m testing
```

you'll get:

![](https://i.imgur.com/wLqMrev.png)

compare this sequence of messages with the one obtanined with `-q 0` or with `-q 1`.

### Retained messages:
Normally if a publisher publishes a message to a topic, and *no one is subscribed* to that topic the message is simply discarded by the broker. If you want your broker to remember the last published message, you'll have to use the ```retain``` option. Only one message is retained per topic. The next message published on that topic replaces the retained message for that topic. 
> To set the retain message flag you have to add `-r` using the Mosquitto clients.

So try the following cases, but  **remember now to start the subscriber after** the publisher:
1. Publish a message with the retain message flag not set, like we did before. What happens?
1. Publish a message with the retain message flag set (`-r`). What happens?
1. Publish several (different) messages with the retain message flag set before starting the subscriber. What happens?
2. Publish a message with the retain message flag **not** set again. What happens?

Finaly, how do I remove or delete a retained message? You have to publish a blank message with the retain flag set to true which clears the retained message. Try it.

### Public brokers
There are also various public brokers in Internet, also called `sandboxes`. For example:
* `test.mosquitto.org`
    * more infos at: http://test.mosquitto.org/
* `iot.eclipse.org`
    * more infos at: https://iot.eclipse.org/getting-started#sandboxes
* `broker.hivemq.com`
    * more infos at: http://www.hivemq.com/try-out/
        * http://www.mqtt-dashboard.com/
        
we will always access them through port `1883`. Repeat some of the exercise above with one of these sandboxes (remember to use the `-h` option). Any difference?





# Block 2: MQTT clients with MicroPython and the LoPy

> **All the code that you will be using is available here https://github.com/pmanzoni/MQTT_handson_code**


## First, some basic code

### The `ufun.py` library
To ease the programming of the following exercises some generic code is provided in a library called ```ufun.py```  available in the repository indicated above. The library provides the code to: 
* `connect_to_wifi()`: connects the LoPy to a WiFi LAN. By properly passing the values `wifi_ssid` and `wifi_passwd`  this function will try three times to connect to the specified AP, exiting if the operation is not possible. 
* `random_in_range()`: generates random numbers in a range, and 
* `set_led_to()` and `flash_led_to()`: simplify the control of the LED. 

_Take a look at the code  to understand how it works._


### Installing the MQTT client library in the LoPy

The LoPy devices require a MQTT library to write the client application. The code is available in the [above described repository.](#Block-2-MQTT-clients-with-MicroPython-and-the-LoPy) You basically need to download the **`mqtt.py`** file and copy it in the directory of your project. 


## Let's start: a simple subscriber

The code below represent a simple subscriber. As a first step it connects to the WiFi network available in the lab.

> **Remeber to properly assign a value to variables: `wifi_ssid`, `wifi_passwd`, and `dev_id`.**

> In this case we use the broker `test.mosquitto.org` but you can use any other accesible broker.

```python=
# file: a_simple_sub.py

from mqtt import MQTTClient
import time
import sys
import pycom

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

```

**Now, in a terminal and using `mosquitto_pub`, write the proper command to send some message to the LoPy.**

## A simple publisher

Let's produce some random data using the code below. As before, it first connects to the WiFi network available in the lab.
> **Remeber to properly assign a value to variables: `wifi_ssid`, `wifi_passwd`, and `dev_id`.**

> In this case we use the broker `test.mosquitto.org` but you can use any other accesible broker.

```python=
# file: a_simple_pub.py

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

def get_data_from_sensor(sensor_id="RAND"):
    if sensor_id == "RAND":
        return ufun.random_in_range()

### if __name__ == "__main__":

ufun.connect_to_wifi(wifi_ssid, wifi_passwd)

client = MQTTClient(dev_id, broker_addr, 1883)

print ("Connecting to broker: " + broker_addr)
try:
	client.connect()
except OSError:
	print ("Cannot connect to broker: " + broker_addr)
	sys.exit()	
print ("Connected to broker: " + broker_addr)

print('Sending messages...')
while True:
    # creating the data
    the_data = get_data_from_sensor()
    # publishing the data
    client.publish(dev_id+'/sdata', str(the_data))
    time.sleep(1)

```

**Now, in a terminal and using `mosquitto_sub`, write the proper command to read the generated data.**


---

# Block 3: Final exercises
Now let's work on some final exercises to put together most of what we saw in this lab session. Since you'll have to write some MQTT Python program (_not MicroPython_  :smirk:)  for your computer, you have to install the [Paho library](https://www.eclipse.org/paho/clients/python/) that I described in class; it's just one step, execute:

```shell
sudo pip install paho-mqtt
```

## The first
Let's control remotely the color of the LoPy's LED using MQTT.

![block 3, first exercise](https://i.imgur.com/3pnXsWm.jpg)

**Code “p1”.** This code runs in the LoPy, so must use MicroPython, and has to:
* Connect each group's LoPy to its own 'private' broker; 'private' means that each group should use a different broker, basically the one you installed at the beginning of this Lab session.
* Have the LoPy to change the color of its LED according to the "instructions" it receives using MQTT. Use the functions in library `ufun.py` to control the LED.

**Code “p2”.** This code runs in a computer, so must use Python, and has to:
* Connect to the LoPy 'private' broker. 
* Publish the "instructions", using MQTT, to 
 inform the LoPy to which color has to set its LED:
    1) Try first simply using: `mosquitto_pub`
    2) Then, write a program that reads 2 parameters: the broker address and the LED color you want that specific LoPy to show. 
    3) Finally, try to control the LoPy of another group.

## The second
Now repeat the previous exercise but using a unique ("common") broker for the whole lab. It could either be one running in a computer in the lab or a remote one (e.g., test.mosquitto.org). How will you identify a specific LoPy now? 

![block 3, second exercise](https://i.imgur.com/V2q18hb.jpg)


---

# Block 4: Extended exercises and projects hints

Accessing ThingSpeak and Ubidots via MQTT


## Using ThingSpeak

ThingSpeak is an IoT analytics platform service that allows you to aggregate, visualize and analyze live data streams in the cloud. ThingSpeak provides instant visualizations of data posted by your devices to ThingSpeak. With the ability to execute MATLAB® code in ThingSpeak you can perform online analysis and processing of the data as it comes in. 

### Creating a *channel*
You first have to sign in. Go to https://thingspeak.com/users/sign_up and create your own account. Then you can create your first channel. Like for example:
![](https://i.imgur.com/nN8iyWl.png)

In the "Private View" section you can get an overview of your data:
![](https://i.imgur.com/DzkbXVF.png)

Take a look to the other sections. To connect to your channel, you need the data in the API Keys section. In my case it says:
![](https://i.imgur.com/BlfIqlK.png)

Now, ThingSpeak offers either a REST and a MQTT API to work with channels. See here: https://es.mathworks.com/help/thingspeak/channels-and-charts-api.html

### Exercise
Let's publish to your channel field feed some random value using `mosquitto_pub`.

![](https://i.imgur.com/f4vfCTZ.png)

Consider that:
1. the hostname of the ThinSpeak MQTT service is "mqtt.thingspeak.com"
2. the topic you have to use is `channels/<channelID>/publish/fields/field<fieldnumber>/<apikey>` where you have to replace:
    * <channelID> with the channel ID,
    * <fieldnumber> with field number that you want to update, and 
    * <apikey> with the write API key of the channel. 
3. finally, remember that ThingSpeak requires you to:
    * set the PUBLISH messages to a QoS value of 0.
    * set the connection RETAIN flag to 0 (False).
    * set the connection CleanSession flag to 1 (True).
4.  more infos here
https://es.mathworks.com/help/thingspeak/publishtoachannelfieldfeed.html 


## Using Ubidots

Repeat the previous exercise with the Ubidots platform. You will have to first create your free account here: https://app.ubidots.com/accounts/signup/
