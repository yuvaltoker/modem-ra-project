#!/usr/bin/env python3

import socket
import threading
import datetime
import time
#from datetime import datetime, date
from pysnmp.carrier.asynsock.dispatch import AsynsockDispatcher
from pysnmp.carrier.asynsock.dgram import udp, udp6
from pyasn1.codec.ber import decoder
from pysnmp.proto import api
from pysnmp.hlapi import *
from pysnmp.smi import builder, view, compiler
from threading import Thread, Lock, Event

numOfModems = 0



def cbFun(transportDispatcher, transportDomain, transportAddress, wholeMsg):
        global numOfModems
        print('cbFun is called')
        while wholeMsg:
            print('loop...')
            msgVer = int(api.decodeMessageVersion(wholeMsg))
            if msgVer in api.protoModules:
                pMod = api.protoModules[msgVer]
            else:
                print('Unsupported SNMP version %s' % msgVer)
                return
            reqMsg, wholeMsg = decoder.decode(wholeMsg, asn1Spec=pMod.Message(),)
            print('Notification message from %s:%s: ' % (transportDomain, transportAddress))
            reqPDU = pMod.apiMessage.getPDU(reqMsg)
            if reqPDU.isSameTypeWith(pMod.TrapPDU()):
                if msgVer == api.protoVersion1:
                    print('Enterprise: %s' % (pMod.apiTrapPDU.getEnterprise(reqPDU).prettyPrint()))
                    print('Agent Address: %s' % (pMod.apiTrapPDU.getAgentAddr(reqPDU).prettyPrint()))
                    print('Generic Trap: %s' % (pMod.apiTrapPDU.getGenericTrap(reqPDU).prettyPrint()))
                    print('Specific Trap: %s' % (pMod.apiTrapPDU.getSpecificTrap(reqPDU).prettyPrint()))
                    print('Uptime: %s' % (pMod.apiTrapPDU.getTimeStamp(reqPDU).prettyPrint()))
                    varBinds = pMod.apiTrapPDU.getVarBindList(reqPDU)
                else:
                    varBinds = pMod.apiPDU.getVarBinds(reqPDU)
                #print('Var-binds:')
                message = ""
                for oid, val in varBinds:
                    #print('%s = %s' % (oid.prettyPrint(), val.prettyPrint()))
                    message = val.prettyPrint() # ignoring past values, thus saving the last value - the snmptrap message itself 
                
                print('%s \n' % message)
                if "is now available" in message:
                    # welcome new modem
                    numOfModems = numOfModems + 1
                if "is dead" in message:
                    print("modem died")
                    # how unfortunate... you will always be remembered, there are no modems like you "modem_NO_X"
                    # getting you back to life(?)
        return wholeMsg

class snmptrapHandler(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    @classmethod
    def run(self):
                transportDispatcher = AsynsockDispatcher()

                transportDispatcher.registerRecvCbFun(cbFun)

                # UDP/IPv4
                transportDispatcher.registerTransport(
                    udp.domainName, udp.UdpSocketTransport().openServerMode(('', 162)))
                # if test.py is running inside a container named "ra", the traps messages will be for exampleL:
                #snmptrap -v2c -c public ra:162 '' SNMPv2-MIB::coldStart.0 SNMPv2-MIB::sysContact.0 s 'trap testing number #7'

                transportDispatcher.jobStarted(1)

                try:
                    # Dispatcher will never finish as job#1 never reaches zero
                    print('run dispatcher')
                    transportDispatcher.runDispatcher()
                except:
                    transportDispatcher.closeDispatcher()
                    raise



def snmpsetFunction(objectOID, new_value):
    for (errorIndication,
     errorStatus,
     errorIndex,
     varBinds) in setCmd(SnmpEngine(),
                          CommunityData('public', mpModel=1),
                          UdpTransportTarget(('snmpd', 1662)),
                          ContextData(),
                          ObjectType(ObjectIdentity(objectOID), Integer32(new_value)),
                          lookupMib=False):

     if errorIndication:
         print(errorIndication)
         break
     elif errorStatus:
         print('%s at %s' % (errorStatus.prettyPrint(),
                             errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
         break
     else:
         for oid, val in varBinds:
             print('%s = %s' % (oid, val))

def snmpgetFunction(objectOID):

    g = getCmd(SnmpEngine()
              , CommunityData('public', mpModel=1)
              , UdpTransportTarget(('snmpd', 1662))
              , ContextData()
              , ObjectType(ObjectIdentity(objectOID)))

    errorIndication, errorStatus, errorIndex, varBinds = next(g)

    for oid, val in varBinds:
        return (val)


def printStateOfModems():
    batteryObjectOID = '1.3.6.1.4.1.8072.2.4.1.1.4'
    channelObjectOID = '1.3.6.1.4.1.8072.2.4.1.1.5'
    currentObjectOID = '1.3.6.1.4.1.8072.2.4.1.1.6'
    isAliveObjectOID = '1.3.6.1.4.1.8072.2.4.1.1.7'

    global numOfModems
    print('------------------------------------------\n')
    print('\n')
    print('Status of all modems:\n')
    numOfWellModems = 0
    numOfDyingModems = 0
    numOfDeadModems = 0
    for i in range(1, numOfModems + 1): # wantedto start with i=1, so the last one will be num + 1 
        snmpsetFunction(currentObjectOID, i)
        battery = snmpgetFunction(batteryObjectOID)
        channel = snmpgetFunction(channelObjectOID)
        state = snmpgetFunction(isAliveObjectOID)
        if state == "ALIVE":
            numOfWellModems = numOfWellModems + 1
        elif state == "DYING":
            numOfDyingModems = numOfDyingModems + 1
        elif state == "DEAD":
            numOfDeadModems = numOfDeadModems + 1
        print("Modem NO.%d is %s:" % (i, state))
        print("    battery = %s\n    channel = %s\n\n" % (battery, channel))
        
    print('\n\n%s total, %s on & good, %s dying and %s dead' %(numOfModems, numOfWellModems, numOfDyingModems, numOfDeadModems))
    print('\n')
    print('------------------------------------------\n')


def isPrintStateTime(duration):
    if int(duration % 10) == 0:
        return True
    return False


def main():
    start_time = datetime.datetime.now()
    trapDaemon = snmptrapHandler()
    trapDaemon.start()
    while True:
        #consider moving into time.sleep()
        #now_time = datetime.datetime.now()
        #duration = (start_time - now_time).total_seconds()
        #if isPrintStateTime(duration):
            # printing the modems from DB
        printStateOfModems()
        time.sleep(10)




if __name__ == "__main__":
    main()
