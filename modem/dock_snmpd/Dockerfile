# What image do we start from
FROM polinux/snmpd

# Making directories, for the files to be contained, in the container 
RUN mkdir create_snmpd
RUN mkdir create_snmpd/hiredis

# The instructions for when the container is on && making it executive:
COPY ./instructions.sh /create_snmpd/
RUN chmod +x /create_snmpd/instructions.sh

# The mib files 
COPY ./MY-TUTORIAL-MIB.txt /usr/share/snmp/mibs
COPY ./NET-SNMP-TUTORIAL-MIB.txt /usr/share/snmp/mibs

# A former try with subagent, is working with the mibs of NET-SNMP-TUTORIAL-MIB:
COPY ./mysubagent /create_snmpd/

# Files which set the subagent behaviour with the mibs:
COPY ./subagents.c /create_snmpd/
COPY ./subagents.h /create_snmpd/
COPY ./nstAgentSubagentObject.c /create_snmpd/
COPY ./nstAgentSubagentObject.h /create_snmpd/

# Unites the above files and use their functions:
COPY ./example-daemon.c /create_snmpd/

# Contains redis library for C usage:
ADD ./hiredis /create_snmpd/hiredis/

# The makefile which builds the executive "example-daemon" AKA the subagent for the additioned mibs:
COPY ./Makefile /create_snmpd/

# Configuration file of the snmpd:
COPY ./snmpd.conf /etc/snmp/

# Installing helpful functioning for the programmer's use && requiered libs for the subagent
RUN yum install -y make
RUN yum install -y nano
RUN yum install -y net-snmp-utils
RUN yum install -y gcc
RUN yum install -y net-snmp-devel
RUN yum install -y libevent-devel
RUN yum install -y http://repo.okay.com.mx/centos/7/x86_64/release/okay-release-1-1.noarch.rpm
RUN yum install -y hiredis
RUN yum install -y hiredis-devel

# When the container is on, execute the instruction file
ENTRYPOINT ["bash","/create_snmpd/instructions.sh"]

