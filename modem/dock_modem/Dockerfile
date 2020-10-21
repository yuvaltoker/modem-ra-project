# What image do we start from
FROM polinux/snmpd
# The instructions for when the container is on && making it executive:
COPY ./instructions.sh /
RUN chmod +x /instructions.sh
# The mib files
COPY ./MY-TUTORIAL-MIB.txt /usr/share/snmp/mibs/
COPY ./NET-SNMP-TUTORIAL-MIB.txt /usr/share/snmp/mibs/
# Installing helpful functioning for the programmer's use
RUN yum install -y nano
# When the container is on, execute the instruction file
ENTRYPOINT ["bash","/instructions.sh"]
