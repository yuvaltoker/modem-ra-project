# What image do we start from
FROM polinux/snmpd
# Making directories, for the files to be contained, in the container 
RUN mkdir new_snmpd_test
RUN mkdir new_snmpd_test/hiredis
# The instructions for when the container is on && making it executive:
COPY ./instructions.sh /new_snmpd_test/
RUN chmod +x /new_snmpd_test/instructions.sh
# The mib files 
COPY ./MY-TUTORIAL-MIB.txt /usr/share/snmp/mibs
COPY ./NET-SNMP-TUTORIAL-MIB.txt /usr/share/snmp/mibs
# A former try with subagent, is working with the mibs of NET-SNMP-TUTORIAL-MIB:
COPY ./mysubagent /new_snmpd_test/
# Files which set the subagent behaviour with the mibs:
COPY ./subagents.c /new_snmpd_test/
COPY ./subagents.h /new_snmpd_test/
COPY ./nstAgentSubagentObject.c /new_snmpd_test/
COPY ./nstAgentSubagentObject.h /new_snmpd_test/
# Unites the above files and use their functions:
COPY ./example-daemon.c /new_snmpd_test/
# Contains redis library for C usage:
ADD ./hiredis /new_snmpd_test/hiredis/
# The makefile which builds the executive "example-daemon" AKA the subagent for the additioned mibs:
COPY ./Makefile /new_snmpd_test/
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
ENTRYPOINT ["bash","/new_snmpd_test/instructions.sh"]

