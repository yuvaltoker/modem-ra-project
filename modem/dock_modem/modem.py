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

def isModemDying(battery, informed_dying):
    if int(battery) <= 15 and not informed_dying:
        return True
    return False

def updateModemState(modem_name, redis_field, state):
    global client
    global battery_value, channel_value, isAlive_value
    if "battery" in redis_field:
        battery_value = state
    elif "channel" in redis_field:
        channel_value = state
    elif "isAlive" in redis_field:
        isAlive_value = state
    client.hset(modem_name, redis_field, state)

def getModemVariable(modem_name, redis_field):
    global client
    return client.hget(modem_name, redis_field)


def incramentTime():
    global timer
    time.sleep(1)
    timer += 1


client = redis.Redis(host = 'redis_db', port = 6379)

rand = random.Random()

# is changed personally for every modem to "modem_NO_x", x stands for the modem's id
modem_name = 'modem_NO_3'

max_channel = 12

min_channel = 0

battery_value = 100

channel_value = rand.randint(min_channel, max_channel)

isAlive_value = "ALIVE"

timer = 0

redis_battery_field = "batteryObjectField"

redis_channel_field = "channelObjectField"

redis_isAlive_field = "isAliveObjectField"

update_battery_time = 5

update_channel_time = 30

battery_usage = 1

def main():
    global client
    global rand
    global modem_name
    global max_channel, min_channel
    global battery_value, channel_value, isAlive_value
    global timer, update_battery_time, update_channel_time, battery_usage
    global redis_battery_field, redis_channel_field, redis_isAlive_field
    informed_dying = False

    informRaAboutSituation(modem_name + " is now available")
    updateModemState(modem_name, redis_battery_field, battery_value)
    updateModemState(modem_name, redis_channel_field, channel_value)
    updateModemState(modem_name, redis_isAlive_field, isAlive_value)

    while True:
        while isModemAlive(battery_value):
            incramentTime()
            print(timer)
            battery_value = int(getModemVariable(modem_name, redis_battery_field))
            channel_value = int(getModemVariable(modem_name, redis_channel_field))
            if haveXSecondsPassed(timer, update_battery_time):
                print("%s - %i" % ("battery" , battery_value))
                battery_value = battery_value - battery_usage
                # updating the redis_db of the new battery state
                updateModemState(modem_name, redis_battery_field, battery_value)
                if isModemDying(battery_value, informed_dying):
                    updateModemState(modem_name, redis_isAlive_field, "DYING")
                    informRaAboutSituation(modem_name + " is dying")
                    informed_dying = True
            if haveXSecondsPassed(timer, update_channel_time):
                channel_value = rand.randint(min_channel, max_channel)
                print("%s - %i" % ("channel" , channel_value))
                # updating the redis_db of the new channel state
                updateModemState(modem_name, redis_channel_field, channel_value)

        # modem died :(update isAlive && sending message about that)
        updateModemState(modem_name, redis_isAlive_field, "DEAD")
        informRaAboutSituation(modem_name + " is dead")

        #checking if someone brought the modem back to life (future feature)
        battery_value = getModemVariable(modem_name, redis_battery_field)
        while not isModemAlive(battery_value):
            incramentTime()
            battery_value = getModemVariable(modem_name, redis_battery_field)
        
        # modem is back to life
        updateModemState(modem_name, redis_isAlive_field, "ALIVE")
        informed_dying = False





if __name__ == "__main__":
    main()
