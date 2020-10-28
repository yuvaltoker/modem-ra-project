#!/usr/bin/env python3

import time
import random
import redis
from datetime import datetime
from pysnmp.hlapi import *
from pysnmp import debug


def informRaAboutSituation(situation):
    errorIndication, errorStatus, errorIndex, varbinds = next(sendNotification(SnmpEngine(),
        CommunityData('public'),
        UdpTransportTarget(('ra', 162)),
        ContextData(),
        'trap',
        [ObjectType(ObjectIdentity('.1.3.6.1.6.3.1.1.5.1.0'), OctetString('coldStart test trap - ignore')), 
        ObjectType(ObjectIdentity('.1.3.6.1.2.1.1.4.0'), OctetString('sysContact trap - ' + situation))])
    )

    if errorIndication:
        print(errorIndication)
    else:
        print("successfully sent trap")


def haveXSecondsPassed(timer, seconds):
    if int(timer % seconds) == 0:
        return True
    return False

def isModemAlive(battery):
    if int(battery) > 0:
        return True
    return False

def incramentTime():
    global timer
    time.sleep(1)
    timer += 1

#global client
client = redis.Redis(host = 'redis_db', port = 6379)
#global rand
rand = random.Random()
#global modem_name
modem_name = "modem_NO_1" # is changed personally for every modem to "modem_NO_x", x stands for the modem's id
#global num_of_channels
num_of_channels = 12
#global battery_value
battery_value = 100
#global channel_value
channel_value = rand.randint(0, num_of_channels)
#global timer
timer = 0
#global redis_battery_field
redis_battery_field = "batteryObjectField"
#global redis_channel_field
redis_channel_field = "channelObjectField"

def main():
    global client
    global rand
    global modem_name
    global num_of_channels
    global battery_value
    global channel_value
    global timer
    global redis_battery_field
    global redis_channel_field


    informRaAboutSituation(modem_name + " is now available")
    client.hset(modem_name, redis_battery_field, battery_value)
    client.hset(modem_name, redis_channel_field, channel_value)
    while True:
        while isModemAlive(battery_value):
            incramentTime()
            print(timer)
            battery_value = int(client.hget(modem_name, redis_battery_field))
            channel_value = int(client.hget(modem_name, redis_channel_field))
            if haveXSecondsPassed(timer, 5):
                print("%s - %i" % ("battery" , battery_value))
                battery_value = battery_value - 1
                # updating the redis_db of the new battery state
                client.hset(modem_name, redis_battery_field, battery_value)
            if haveXSecondsPassed(timer, 30):
                channel_value = rand.randint(0, num_of_channels)
                print("%s - %i" % ("channel" , channel_value))
                # updating the redis_db of the new channel state
                client.hset(modem_name, redis_channel_field, channel_value)

        # modem died :(sending message about that)
        informRaAboutSituation(modem_name + " is dead")

        #checking if someone brought the modem back to life (future feature)
        battery_value = client.hget(modem_name, redis_battery_field)
        while not isModemAlive(battery_value):
            incramentTime()
            battery_value = client.hget(modem_name, redis_battery_field)






if __name__ == "__main__":
    main()
