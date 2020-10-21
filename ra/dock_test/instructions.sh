#!/bin/bash

declare -i x=1
while true; do
    sleep 5
    snmptrap -v2c -c public testing_snmptrapd:162 '' SNMPv2-MIB::coldStart.0 SNMPv2-MIB::sysContact.0 s 'trap number #'$x
    x=x+1
done

