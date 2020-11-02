#!/usr/bin/env python3

import socket
from datetime import datetime, date
from pysnmp.carrier.asynsock.dispatch import AsynsockDispatcher
from pysnmp.carrier.asynsock.dgram import udp, udp6
from pyasn1.codec.ber import decoder
from pysnmp.proto import api

numOfModems = 0
numOfDeadModems = 0



class snmptrapHandler(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    

	def cbFun(transportDispatcher, transportDomain, transportAddress, wholeMsg):
        global numOfModems
        global numOfDeadModems
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
		        #print('Var-binds:')
		        for oid, val in varBinds:
		            #print('%s = %s' % (oid.prettyPrint(), val.prettyPrint()))
                	message = val.prettyPrint() # ignoring past values, thus saving the last value - the snmptrap message itself 
                
                print('%s \n' % (message))
				if "is now available" in message:
					# welcome new modem
                    numOfModems = numOfModems + 1
				if "is dead" in message:
					# how unfortunate... you will always be remembered, there are no modems like you "modem_NO_X"
                    numOfDeadModems = numOfDeadModems + 1
		return wholeMsg



    def run(self):
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




def printStateOfModems():
	print('you still need to wrtie the printStateOfModems() function in ra.py')
	global numOfModems
	global numOfDeadModems
    print('------------------------------------------\n')
    print('\n')
    print('Status of all modems:')
    
    for i in range(1, numOfModems):
    	

    print('\n\n%s total, %s on & good, %s dying and %s dead' %(numOfModems, , , numOfDeadModems))
    print('\n')
    print('------------------------------------------\n')
  

def isPrintStateTime(duration):
	if duration % 10 == 0:
		return True
	return False


def main():
    start_time = datetime.datetime.utcnow()
	trapDaemon = snmptrapHandler(s, clientID)
    trapDaemon.start()
	while True:
	    now_time = datetime.datetime.utcnow()
	    duration = (start_time - now_time).total_seconds()
	    if isPrintStateTime(duration):
			# printing the modems from DB
        	printStateOfModems()





if __name__ == "__main__":
    main()
