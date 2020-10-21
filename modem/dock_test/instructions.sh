#!/bin/bash

declare -i x=1
sleep 15
while true; do
#    snmpset -v2c -c public testing_snmpd:1662 MY-TUTORIAL-MIB::batteryObject.0 i $x >> file.log
#    snmpset -v2c -c public testing_snmpd:1662 NET-SNMP-TUTORIAL-MIB::nstAgentSubagentObject.0 i $x >> file.log
#    snmpget -v2c -c public testing_snmpd:1662 MY-TUTORIAL-MIB::batteryObject.0 >> file.log
#    snmpget -v2c -c public testing_snmpd:1662 NET-SNMP-TUTORIAL-MIB::nstAgentSubagentObject.0 >> file.log

    x=x+1
    sleep 5
done
