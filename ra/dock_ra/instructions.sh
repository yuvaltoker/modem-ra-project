#!/bin/bash


while true; do
    sleep 5
    #actuall garbage, snmptrap sending example. the main event here is the loop keeping the container up and running
    #snmptrap -v2c -c public testing_snmptrapd:162 '' SNMPv2-MIB::coldStart.0 SNMPv2-MIB::sysContact.0 s 'trap number #'$x
    #x=x+1
done

