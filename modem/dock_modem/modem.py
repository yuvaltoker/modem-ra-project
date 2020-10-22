import time
import random
import redis
from datetime import datetime
from pysnmp.hlapi import *


client = redis.Redis(host = 'redis_db', port = 6379)

modem_name = "modem_NO_" # is changed personally for every modem to "modem_NO_x", x stands for the modem's id
num_of_channels = 12
battery = 100
channel = random(0, num_of_channels)
timer = 0
check_on_battery = 0

def main():
    client.hset(modem_name, "batteryObjectField", battery, "channelObjectField", channel)
    while true:
        while battery > 0:
            time.sleep(1)
            timer += 1
            if timer % 5 == 0:
                battery -= 1
                # updating the redis_db of the new battery state
                client.hset(modem_name, "batteryObjectField", battery)
            if timer % 30 == 0:
                channel = random(0, num_of_channels)
                # updating the redis_db of the new channel state
                client.hset(modem_name,"channelObjectField", channel)

        # modem died :(sending message about that)
        check_on_battery = client.hget(modem_name, "batteryObjectField")
        while check_on_battery <= 0:
            time.sleep(1)
            check_on_battery = client.hget(modem_name, "batteryObjectField")


if __name__ == "__main__":
    main()
