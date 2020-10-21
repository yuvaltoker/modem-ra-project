#!/bin/bash


echo "snmpd:127.0.0.1" >> /etc/hosts.allow
echo "master agentx" >> /etc/snmp/snmpd.conf

snmpd -f -Lf snmpd_file.log -C -M /usr/share/snmp/mibs --rwcommunity=public --master=agentx --agentXSocket=tcp:localhost:161 udp:1662 &

#make example-daemon
#./example-daemon -f -Lf subagent_file.log -x  tcp:localhost:161 &

while true; do
    sleep 5
done
