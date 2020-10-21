#!/bin/bash



echo "snmpd:127.0.0.1" >> /etc/hosts.allow
echo "snmptrapd: 127.0.0.1" >> /etc/hosts.allow
echo "master agentx" >> /etc/snmp/snmpd.conf # for the futue snmpd, doesn't belong to the current example
echo "authCommunity   log,execute,net public" >> /etc/snmp/snmptrapd.conf
echo "forward default unix:/var/opt/FJSVssmgr/trap_socket" >> /etc/snmp/snmptrapd.conf
echo "traphandle SNMPv2-MIB::coldStart    /tmp/go cold" >> /etc/snmp/snmptrapd.conf
echo "traphandle SNMPv2-MIB::sysContact   /tmp/go contact" >> /etc/snmp/snmptrapd.conf
cp ./go /tmp/
snmptrapd -f -Lf file.log -c /etc/snmp/snmptrapd.conf -M /usr/share/snmp/mibs --agentXSocket=tcp:localhost:161 udp:162

