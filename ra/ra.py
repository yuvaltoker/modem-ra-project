import redis
import socket
from datetime import datetime, date

client = rediss.Redis(host = 'redis_db', port = 6379)

port = 162
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", port))

numOfModems = 0
numOfConnected = 0
isModemAlive = []
addresses = []
start_time = datetime.datetime.utcnow()

while True:
    if numOfConnected == 0:
        print("Waiting for modems")

    data, addr = s.recvfrom(4048)
    message  = "message" # receiving snmptrap message


    # checking wether the message is String ("im here" / "im dead")
    #                                integer(battery / channel updating)
    if message == "string": #
        if message == "im here": #
            # welcome new modem, lets add you to the list and DB
        if message == "im dead": #
            # bye bye... lets update everything


    if message == "integer": #
        if message == "battery": #
            # update the DB about the modem's battery
        if message == "channel": #
            # update the DB about the modem's channel


    now_time = datetime.datetime.utcnow()
    duration = (start_time - now_time).total_seconds()
    if duration % 10 == 0:
        # printing the modems from DB
