import time
import random
from datetime import datetime
from pysnmp.hlapi import *


num_of_channels = 12
battery = 100
channel = random(0, num_of_channels)
timer = 0

def main():
    while battery > 0:
        time.sleep(1)
        timer += 1
        if timer % 5 == 0:
            battery -= 1
            # snmptrap updating the nms of the new battery state
        if timer % 30 == 0:
            channel = random(0, num_of_channels)
            # snmptrap updating the nms of the new channel state



    # modem died :(sending message about that)

if __name__ == "__main__":
    main()
