#!/bin/bash

while true; do
# actuall garbage, snmpset and snmpget examples, the main event here is the loop so that the container will keep up running
#    snmpset -v2c -c public snmpd:1662 MY-TUTORIAL-MIB::batteryObject.0 i $x >> file.log
#    snmpset -v2c -c public snmpd:1662 NET-SNMP-TUTORIAL-MIB::nstAgentSubagentObject.0 i $x >> file.log
#    snmpget -v2c -c public snmpd:1662 MY-TUTORIAL-MIB::batteryObject.0 >> file.log
#    snmpget -v2c -c public snmpd:1662 NET-SNMP-TUTORIAL-MIB::nstAgentSubagentObject.0 >> file.log
#    snmpset -v2c -c public :1662 MY-TUTORIAL-MIB::currentObject.0 i 0 >> file.log
    sleep 5
done
