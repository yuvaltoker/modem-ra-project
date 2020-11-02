#!/usr/bin/env python3


import socket
from datetime import datetime, date

from pysnmp.carrier.asynsock.dispatch import AsynsockDispatcher
from pysnmp.carrier.asynsock.dgram import udp, udp6
from pyasn1.codec.ber import decoder
from pysnmp.proto import api
from pysnmp.hlapi import *
from pysnmp.smi import builder, view, compiler



def cbFun(transportDispatcher, transportDomain, transportAddress, wholeMsg):
    print('cbFun is called')
    while wholeMsg:
        print('loop...')
        msgVer = int(api.decodeMessageVersion(wholeMsg))
        if msgVer in api.protoModules:
            pMod = api.protoModules[msgVer]
        else:
            print('Unsupported SNMP version %s' % msgVer)
            return
        reqMsg, wholeMsg = decoder.decode(
            wholeMsg, asn1Spec=pMod.Message(),
            )
        print('Notification message from %s:%s: ' % (
            transportDomain, transportAddress
            )
        )
        reqPDU = pMod.apiMessage.getPDU(reqMsg)
        if reqPDU.isSameTypeWith(pMod.TrapPDU()):
            if msgVer == api.protoVersion1:
                print('Enterprise: %s' % (
                    pMod.apiTrapPDU.getEnterprise(reqPDU).prettyPrint()
                     )
                )
                print('Agent Address: %s' % (
                    pMod.apiTrapPDU.getAgentAddr(reqPDU).prettyPrint()
                    )
                )
                print('Generic Trap: %s' % (
                    pMod.apiTrapPDU.getGenericTrap(reqPDU).prettyPrint()
                    )
                )
                print('Specific Trap: %s' % (
                    pMod.apiTrapPDU.getSpecificTrap(reqPDU).prettyPrint()
                    )
                )
                print('Uptime: %s' % (
                    pMod.apiTrapPDU.getTimeStamp(reqPDU).prettyPrint()
                    )
                )
                varBinds = pMod.apiTrapPDU.getVarBindList(reqPDU)
            else:
                varBinds = pMod.apiPDU.getVarBinds(reqPDU)
            print('Var-binds:')
            for oid, val in varBinds:
                print('%s = %s' % (oid.prettyPrint(), val.prettyPrint()))
    return wholeMsg

def runDispatcherFunction():
    
    transportDispatcher = AsynsockDispatcher()

    transportDispatcher.registerRecvCbFun(cbFun)

    # UDP/IPv4
    transportDispatcher.registerTransport(
        udp.domainName, udp.UdpSocketTransport().openServerMode(('', 162))
    # if test.py is running inside a container named "ra", the traps messages will be for exampleL:
    #snmptrap -v2c -c public ra:162 '' SNMPv2-MIB::coldStart.0 SNMPv2-MIB::sysContact.0 s 'trap testing number #7'  
    )

    # UDP/IPv6
    #transportDispatcher.registerTransport(
    #    udp6.domainName, udp6.Udp6SocketTransport().openServerMode(('::1', 162))
    #)

    transportDispatcher.jobStarted(1)

    try:
        # Dispatcher will never finish as job#1 never reaches zero
        print('run dispatcher')
        transportDispatcher.runDispatcher()
    except:
        transportDispatcher.closeDispatcher()
        raise


def snmpsetFunction(objectOID, value):
    for (errorIndication,
     errorStatus,
     errorIndex,
     varBinds) in setCmd(SnmpEngine(),
                          CommunityData('public', mpModel=1),
                          UdpTransportTarget(('snmpd', 1662)),
                          ContextData(),
                          ObjectType(ObjectIdentity(objectOID), Integer32(value)),
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
    #engine = SnmpEngine()
    #community = CommunityData('public', mpModel=1)
    #transport = UdpTransportTarget(('snmpd', 1662))
    #context = ContextData()

    #mibBuilder = builder.MibBuilder() 
    #mibPath = mibBuilder.getMibSources()+(builder.DirMibSource('/root/.pysnmp/mibs'),)
    #mibBuilder.setMibSources(*mibPath)
    #mibBuilder.loadModules('MY-TUTORIAL-MIB')
    #mibView = view.MibViewController(mibBuilder)
    ## Your OID goes here.
    #identity = ObjectIdentity(objectOID).resolveWithMib(mibView)

    ## If this was a string value, use OctetString() instead of Integer().
    ##new_value = OctetString(value)
    #new_value = value
    #type = ObjectType(identity, new_value)

    ## Setting lookupMib=False here because this example uses a numeric OID.
    #g = setCmd(engine, community, transport, context, identity, type, lexicographicMode=True)

    #errorIndication, errorStatus, errorIndex, varBinds = next(g)
    #print(errorIndication, varBinds)

def snmpgetFunction(objectOID):

    g = getCmd(SnmpEngine()
              , CommunityData('public', mpModel=1)
              , UdpTransportTarget(('snmpd', 1662))
              , ContextData()
              , ObjectType(ObjectIdentity(objectOID)))

    errorIndication, errorStatus, errorIndex, varBinds = next(g)

    for oid, val in varBinds:
        print('%s' % (val))

    #g = getCmd(SnmpEngine(),
    #        CommunityData('public'),
    #        UdpTransportTarget(('demo.snmplabs.com', 161)),
    #        ContextData(),
    #        ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysUpTime', 0)))
    #next(g)


def main():
    
    batteryObjectOID = '1.3.6.1.4.1.8072.2.4.1.1.4'
    channelObjectOID = '1.3.6.1.4.1.8072.2.4.1.1.5'
    currentObjectOID = '1.3.6.1.4.1.8072.2.4.1.1.6'
    isAliveObjectOID = '1.3.6.1.4.1.8072.2.4.1.1.7'
    snmpsetFunction(currentObjectOID, 3)
    snmpgetFunction(currentObjectOID)
    snmpgetFunction(batteryObjectOID)
    snmpgetFunction(channelObjectOID)
    snmpgetFunction(isAliveObjectOID)  

if __name__ == "__main__":
    main()


