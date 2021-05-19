#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
import datetime

printerChannel = 21
ledChannel = 18 

def on_connect(client, userdata, flags, rc):  # The callback for when the client connects to the broker
    now = datetime.datetime.now()
    print(now, ": Connected with result code {0}".format(str(rc)))  # Print result of connection attempt
    client.subscribe("ender/relay/0/command")  # Subscribe to the topic “digitest/test1”, receive any messages published on it
    client.subscribe("ender/relay/1/command")

def on_message(client, userdata, msg):  # The callback for when a PUBLISH message is received from the server.
    payload = msg.payload.decode('utf8')
    now = datetime.datetime.now()
    print(now, ": Message received-> " + msg.topic + " " + str(payload))  # Print a received msg
    action = str(payload)
    topic=""
    if msg.topic == "ender/relay/0/command":
        gpio = printerChannel
        topic = "ender/relay/0"
    elif msg.topic == "ender/relay/1/command":
        gpio = ledChannel
        topic = "ender/relay/1"

    if action == "on":
        turn_on(gpio)
        client.publish(topic, payload="on", qos=0, retain=False)
    elif action == "off":
        turn_off(gpio)
        client.publish(topic, payload="off", qos=0, retain=False)


def turn_on(pin):
    now = datetime.datetime.now()
    print(now, ": ON for "+str(pin))
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)  
    GPIO.output(pin, GPIO.HIGH)  # Turn on

def turn_off(pin):
    now = datetime.datetime.now()
    print(now, ": OFF for "+str(pin))
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)  # Turn off


if __name__ == '__main__':
    try:
        client = mqtt.Client("Ender controller")  # Create instance of client with client ID “digi_mqtt_test”
        client.on_connect = on_connect  # Define callback function for successful connection
        client.on_message = on_message  # Define callback function for receipt of a message

        client.connect('192.168.1.102', 1883)
        client.loop_forever()  # Start networking daemon

    except KeyboardInterrupt:
        now = datetime.datetime.now()
        print(now, ": CLOSING")
        GPIO.cleanup()
