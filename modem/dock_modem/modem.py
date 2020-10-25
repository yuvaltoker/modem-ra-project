#!/usr/bin/env python3

import time
import random
import redis
from datetime import datetime
#from pysnmp.hlapi import *


global client
client = redis.Redis(host = 'redis_db', port = 6379)
global rand
rand = random.Random()
global modem_name
modem_name = "modem_NO_1" # is changed personally for every modem to "modem_NO_x", x stands for the modem's id
global num_of_channels
num_of_channels = 12
global battery
battery = 100
global channel
channel = rand.randint(0, num_of_channels)
global timer
timer = 0
global check_on_battery
check_on_battery = 0

def main():
    global client
    global rand
    global modem_name
    global num_of_channels
    global battery
    global channel
    global timer
    global check_on_battery
    client.hset(modem_name, "batteryObjectField", battery)
    client.hset(modem_name, "channelObjectField", channel)
    while True:
        while battery > 0:
            time.sleep(1)
            timer += 1
            battery = client.hget(modem_name, "batteryObjectField")
            channel = client.hget(modem_name, "channelObjectField")
            if timer % 5 == 0:
                battery -= 1
                # updating the redis_db of the new battery state
                client.hset(modem_name, "batteryObjectField", battery)
            if timer % 30 == 0:
                channel = rand.randint(0, num_of_channels)
                # updating the redis_db of the new channel state
                client.hset(modem_name,"channelObjectField", channel)

        # modem died :(sending message about that)
        check_on_battery = client.hget(modem_name, "batteryObjectField")
        while check_on_battery <= 0:
            time.sleep(1)
            check_on_battery = client.hget(modem_name, "batteryObjectField")


if __name__ == "__main__":
    main()
